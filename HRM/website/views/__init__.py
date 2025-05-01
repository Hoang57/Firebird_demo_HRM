from flask import Blueprint

auth = Blueprint('view', __name__)

from . import routes
