from app import create_app, db
from app.models import Usuario
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    admin = Usuario(
        nome='Admin',
        email='a@a.com',
        senha=generate_password_hash('123456'),
        perfil='ADMIN'
    )

    cliente = Usuario(
        nome='Cliente',
        email='c@c.com',
        senha=generate_password_hash('123456'),
        perfil='CLIENTE'
    )

    db.session.add(admin)
    db.session.add(cliente)
    db.session.commit()
    print('Usuários criados com sucesso!')