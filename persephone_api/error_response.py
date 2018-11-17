"""RCF 7807 error handling"""

from typing import Tuple

def error_information(error_type: str, title: str, status: str, detail: str, instance: str, **kwargs) -> Tuple[dict, int]:
    """Construct an error response in the RFC 8707 format
    see https://tools.ietf.org/html/rfc7807
    """
    error_data = kwargs
    error_data.update({
        "type": error_type,
        "title": title,
        "status": status,
        "detail": detail,
        "instance": instance,
    })
    return error_data, status