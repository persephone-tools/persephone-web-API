"""
API endpoints for /backend
Get information about the backend capabilities supported through this API.
"""
import persephone

def search():
    """
    Handle a get request for the backend information
    """
    persephone_information = {
        "name": "Persephone",
        "version": persephone.__version__,
    }
    return persephone_information, 200
