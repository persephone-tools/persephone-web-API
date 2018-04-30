"""
API endpoints for /utterance
"""

def post(utteranceInfo):
    """POST request"""
    audioId = utteranceInfo['audioId']
    transcriptionId = utteranceInfo['transcriptionId']
    print("Got audioId {} transcriptionId {}".format(audioId, transcriptionId))
    # TODO check that ID's for audio and transcription exist
    return "Utterance upload not implemented", 501
