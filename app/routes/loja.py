from flask import Blueprint, render_template, request, flash, redirect, jsonify
from flask_login import current_user
from sqlalchemy import or_
from app.models import Produto

loja = Blueprint('loja', __name__)

PRODUTOS_POR_PAGINA = 12

@loja.route('/loja')
def loja_home():
    pagina = request.args.get('pagina', 1, type=int)
    if pagina < 1:
        pagina = 1

    paginacao = Produto.query.filter(Produto.quantidade > 0).order_by(Produto.nome).paginate(
        page=pagina, per_page=PRODUTOS_POR_PAGINA, error_out=False
    )

    return render_template(
        'loja/catalogo.html',
        produtos=paginacao.items,
        paginacao=paginacao,
        current_user=current_user
    )

@loja.route('/produto/<int:id>')
def produto_detalhe(id):
    produto = Produto.query.get_or_404(id)

    return render_template('loja/produto_detalhe.html', produto=produto, current_user=current_user)

@loja.route('/busca', methods=['GET'])
def busca():
    termo = request.args.get('q', '').strip()
    pagina = request.args.get('pagina', 1, type=int)
    if pagina < 1:
        pagina = 1

    if not termo:
        flash('Digite algo para buscar.', 'aviso')
        return redirect('/loja')

    if len(termo) < 3:
        flash('Digite pelo menos 3 caracteres para buscar.', 'aviso')
        return redirect('/loja')

    paginacao = Produto.query.filter(
        or_(
            Produto.nome.ilike(f'%{termo}%'),
            Produto.codigo.ilike(f'%{termo}%'),
            Produto.categoria.ilike(f'%{termo}%')
        )
    ).order_by(Produto.nome).paginate(page=pagina, per_page=PRODUTOS_POR_PAGINA, error_out=False)

    if not paginacao.items:
        flash(f'Nenhum produto encontrado para "{termo}".', 'aviso')
        return redirect('/loja')

    return render_template(
        'loja/busca.html',
        produtos=paginacao.items,
        paginacao=paginacao,
        termo=termo,
        vazio=False,
        curto=False
    )


@loja.route('/busca/sugestoes')
def sugestoes():
    termo = request.args.get('q', '')
    if len(termo) < 2:
        return jsonify([])

    produtos = Produto.query.filter(
        Produto.nome.ilike(f'%{termo}%')
    ).limit(5).all()

    return jsonify([{'id': p.id, 'nome': p.nome} for p in produtos])

@loja.route('/')
def index():
    return redirect('/loja')
