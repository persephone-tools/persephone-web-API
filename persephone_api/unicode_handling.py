"""Unicode normalization for the API.

Helper functions are defined here for the sake of consistency across the entire API

We are normalizing all labels (currently with NFC) to handle the potential duplicates.
Refer to https://unicode.org/reports/tr15/ for details about how this works.
"""

import unicodedata

def normalize(unicode_data, *, normalization_strategy="NFC"):
    """Central point for normalizing all data across the whole API.
    This helper function is used so we can ensure consistency.

    as a default this will use the "NFC" normalization
    """
    return unicodedata.normalize(normalization_strategy, unicode_data)
