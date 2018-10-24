import datetime

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection

from .extensions import db

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

class FileMetaData(db.Model):
    """Database ORM definition for file metadata"""
    __tablename__ = 'file_metadata'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Audio(db.Model):
    """Database ORM definition for Audio files"""
    __tablename__ = 'audio'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    url = db.Column(db.String)

    in_utterances = db.relationship("DBUtterance", cascade="all, delete-orphan")

    def __repr__(self):
        return "<Audio(filename={}, url={})>".format(self.filename, self.url)


class Transcription(db.Model):
    """Database ORM definition for Transcription files"""
    __tablename__ = 'transcription'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    url = db.Column(db.String)

    in_utterances = db.relationship("DBUtterance", cascade="all, delete-orphan")

    def __repr__(self):
        return "<Transcription(filename={}, url={})>".format(self.filename, self.url)


class DBUtterance(db.Model):
    """Database ORM definition for Utterances.
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
        return "<DBUtterance(audio={}, transcription={})>".format(self.audio, self.transcription)


class DBcorpus(db.Model):
    """Database ORM definition for DBcorpus"""
    __tablename__ = 'corpus'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # Persephone supports a default partition generation when the user does not supply
    # the partitions. Should we support this behavior in the API?
    # If yes we need a user supplied partition of train/valid/test data sets flag
    # and the parameters with which the partition sizes are determined.

    training = db.relationship('TrainingDataSet')
    testing = db.relationship('TestingDataSet')
    validation = db.relationship('ValidationDataSet')

    filesystem_path = db.Column(db.String)

    #Flag to track if DBcorpus has been preprocessed and ready for use in ML models
    preprocessed = db.Column(db.Boolean, unique=False, default=False)

    # the type of the feature files in this corpus
    feature_type = db.Column(db.String)

    # A string describing the transcription labels.
    # For example, “phonemes” or “tones”.
    label_type = db.Column(db.String)

    # The maximum number of samples an utterance in the corpus may have.
    # If an utterance is longer than this, it is not included in the corpus.
    max_samples = db.Column(db.Integer)

    def __repr__(self):
        return '<DBcorpus(name="{}", label_type="{}", feature_type="{}", max_samples="{}")>'.format(self.name, self.label_type, self.feature_type, self.max_samples)


class TrainingDataSet(db.Model):
    """This serves to facilitate mappings between Utterances and DBcorpus as stored in the database"""
    __tablename__ = 'trainingdata'

    id = db.Column(db.Integer, primary_key=True)
    corpus_id = db.Column(
        db.Integer,
        db.ForeignKey('corpus.id'),
        nullable=False
    )
    corpus = db.relationship(DBcorpus)

    utterance_id = db.Column(
        db.Integer,
        db.ForeignKey('utterance.id'),
        nullable=False
    )
    utterance = db.relationship(DBUtterance)

    def __repr__(self):
        return "<TrainingDataSet(corpus={}, utterance={})>".format(self.corpus, self.utterance)


class ValidationDataSet(db.Model):
    """This serves to facilitate mappings between Utterances and DBcorpus as stored in the database"""
    __tablename__ = 'validationdata'

    id = db.Column(db.Integer, primary_key=True)
    corpus_id = db.Column(
        db.Integer,
        db.ForeignKey('corpus.id'),
        nullable=False
    )
    corpus = db.relationship(DBcorpus)

    utterance_id = db.Column(
        db.Integer,
        db.ForeignKey('utterance.id'),
        nullable=False
    )
    utterance = db.relationship(DBUtterance)

    def __repr__(self):
        return "<ValidationDataSet(corpus={}, utterance={})>".format(self.corpus, self.utterance)


class TestingDataSet(db.Model):
    """This serves to facilitate mappings between Utterances and DBcorpus as stored in the database"""
    __tablename__ = 'testingdata'

    id = db.Column(db.Integer, primary_key=True)
    corpus_id = db.Column(
        db.Integer,
        db.ForeignKey('corpus.id'),
        nullable=False
    )
    corpus = db.relationship(DBcorpus)

    utterance_id = db.Column(
        db.Integer,
        db.ForeignKey('utterance.id'),
        nullable=False
    )
    utterance = db.relationship(DBUtterance)

    def __repr__(self):
        return "<TestingDataSet(corpus={}, utterance={})>".format(self.corpus, self.utterance)


class TranscriptionModel(db.Model):
    """Represents a transcription Model that specifies a RNN CTC neural network"""
    __tablename__ = 'transcriptionmodel'

    id = db.Column(db.Integer, primary_key=True)
    corpus_id = db.Column(
        db.Integer,
        db.ForeignKey('corpus.id'),
        nullable=False
    )
    corpus = db.relationship(DBcorpus)

    name = db.Column(db.String, nullable=False)

    min_epochs = db.Column(db.Integer, default=0, nullable=False)
    max_epochs = db.Column(db.Integer, nullable=True)

    # The number of layers in the network
    num_layers = db.Column(db.Integer, nullable=False)
    # The size of each layer
    hidden_size = db.Column(db.Integer, nullable=False)

    early_stopping_steps = db.Column(db.Integer, nullable=False)

    #Width of beam as used in beam search
    beam_width = db.Column(db.Integer, nullable=False)
    # Flag to toggle merging of repeated phonemes in results stream
    # for example "A B B B C" becomes "A B C" with this enabled
    decoding_merge_repeated = db.Column(db.Boolean, unique=False, default=True, nullable=False)

    # Maximum Label Error Rate on validation data set
    max_valid_LER = db.Column(db.Float)

    # Maximum Label Error Rate on validation training set
    max_train_LER = db.Column(db.Float)

    filesystem_path = db.Column(db.String, nullable=False)

    def __repr__(self):
        return ("<Model(name={}, corpus={}, min_epochs={}, max_epochs={}, "
               "max_valid_LER={}, max_train_LER={}, "
               "early_stopping_steps={}, beam_width={}, decoding_merge_repeated={})>").format(
                    self.name, self.corpus, self.min_epochs, self.max_epochs,
                    self.max_valid_LER, self.max_train_LER,
                    self.early_stopping_steps, self.beam_width, self.decoding_merge_repeated)


class Label(db.Model):
    """Represents a phonetic label"""
    __tablename__ = 'label'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Unicode, nullable=False, unique=True)
    def __repr__(self):
        return "<Label({})>".format(self.label)


class CorpusLabelSet(db.Model):
    """Represents a set of phonetic labels found in a corpus.
    This is used for keeping track of which labels a model was trained with"""
    __tablename__ = 'labelset'

    id = db.Column(db.Integer, primary_key=True)

    corpus_id = db.Column(
        db.Integer,
        db.ForeignKey('corpus.id'),
        nullable=False
    )
    corpus = db.relationship(DBcorpus)

    label_id = db.Column(
        db.Integer,
        db.ForeignKey('label.id'),
        nullable=False
    )
    label = db.relationship(Label)