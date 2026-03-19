from flask import Blueprint, render_template
from flask_login import current_user
from app.models import Produto

loja = Blueprint('loja', __name__)

@loja.route('/loja')
def loja_home():
    produtos = Produto.query.filter(Produto.quantidade > 0).all()
    return render_template('loja/catalogo.html', produtos=produtos)

@loja.route('/produto/<int:id>')
def produto_detalhe(id):
    produto = Produto.query.get_or_404(id)

    return render_template('loja/produto_detalhe.html', produto=produto, current_user=current_user)