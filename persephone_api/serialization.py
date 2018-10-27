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
    class Meta:
        model = db_models.TranscriptionModel

class LabelSchema(ModelSchema):
    class Meta:
        model = db_models.Label