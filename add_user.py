from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()

    # Crear un usuario administrador
    admin = User(username='admin', password=generate_password_hash('password123', method='sha256'), role='administrador')
    db.session.add(admin)
    db.session.commit()

    print("Usuario administrador creado: admin / password123")
