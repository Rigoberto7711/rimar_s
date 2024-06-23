from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .db import db  # Asegúrate de que esto está importando db correctamente

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contab.db'
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'


    with app.app_context():
        from .models import User  # Asegúrate de que User está importado correctamente
        db.create_all()
        
        # Crear un usuario administrador
        admin = User(username='admin', password='password123', agency_id="1", role='administrador')
        db.session.add(admin)
        db.session.commit()
    
    from app.models import User, Agency, Permission
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.models import User
    from app.blueprints.auth import auth_bp
    from app.blueprints.caja import caja_bp
    from app.blueprints.tasas import tasas_bp
    from app.blueprints.opwu import opwu_bp
    from app.blueprints.contabilidad import contabilidad_bp
    from app.blueprints.clientes import clientes_bp
    from app.blueprints.init import init_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(caja_bp, url_prefix='/caja')
    app.register_blueprint(tasas_bp, url_prefix='/tasas')
    app.register_blueprint(opwu_bp, url_prefix='/opwu')
    app.register_blueprint(contabilidad_bp, url_prefix='/contabilidad')
    app.register_blueprint(clientes_bp, url_prefix='/clientes')
    app.register_blueprint(init_bp, url_prefix='/init')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))