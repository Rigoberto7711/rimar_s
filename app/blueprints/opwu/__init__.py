from flask import Blueprint

opwu_bp = Blueprint('opwu', __name__)

from . import views
