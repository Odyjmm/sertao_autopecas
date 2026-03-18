from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user
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

                login_user(usuario)

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
        email = request.form.get("email")
        senha = request.form.get("senha")

        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=generate_password_hash(senha),
            perfil='CLIENTE'
        )

        db.session.add(novo_usuario)
        db.session.commit()

        return redirect('/login')
    return render_template('cadastro.html')