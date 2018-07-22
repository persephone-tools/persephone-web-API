"""
Serialization for data defined in ORM/DB
"""

from marshmallow_sqlalchemy import ModelSchema

from . import db_models

class AudioSchema(ModelSchema):
    class Meta:
        model = db_models.Audio
        exclude = ("utterances",)

class TranscriptionSchema(ModelSchema):
    class Meta:
        model = db_models.Transcription
        exclude = ("utterances",)


class UtteranceSchema(ModelSchema):
    class Meta:
        model = db_models.DBUtterance

class CorpusSchema(ModelSchema):
    class Meta:
        model = db_models.Corpus

class TranscriptionModelSchema(ModelSchema):
    class Meta:
        model = db_models.TranscriptionModel