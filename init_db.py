from app import create_app, db
from app.models import User, Agency

app = create_app()

with app.app_context():
    db.create_all()
    print("Base de datos creada exitosamente.")

if __name__ == '__main__':
    app.run()
