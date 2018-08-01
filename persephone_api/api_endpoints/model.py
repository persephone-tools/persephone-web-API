"""
API endpoints for /model
This deals with the API access for model definitions and metadata
"""

from persephone.rnn_ctc import Model

from ..extensions import db
from ..db_models import TranscriptionModel
from ..serialization import TranscriptionModelSchema

def create_RNN_CTC_model(model: TranscriptionModel):
    """Create a persephone RNN CTC model"""
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
    min_epochs = modelInfo.get('minimumEpochs', None)
    max_epochs = modelInfo.get('maximumEpochs', None)
    if min_epochs and max_epochs and min_epochs > max_epochs:
        return "minimum number of epochs must be smaller than maximum", 400

    early_stopping_steps = modelInfo.get('', None)

    current_model = TranscriptionModel(
        name=modelInfo['name'],
        corpus=modelInfo['corpusID'],
        min_epochs=min_epochs,
        max_epochs=max_epochs,
        early_stopping_steps=early_stopping_steps
    )
    create_RNN_CTC_model(current_model)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return "Invalid model provided", 400
    else:
        raise NotImplementedError
