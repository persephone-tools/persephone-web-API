"""These endpoints exist to handle bulk data uploading functionality.

Make these endpoints be behind an auth wall if possible.
"""
import logging
import os
from pathlib import Path
import tempfile
from zipfile import ZipFile

import flask
import flask_uploads

from .audio import create_audio
from .transcription import create_transcription

from ..db_models import FileMetaData
from ..error_response import error_information
from ..upload_config import (
    compressed_files,
    audio_files,
    text_files,
    uploads_url_base
)

logger = logging.getLogger(__name__)

def utterances(utterancesFile):
    """handle POST request for bulk utterances file uploading"""
    try:
        filename = compressed_files.save(utterancesFile)
    except flask_uploads.UploadNotAllowed:
        return error_information(
            status=415,
            title="Invalid file format for bulk utterances upload",
            detail="Invalid file format for bulk utterances upload, must be a compressed file."
                   " Got filename {} , allowed extensions are {}".format(utterancesFile.filename, compressed_files.extensions),
        )
    try:
        # have to read from the full path
        base_zip_path = flask.current_app.config['UPLOADED_COMPRESSED_DEST']
        full_path = os.path.join(base_zip_path, filename)
        zf = ZipFile(full_path, mode='r')
    except NotImplementedError:
        # If Zip compression is not implemented
        return error_information(
            status=400,
            title="Invalid Zip files",
            detail="Invalid zip file provided"
        )
    check_against = [audio_files, text_files] # Allowed upload types
    to_extract = []
    for member in zf.infolist():
        if any(ft.extension_allowed(member.filename) for ft in check_against):
            to_extract.append(member)
        else:
            logger.info("Not allowed filetype in uploaded zip file: %s", member)

    if not to_extract:
        # no files to extract
        return error_information(
            status=400,
            title="Empty zip file provided",
            detail="Empty zip file provided"
        )

    audio_results = []
    transcription_results = []

    for file in to_extract:
        extracted_name = file.filename
        path, extension = os.path.splitext(extracted_name)
        if extension in audio_files.extensions:
            # Got an audio file
            data = zf.open(file).read() # extract data without creating file on disk
            audio_result = create_audio(filepath=Path(extracted_name), data=data)
            audio_results.append(audio_result)
        elif extension in text_files.extensions:
            # Got a text/transcription file
            data = zf.open(file).read() # extract data without creating file on disk
            transcription_result = create_transcription(filepath=Path(extracted_name), data=data)
            transcription_results.append(transcription_result)
    #TODO return proper serialized results
    return {'audios_created': [], 'transcriptions_created': []}, 201
