"""These endpoints exist to handle bulk data uploading functionality.

Make these endpoints be behind an auth wall if possible.
"""
import logging
from zipfile import ZipFile


import flask_uploads

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
        
    raise NotImplementedError("Bulk upload not implemented yet")