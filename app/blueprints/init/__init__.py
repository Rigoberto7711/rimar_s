from flask import Blueprint

init_bp = Blueprint('init', __name__)

from . import views
