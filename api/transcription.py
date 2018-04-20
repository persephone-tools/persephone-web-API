"""
API endpoints for /transcription
This deals with the API access for transcription files uploading/downloading.
"""

def post(transcriptionFile):
    """handle POST request for transcription file"""
    print("Got {}".format(transcriptionFile))
    return "transcription upload not implemented", 501

def get(transcriptionID):
    print("Got transcription file ID {}".format(transcription))
    return "Get transcription info not implemented", 501
