from app import create_app
from app.models import db, User, Agency
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Eliminar la base de datos si ya existe para empezar de cero
    db.drop_all()
    db.create_all()  # Crear todas las tablas definidas en los modelos

    # Crear una agencia
    agency = Agency(name='Default Agency')
    db.session.add(agency)
    db.session.commit()

    # Crear un usuario administrador
    admin = User(username='admin', password='password123', agency_id=agency.id, role='administrador')
    db.session.add(admin)
    db.session.commit()

    print("Usuario administrador creado: admin / password123")
