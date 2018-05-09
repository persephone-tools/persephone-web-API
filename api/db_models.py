from . import db

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

class Audio(db.Model):
    """Database ORM definition for Audio files"""
    __tablename__ = 'audio'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    url = db.Column(db.String)

    in_utterances = db.relationship("Utterance", cascade="all, delete-orphan")

    def __repr__(self):
        return "<Audio(filename={}, url={})>".format(self.filename, self.url)


class Transcription(db.Model):
    """Database ORM definition for Transcription files"""
    __tablename__ = 'transcription'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    url = db.Column(db.String)

    in_utterances = db.relationship("Utterance", cascade="all, delete-orphan")

    def __repr__(self):
        return "<Transcription(filename={}, url={})>".format(self.filename, self.url)


class Utterance(db.Model):
    """Database ORM definiton for Utterances.
    This consists of a relationship between an Audio file and a transcription file
    """
    __tablename__ = 'utterance'

    id = db.Column(db.Integer, primary_key=True)

    audio_id = db.Column(
        db.Integer,
        db.ForeignKey('audio.id'),
        nullable=False,
    )
    audio = db.relationship('Audio', backref='utterances')

    transcription_id = db.Column(
        db.Integer,
        db.ForeignKey('transcription.id'),
        nullable=False,
    )
    transcription = db.relationship('Transcription', backref='utterances')

    def __repr__(self):
        return "<Utterance(audio={}, transcription={})>".format(self.audio, self.transcription)


class Corpus(db.Model):
    """Database ORM definiton for Corpus"""
    __tablename__ = 'corpus'

    id = db.Column(db.Integer, primary_key=True)
    # Persephone supports a default partition generation when the user does not supply
    # the partitions. Should we support this behavior in the API?
    # If yes we need a user supplied partition of traing/valid/test data sets flag
    # and the parameters with which the partition sizes are determined.

    def __repr__(self):
        return "<Corpus>"


class TrainingDataSet(db.Model):
    """This serves to facilitate mappings beween Utterances and Corpus as stored in the database"""
    __tablename__ = 'trainingdata'

    id = db.Column(db.Integer, primary_key=True)
    corpus_id = db.Column(
        db.Integer,
        db.ForeignKey('corpus.id'),
        nullable=False
    )
    corpus = db.relationship(Corpus)

    utterance_id = db.Column(
        db.Integer,
        db.ForeignKey('utterance.id'),
        nullable=False
    )
    utterance = db.relationship(Utterance)

    def __repr__(self):
        return "<TrainingDataSet(corpus={}, utterance={})>".format(self.corpus, self.utterance)


class ValidationDataSet(db.Model):
    """This serves to facilitate mappings beween Utterances and Corpus as stored in the database"""
    __tablename__ = 'validationdata'

    id = db.Column(db.Integer, primary_key=True)
    corpus_id = db.Column(
        db.Integer,
        db.ForeignKey('corpus.id'),
        nullable=False
    )
    corpus = db.relationship(Corpus)

    utterance_id = db.Column(
        db.Integer,
        db.ForeignKey('utterance.id'),
        nullable=False
    )
    utterance = db.relationship(Utterance)

    def __repr__(self):
        return "<ValidationDataSet(corpus={}, utterance={})>".format(self.corpus, self.utterance)


class TestingDataSet(db.Model):
    """This serves to facilitate mappings beween Utterances and Corpus as stored in the database"""
    __tablename__ = 'testingdata'

    id = db.Column(db.Integer, primary_key=True)
    corpus_id = db.Column(
        db.Integer,
        db.ForeignKey('corpus.id'),
        nullable=False
    )
    corpus = db.relationship(Corpus)

    utterance_id = db.Column(
        db.Integer,
        db.ForeignKey('utterance.id'),
        nullable=False
    )
    utterance = db.relationship(Utterance)

    def __repr__(self):
        return "<TestingDataSet(corpus={}, utterance={})>".format(self.corpus, self.utterance)
