from flask import Blueprint

tasas_bp = Blueprint('tasas', __name__)

from . import views
