from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# import the models *after* the db object is defined
from . import db_models
