from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import Usuario

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")  # ou "email"
        senha = request.form.get("senha")

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario:
            if check_password_hash(usuario.senha, senha):

                logout_user()
                session.clear()
                login_user(usuario)
                session.pop('carrinho', None)

                if usuario.perfil == "ADMIN":
                    return redirect('/admin')
                else:
                    return redirect('/loja')

        return "Email ou senha inválidos"
    return render_template('login.html')

@auth.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get("nome")
        email = request.form.get("email").lower().strip()
        senha = request.form.get("senha")
        endereco = request.form.get("endereco")
        cidade = request.form.get("cidade")
        estado = request.form.get("estado")
        cep = request.form.get("cep")

        if Usuario.query.filter_by(email=email).first():
            return render_template('cadastro.html', erro='Email já cadastrado!')

        if senha != request.form.get("confirmar_senha"):
            return render_template("cadastro.html", erro="As senhas não coincidem")

        if not all([nome, email, senha, endereco, cidade, estado, cep]):
            return render_template('cadastro.html', erro='Preencha todos os campos!')

        if len(senha) < 6:
            return render_template('cadastro.html', erro='A senha deve ter pelo menos 6 caracteres')

        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=generate_password_hash(senha),
            perfil='CLIENTE',
            endereco=endereco,
            cidade=cidade,
            estado=estado,
            cep=cep
        )

        db.session.add(novo_usuario)
        db.session.commit()

        return redirect('/login')
    return render_template('cadastro.html')

@auth.route('/logout')
@login_required
def logout():
    session.pop('carrinho', None)
    logout_user()
    return redirect('/login')

@auth.route('/termos')
def termos():
    return render_template('termos.html')