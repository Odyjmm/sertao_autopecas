from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user
from werkzeug.security import check_password_hash

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