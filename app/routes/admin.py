from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required, current_user
from app.models import Produto
from app import db

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def painel_admin():
    if current_user.perfil != 'ADMIN':
        return redirect('/loja')

    produtos = Produto.query.all()
    return render_template('admin/inventario.html', produtos=produtos)

@admin.route('/admin/produto/novo', methods=['GET','POST'])
@login_required
def novo_produto():
    if current_user.perfil != 'ADMIN':
        return redirect('/loja')

    if request.method == 'POST':
        nome = request.form.get('nome')
        codigo = request.form.get('codigo')
        categoria = request.form.get('categoria')
        preco = request.form.get('preco', type=float)
        quantidade = request.form.get('quantidade', type=int)

        produto = Produto(
            nome=nome,
            codigo=codigo,
            categoria=categoria,
            preco=preco,
            quantidade=quantidade
        )

        db.session.add(produto)
        db.session.commit()

        return redirect('/admin')
    return render_template('admin/novo_produto.html')

@admin.route('/admin/produto/remover', methods=['POST'])
@login_required
def remover_produto():
    if current_user.perfil != 'ADMIN':
        return redirect('/loja')

    produto_id = request.form.get('produto_id', type=int)
    produto = Produto.query.get_or_404(produto_id)

    if produto.quantidade > 0:
        flash('Não é possível remover um produto com estoque disponível!', 'erro')
        return redirect('/admin')

    db.session.delete(produto)
    db.session.commit()

    return redirect('/admin')