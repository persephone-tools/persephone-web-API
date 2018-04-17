"""
API endpoints for /utterance
"""

def post(wav_file, transcription_file):
    """POST request"""
    print("Got {} {}".format(wav_file, transcription_file))
    return "Utterance upload not implemented", 501
