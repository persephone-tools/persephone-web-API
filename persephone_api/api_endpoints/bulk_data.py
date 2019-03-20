"""These endpoints exist to handle bulk data uploading functionality.

Make these endpoints be behind an auth wall if possible.
"""
import logging
from pathlib import Path
from zipfile import ZipFile

import flask_uploads

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

import os
output_path = "zip_file_output/"
logger.info("Zip files being extracted to path %s", output_path)

def utterances(utterancesFile):
    """handle POST request for bulk utterances file uploading"""
    if not os.path.isdir(output_path):
        logger.critical("The output path for compressed files %s does not exist", output_path)
        raise RuntimeError("Server configuration issue, contact your administrator")
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
        zf = ZipFile(filename, mode='r')
    except NotImplementedError:
        # If Zip compression is not implemented
        return error_information(
            status=415,
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
            status=415,
            title="Empty zip file provided",
            detail="Empty zip file provided"
        )

    for file in to_extract:
        extracted_name = file.filename
        path, extension = os.path.splitext(extracted_name)
        if extension in audio_files.extensions:
            # Got an audio files
            file_url = uploads_url_base + 'audio_uploads/' + filename
            metadata = FileMetaData(path=file_url, name=filename)
            current_file = Audio(file_info=metadata, url=file_url)
            db.session.add(current_file)
            db.session.commit()
        elif extension in text_files.extensions:
            # Got a text/transcription file
            data = zf.open(file).read() # extract data without creating file on disk
            result = create_transcription(filepath=Path(extracted_name), data=data)
    raise NotImplementedError("Bulk upload not implemented yet")
