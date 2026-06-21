from functools import wraps
from flask import redirect, flash
from flask_login import current_user

EXTENSOES_IMAGEM_PERMITIDAS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}


def admin_required(f):
    """Garante que apenas usuários com perfil ADMIN acessem a rota.
    Deve ser usado junto com @login_required (abaixo dele)."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.perfil != 'ADMIN':
            return redirect('/loja')
        return f(*args, **kwargs)
    return wrapper


def extensao_permitida(filename):
    """Valida a extensão de um arquivo de imagem enviado por upload."""
    if not filename or '.' not in filename:
        return False
    extensao = filename.rsplit('.', 1)[1].lower()
    return extensao in EXTENSOES_IMAGEM_PERMITIDAS
