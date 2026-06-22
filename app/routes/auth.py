from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import Usuario

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = (request.form.get("email") or "").strip().lower()
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

        return render_template('login.html', erro='Email ou senha inválidos!')

    erro = None
    if request.args.get('msg') == 'carrinho':
        erro = 'Por favor, crie uma conta ou faça login para continuar a compra.'

    return render_template('login.html', erro=erro)

@auth.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = (request.form.get("nome") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        senha = request.form.get("senha")
        endereco = (request.form.get("endereco") or "").strip()
        cidade = (request.form.get("cidade") or "").strip()
        estado = (request.form.get("estado") or "").strip().upper()
        cep = (request.form.get("cep") or "").strip()
        termos = request.form.get("termos")

        if not all([nome, email, senha, endereco, cidade, estado, cep]):
            return render_template('cadastro.html', erro='Preencha todos os campos!')

        if not termos:
            return render_template('cadastro.html', erro='Você precisa aceitar os Termos de Uso para se cadastrar.')

        if Usuario.query.filter(Usuario.email.ilike(email)).first():
            return render_template('cadastro.html', erro='Email já cadastrado!')

        if senha != request.form.get("confirmar_senha"):
            return render_template("cadastro.html", erro="As senhas não coincidem")

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

        login_user(novo_usuario)
        session.pop('carrinho', None)

        return redirect('/loja')
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
