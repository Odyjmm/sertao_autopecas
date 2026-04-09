from flask import Blueprint, render_template, request, flash, redirect, jsonify
from flask_login import current_user
from sqlalchemy import or_
from app.models import Produto

loja = Blueprint('loja', __name__)

@loja.route('/loja')
def loja_home():
    produtos = Produto.query.filter(Produto.quantidade > 0).all()
    return render_template('loja/catalogo.html', produtos=produtos, current_user=current_user)

@loja.route('/')
def index():
    produtos = Produto.query.filter(Produto.quantidade > 0).all()
    return render_template('loja/catalogo.html', produtos=produtos, current_user=current_user)

@loja.route('/produto/<int:id>')
def produto_detalhe(id):
    produto = Produto.query.get_or_404(id)

    return render_template('loja/produto_detalhe.html', produto=produto, current_user=current_user)

@loja.route('/busca', methods=['GET'])
def busca():
    termo = request.args.get('q', '').strip()

    if not termo:
        flash('Digite algo para buscar.', 'aviso')
        return redirect('/loja')

    if len(termo) < 3:
        flash('Digite pelo menos 2 caracteres para buscar.', 'aviso')
        return redirect('/loja')

    produtos = Produto.query.filter(
        or_(
            Produto.nome.ilike(f'%{termo}%'),
            Produto.codigo.ilike(f'%{termo}%'),
            Produto.categoria.ilike(f'%{termo}%')
        )
    ).all()

    if not produtos:
        flash(f'Nenhum produto encontrado para "{termo}".', 'aviso')
        return redirect('/loja')

    return render_template('loja/busca.html', produtos=produtos, termo=termo, vazio=False, curto=False)


@loja.route('/busca/sugestoes')
def sugestoes():
    termo = request.args.get('q', '')
    if len(termo) < 2:
        return jsonify([])

    produtos = Produto.query.filter(
        Produto.nome.ilike(f'%{termo}%')
    ).limit(5).all()

    return jsonify([{'id': p.id, 'nome': p.nome} for p in produtos])