from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from app.models import Produto

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def painel_admin():
    if current_user.perfil != 'ADMIN':
        return redirect('/loja')

    produtos = Produto.query.all()
    return render_template('admin/inventario.html', produtos=produtos)