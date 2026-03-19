from app import create_app, db
from app.models import Usuario, Produto
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    #Usuários
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

    #Produtos
    produto1 = Produto(
        nome='Filtro de Óleo',
        codigo='FT-001',
        categoria='Filtros',
        preco=29.90,
        quantidade=50
    )

    produto2 = Produto(
        nome='Filtro de Ar',
        codigo='FT-002',
        categoria='Filtros',
        preco=20.00,
        quantidade=30
    )

    produto3 = Produto(
        nome='Sistema de Freio',
        codigo='FR-001',
        categoria='Freios',
        preco=180.00,
        quantidade=3
    )

    produto4 = Produto(
        nome='Motor V8',
        codigo='MT-001',
        categoria='Motores',
        preco=3200.00,
        quantidade=1
    )

    produto5 = Produto(
        nome='Chave de fenda',
        codigo='FMT-001',
        categoria='Ferramentas',
        preco=2.00,
        quantidade=0
    )

    if not Usuario.query.filter_by(email='a@a.com').first():
        db.session.add(admin)

    if not Usuario.query.filter_by(email='c@c.com').first():
        db.session.add(cliente)
    if not Produto.query.filter_by(codigo='FT-001').first():
        db.session.add(produto1)

    if not Produto.query.filter_by(codigo='FT-002').first():
        db.session.add(produto2)

    if not Produto.query.filter_by(codigo='FR-001').first():
        db.session.add(produto3)

    if not Produto.query.filter_by(codigo='MT-001').first():
        db.session.add(produto4)

    if not Produto.query.filter_by(codigo='FMT-001').first():
        db.session.add(produto5)

    db.session.commit()
    print('Seed concluído com sucesso!')