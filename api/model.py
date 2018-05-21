"""
API endpoints for /model
This deals with the API access for model definitions and metadata
"""

from . import db
from .db_models import Model

def search():
    print("Request for all available models")
    return "Get available models not implemented", 501

def post():
    raise NotImplementedError
