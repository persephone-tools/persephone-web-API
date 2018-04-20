"""
API endpoints for /audio
This deals with the API access for audio files uploading/downloading.
"""

def post(audioFile):
    """handle POST request for audio file"""
    print("Got {}".format(audioFile))
    return "Audio upload not implemented", 501


def get(audioID):
    """Handle GET request for audio file information.
    Note that this does not return the audio file directly but
    rather a JSON object with the relevant information.
    This allows the flexibility of file storage being handled
    by another service that is outside this API service."""
    print("Got audio file ID {}".format(audioID))
    return "Get audio info not implemented", 501
