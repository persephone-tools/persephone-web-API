"""Unicode normalization for the API.

Helper functions are defined here for the sake of consistency across the entire API

We are normalizing all labels (currently with NFC) to handle the potential duplicates.
Refer to https://unicode.org/reports/tr15/ for details about how this works.
"""

import unicodedata

# The unicode normalization strategy used
NORMALIZATION_TYPE = "NFC"

def normalize(unicode_data):
    """Central point for normalizing all data across the whole API.
    This helper function is used so we can ensure consistency."""
    return unicodedata.normalize(NORMALIZATION_TYPE, unicode_data)
