"""
API endpoints for /backend
Get information about the backend capabilities supported through this API.
"""
import persephone

# TODO: These label types should be found from querying against the capabilities of the installed Persephone library
# directly. This is a workaround to enable more front end development to proceed.
AVAILABLE_LABEL_TYPES = [
    {
        "id": 1,
        "name": "phonemes",
        "description": "Phoneme labels",
        "explanation": "Labels that correspond to phonemes. Note there can be more than one character per label, "
                       "for example in Na texts, a 'mmm...' (nasal filled pause) and 'əəə...' (oral filled pause) can be used to "
                       "indicate pauses. These units are declared as such, i.e. 'əəə...' is not a sequence of three vowels but one object.",
    },
    {
        "id": 2,
        "name": "phonemes_and_tones",
        "description": "Phonemes labels with additional information about tones.",
        "explanation": "Labels that correspond to phonemes and tones. Tones can be represented by characters such as \"˩\", \"˥\", \"˧\" "
                       "Note there can be more than one character per label, "
                       "for example in Na texts, a 'mmm...' (nasal filled pause) and 'əəə...' (oral filled pause) can be used to "
                       "indicate pauses. These units are declared as such, i.e. 'əəə...' is not a sequence of three vowels but one object.",
    },
]

AVAILABLE_FEATURE_TYPES = [
    {
        "id": 1,
        "name": "fbank",
        "description": "Filterbank features",
        "explanation": "Create features from preprocessing the audio using log Mel filter banks. "
                       "See https://en.wikipedia.org/wiki/Mel_scale for more information about the Mel scale used here."
    }
]

def search():
    """
    Handle a get request for the backend information
    """
    persephone_information = {
        "name": "Persephone",
        "version": persephone.__version__,
        "projectURL": "https://persephone.readthedocs.io/en/latest/",
    }
    return persephone_information, 200

def supported_labels():
    """Return info about supported label types"""
    return AVAILABLE_LABEL_TYPES, 200

def supported_features():
    """Return info about supported features types"""
    return AVAILABLE_FEATURE_TYPES, 200
