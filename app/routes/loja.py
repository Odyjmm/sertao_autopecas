from flask import Blueprint, render_template, request
from flask_login import current_user
from sqlalchemy import or_
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

@loja.route('/busca', methods=['GET'])
def busca():
    termo = request.args.get('q', '')

    if len(termo) < 2:
        produtos = []
    else:
        produtos = Produto.query.filter(
            or_(
                Produto.nome.ilike(f'%{termo}%'),
                Produto.codigo.ilike(f'%{termo}%'),
                Produto.categoria.ilike(f'%{termo}%')
            )
        ).all()

    return render_template('loja/busca.html', produtos=produtos, termo=termo)