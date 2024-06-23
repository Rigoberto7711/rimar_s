from flask import Blueprint

caja_bp = Blueprint('caja', __name__)

from . import views

