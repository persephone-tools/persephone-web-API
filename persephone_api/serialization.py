"""
Serialization for data defined in ORM/DB
"""

from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from . import db_models

class FileInfoSchema(ModelSchema):
    """Serialization for file information"""
    class Meta:
        model = db_models.FileMetaData

class AudioSchema(ModelSchema):
    file_info = fields.Nested("FileInfoSchema")
    class Meta:
        model = db_models.Audio
        exclude = ("utterances",)

class TranscriptionSchema(ModelSchema):
    file_info = fields.Nested("FileInfoSchema")
    class Meta:
        model = db_models.Transcription
        exclude = ("utterances",)


class UtteranceSchema(ModelSchema):
    class Meta:
        model = db_models.DBUtterance

class CorpusSchema(ModelSchema):
    class Meta:
        model = db_models.DBcorpus

class TranscriptionModelSchema(ModelSchema):
    """Serialization for a transcription model
    The mappings here map the API to the DB names
    """
    beamWidth = fields.Int(attribute="beam_width")
    corpusID = fields.Int(attribute="corpus_id")
    decodingMergeRepeated = fields.Boolean(attribute="decoding_merge_repeated")
    earlyStoppingSteps = fields.Int(attribute="early_stopping_steps")
    hiddenSize = fields.Int(attribute="hidden_size")
    maximumEpochs = fields.Int(attribute="max_epochs")
    maximumTrainingLER = fields.Float(attribute="max_train_LER")
    maximumValidationLER = fields.Float(attribute="max_valid_LER")
    minimumEpochs = fields.Int(attribute="min_epochs")
    numberLayers = fields.Int(attribute="num_layers")
    class Meta:
        model = db_models.TranscriptionModel
        exclude = (
            'beam_width',
            'corpus',
            'decoding_merge_repeated',
            'early_stopping_steps',
            'filesystem_path',
            'hidden_size',
            'max_epochs',
            'max_train_LER',
            'max_valid_LER',
            'min_epochs',
            'num_layers',
        )


class LabelSchema(ModelSchema):
    class Meta:
        model = db_models.Label