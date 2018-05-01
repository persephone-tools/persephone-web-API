from . import db

class Audio(db.Model):
    """Database ORM definition for Audio files"""
    __tablename__ = 'audio'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    url = db.Column(db.String)

    def __repr__(self):
        return "<Audio(filename={}, url={})>".format(self.filename, self.url)


class Transcription(db.Model):
    """Database ORM definition for Transcription files"""
    __tablename__ = 'transcription'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    url = db.Column(db.String)

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
        db.ForeignKey('audio.id', ondelete='CASCADE'),
        nullable=False,
    )
    audio = db.relationship('Audio', backref='utterances')

    transcription_id = db.Column(
        db.Integer,
        db.ForeignKey('transcription.id', ondelete='CASCADE'),
        nullable=False,
    )
    transcription = db.relationship('Transcription', backref='utterances')

    def __repr__(self):
        return "<Utterance(audio={}, transcription={})>".format(self.audio, self.transcription)
