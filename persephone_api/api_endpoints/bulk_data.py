"""These endpoints exist to handle bulk data uploading functionality.

Make these endpoints be behind an auth wall if possible.
"""
import flask_uploads

from ..db_models import FileMetaData
from ..error_response import error_information
from ..upload_config import compressed_files, uploads_url_base

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

    raise NotImplementedError("Bulk upload not implemented yet")