"""These endpoints exist to handle bulk data uploading functionality.

Make these endpoints be behind an auth wall if possible.
"""

from ..db_models import FileMetaData

from ..upload_config import compressed_files, uploads_url_base


def utterances(utterancesFile):
    """handle POST request for bulk utterances file uploading"""
    raise NotImplementedError("Bulk upload not implemented yet")