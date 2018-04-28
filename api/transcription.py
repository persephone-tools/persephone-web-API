"""
API endpoints for /transcription
This deals with the API access for transcription files uploading/downloading.
"""
import flask_uploads

from .upload_config import text_files

def post(transcriptionFile):
    """handle POST request for transcription file"""
    print("Got {}".format(transcriptionFile))
    try:
        filename = text_files.save(transcriptionFile)
    except flask_uploads.UploadNotAllowed:
        return "Invalid upload format, must be a text file", 415
    return "transcription upload not implemented", 501

def get(transcriptionID):
    print("Got transcription file ID {}".format(transcription))
    return "Get transcription info not implemented", 501
