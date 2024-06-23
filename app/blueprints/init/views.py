from flask import current_app as app
from . import init_bp
from app import db

@init_bp.route('/init_db')
def init_db():
    with app.app_context():
        db.create_all()
    return "Base de datos inicializada."
