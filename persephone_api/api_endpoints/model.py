"""
API endpoints for /model
This deals with the API access for model definitions and metadata
"""
from pathlib import Path
import pickle
import uuid

import flask
import sqlalchemy

from persephone import experiment
from persephone import rnn_ctc
from persephone.corpus_reader import CorpusReader
from persephone import model

from .corpus import labels_set

from ..db_models import Audio, DBcorpus, FileMetaData, Transcription, TranscriptionModel
from ..error_response import error_information
from ..extensions import db
from ..serialization import TranscriptionModelSchema
from ..upload_config import uploads_url_base


# quick and dirty way of persisting models, most certainly not fit for production
# in a multi user environment
available_models = {}

def get_transcription_model(model_id: int) -> model.Model:
    """Return an instance of a Persephone model for a given ID"""
    return available_models[model_id]

def register_transcription_model(model_id: int, model_object: model.Model) -> None:
    """Register a python object containing the transcription model"""
    available_models[model_id] = model_object

def decide_batch_size(num_train: int) -> int:
    """Determine size of batches for use in training"""
    if num_train >= 512:
        batch_size = 16
    elif num_train < 128:
        if num_train < 4:
            batch_size = 1
        else:
            batch_size = 4
    else:
        batch_size = int(num_train / 32)

    return batch_size

def create_RNN_CTC_model(model_db: TranscriptionModel, corpus_storage_path: Path,
                         models_storage_path: Path) -> rnn_ctc.Model:
    """Create a persephone RNN CTC model

    :model: The database entry contaning the information about the model attempting
            to be created here.
    :corpus_storage_path: The path the corpuses are stored at.
    :models_storage_path: The path the models are stored at.
    """
    model_path = models_storage_path / model_db.filesystem_path
    exp_dir = experiment.prep_exp_dir(directory=str(model_path))
    corpus_db_entry = model_db.corpus
    pickled_corpus_path = corpus_storage_path / corpus_db_entry.filesystem_path / "corpus.p"
    with pickled_corpus_path.open('rb') as pickle_file:
        corpus = pickle.load(pickle_file)

    corpus_reader = CorpusReader(corpus, batch_size=decide_batch_size(len(corpus.train_prefixes)))
    return rnn_ctc.Model(
        exp_dir,
        corpus_reader,
        num_layers=model_db.num_layers,
        hidden_size=model_db.hidden_size,
        beam_width=model_db.beam_width,
        decoding_merge_repeated=model_db.decoding_merge_repeated
        )

def search(pageNumber=1, pageSize=20):
    """Handle request to search over all models"""
    paginated_results = TranscriptionModel.query.paginate(
        page=pageNumber, per_page=pageSize, error_out=True
    )
    json_results = [TranscriptionModelSchema().dump(model).data for model in paginated_results.items]
    return json_results, 200

def get(modelID):
    """ Get a model by its ID"""
    transcription_model = TranscriptionModel.query.get_or_404(modelID)
    result = TranscriptionModelSchema().dump(transcription_model).data
    return result, 200

def post(modelInfo):
    """Create a new transcription model"""
    current_corpus = DBcorpus.query.get(modelInfo['corpusID'])
    if current_corpus is None:
        return error_information(
            status=400,
            title="The corpus ID provided is not available",
            detail="The corpus ID provided is not available, "
                   "make sure the corpus your model is using exists first.",
        )

    min_epochs = modelInfo.get('minimumEpochs', 0)
    max_epochs = modelInfo.get('maximumEpochs', None)
    if max_epochs and min_epochs > max_epochs:
        return error_information(
            status=400,
            title="Minimum epochs must be smaller than the maximum.",
            detail="Minimum epochs must be smaller than the maximum."
                   "Got max: {} min: {}. Check your parameters".format(max_epochs, min_epochs),
        )

    early_stopping_steps = modelInfo.get('earlyStoppingSteps', None)
    num_layers = modelInfo.get('numberLayers', 3)
    hidden_size = modelInfo.get('hiddenSize', 250)
    beam_width = modelInfo.get('beamWidth', 100)
    decoding_merge_repeated = modelInfo.get('decodingMergeRepeated', True)

    model_uuid = uuid.uuid1()

    current_model = TranscriptionModel(
        name=modelInfo['name'],
        corpus=current_corpus,
        num_layers=num_layers,
        hidden_size=hidden_size,
        min_epochs=min_epochs,
        max_epochs=max_epochs,
        beam_width=beam_width,
        decoding_merge_repeated=decoding_merge_repeated,
        early_stopping_steps=early_stopping_steps,
        filesystem_path=str(model_uuid),
        max_train_LER=modelInfo.get('maximumTrainingLER', 0.3),
        max_valid_LER=modelInfo.get('maximumValidationLER', 1.0)
    )

    db.session.add(current_model)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return error_information(
            status=400,
            title="Database error",
            detail="Database error",
        )
    else:
        result = TranscriptionModelSchema().dump(current_model).data
        return result, 201


def train(modelID):
    """Submit task to train a model"""
    current_model = TranscriptionModel.query.get_or_404(modelID)
    persephone_model = create_RNN_CTC_model(
        current_model,
        corpus_storage_path=Path(flask.current_app.config['CORPUS_PATH']),
        models_storage_path=Path(flask.current_app.config['MODELS_PATH'])
    )

    register_transcription_model(modelID, persephone_model)
    MAX_EPOCHS = 100 # TODO: Set maximum epochs somewhere else
    if current_model.max_epochs:
        epochs = current_model.max_epochs
    else:
        epochs = MAX_EPOCHS

    # we construct the parameters here so that the call to the model training
    # respects the default value for arguments as found in the Persephone library
    parameters = {
        "min_epochs": current_model.min_epochs,
        "max_epochs": epochs,
    }
    if current_model.early_stopping_steps is not None:
        parameters["early_stopping_steps"] = current_model.early_stopping_steps
    if current_model.max_valid_LER is not None:
        parameters["max_valid_ler"] = current_model.max_valid_LER
    if current_model.max_train_LER is not None:
        parameters["max_train_ler"] = current_model.max_train_LER

    persephone_model.train(**parameters)
    # TODO: Save this information about the network topology of tensorflow with the names
    # somewhere so it can be easily used in the transcribe step
    #print("persephone_model.batch_x: ", persephone_model.batch_x)
    #print("persephone_model.batch_x_lens: ", persephone_model.batch_x_lens)
    #print("persephone_model.dense_decoded: ", persephone_model.dense_decoded)

    return "Model trained", 200

def transcribe(modelID, audioID):
    """Transcribe audio with the given model"""
    current_model = TranscriptionModel.query.get_or_404(modelID)
    audio_info = Audio.query.get_or_404(audioID)
    # TODO: test that audio file is not empty

    # TODO: handle experiment number in path
    model_path = Path(flask.current_app.config['MODELS_PATH']) / current_model.filesystem_path / "0"
    model_checkpoint_path = model_path / "model" / "model_best.ckpt"
    audio_uploads_path = Path(flask.current_app.config['UPLOADED_AUDIO_DEST'])

    # putting features into the existing corpus path for now
    corpus_path = Path(flask.current_app.config['CORPUS_PATH']) / current_model.corpus.filesystem_path
    audio_path = audio_uploads_path / audio_info.file_info.name

    labels = [item.label for item in labels_set(current_model.corpus)]

    results = model.decode(
        model_checkpoint_path, [audio_path],
        labels,
        feature_type=current_model.corpus.featureType,
        batch_x_name="batch_x:0",
        batch_x_lens_name="batch_x_lens:0",
        output_name="hyp_dense_decoded:0"
        )

    transcribed_filename = "transcribed-{}".format(audio_info.file_info.name)
    file_url = uploads_url_base + 'text_uploads/' + transcribed_filename
    metadata = FileMetaData(path=file_url, name=transcribed_filename)

    if results[0] == []:
        text = ""
    else:
        text = " ".join(results[0])
    current_transcription = Transcription(
        file_info=metadata,
        url=file_url,
        name=transcribed_filename,
        text=text
    )
    db.session.add(current_transcription)
    db.session.commit()

    return results[0], 201
