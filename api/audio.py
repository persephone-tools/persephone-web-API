"""
API endpoints for /audio
This deals with the API access for audio files uploading/downloading.
"""

def post(audioFile):
    """handle POST request for audio file"""
    print("Got {}".format(audioFile))
    return "Audio upload not implemented", 501
