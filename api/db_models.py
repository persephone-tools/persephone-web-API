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
    audio_id = db.Column(db.Integer, db.ForeignKey(Audio.id), primary_key=True)
    transcription_id = db.Column(db.Integer, db.ForeignKey(Transcription.id), primary_key=True)

    audio = db.relationship('Audio', foreign_keys='Audio.id')
    transcription = db.relationship('Transcription', foreign_keys='Transcription.id')

    def __repr__(self):
        return "<Utterance(audio={}, transcription={})>".format(self.audio, self.transcription)
