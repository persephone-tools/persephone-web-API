"""
Serialization for data defined in ORM/DB
"""

from marshmallow_sqlalchemy import ModelSchema

from . import db_models

class AudioSchema(ModelSchema):
    class Meta:
        model = db_models.Audio

class TranscriptionSchema(ModelSchema):
    class Meta:
        model = db_models.Transcription

class UtteranceSchema(ModelSchema):
    class Meta:
        model = db_models.Utterance

class CorpusSchema(ModelSchema):
    class Meta:
        model = db_models.Corpus
