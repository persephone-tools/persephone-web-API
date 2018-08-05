"""
API endpoints for /model
This deals with the API access for model definitions and metadata
"""
from pathlib import Path
import uuid

import flask
from persephone import experiment
from persephone.rnn_ctc import Model
from persephone.corpus_reader import CorpusReader

from ..extensions import db
from ..db_models import DBcorpus, TranscriptionModel
from ..serialization import TranscriptionModelSchema

def create_RNN_CTC_model(model: TranscriptionModel):
    """Create a persephone RNN CTC model"""
    exp_dir = experiment.prep_exp_dir(directory=model.filesystem_path)
    corpus = DBcorpus.query.get_or_404(model.corpus)
    import pdb; pdb.set_trace()
    corpus_reader = CorpusReader(corpus, batch_size=batch_size)
    model = rnn_ctc.Model(
        exp_dir,
        corpus_reader,
        num_layers=model.num_layers,
        hidden_size=model.hidden_size,
        beam_width=model.beam_width,
        decoding_merge_repeated=model.decoding_merge_repeated
        )
    raise NotImplementedError

def search():
    """Handle request to search over all models"""
    results = []
    for row in db.session.query(TranscriptionModel):
        serialized = TranscriptionModelSchema().dump(row).data
        results.append(serialized)
    return results, 200

def get(modelID):
    """ Get a model by its ID"""
    transcription_model = TranscriptionModel.query.get_or_404(modelID)
    result = TranscriptionModelSchema().dump(transcription_model).data
    return result, 200

def post(modelInfo):
    """Create a new transcription model"""
    min_epochs = modelInfo.get('minimumEpochs', 0)
    max_epochs = modelInfo.get('maximumEpochs', None)
    if max_epochs and min_epochs > max_epochs:
        return "minimum number of epochs must be smaller than maximum", 400

    early_stopping_steps = modelInfo.get('earlyStoppingSteps', None)
    num_layers = modelInfo.get('numberLayers', None)
    hidden_size = modelInfo.get('hiddenSize', None)
    beam_width = modelInfo.get('beamWidth', None)
    decoding_merge_repeated = modelInfo.get('decodingMergeRepeated', True)

    current_model = TranscriptionModel(
        name=modelInfo['name'],
        corpus=modelInfo['corpusID'],
        num_layers=num_layers,
        hidden_size=hidden_size,
        min_epochs=min_epochs,
        max_epochs=max_epochs,
        beam_width=beam_width,
        decoding_merge_repeated=decoding_merge_repeated,
        early_stopping_steps=early_stopping_steps
    )

    model_uuid = uuid.uuid1()
    model_path = Path(flask.current_app.config['MODELS_PATH']) / str(model_uuid)
    current_model.filesystem_path = str(model_path)
    create_RNN_CTC_model(current_model)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return "Invalid model provided", 400
    else:
        result = TranscriptionModelSchema().dump(current_corpus).data
        return result, 201
