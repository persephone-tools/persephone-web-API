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

