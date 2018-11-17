"""Error response helpers for RFC 7807 error handling"""

from typing import Tuple

def error_information(*, title: str, status: int, detail: str, **kwargs) -> Tuple[dict, int]:
    """Construct an error response in the RFC 8707 format
    see https://tools.ietf.org/html/rfc7807
    """
    error_data = kwargs
    error_data.update({
        "title": title,
        "status": status,
        "detail": detail,
    })
    if "type" not in kwargs:
        error_data["type"] = "about:blank"
    return error_data, status