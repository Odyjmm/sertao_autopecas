from flask import Blueprint, render_template, redirect, request, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from app.models import Produto, Pedido, Devolucao, Usuario
from app import db
import os

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

        imagem = request.files.get('imagem')
        nome_arquivo = None

        if imagem and imagem.filename != '':
            nome_arquivo = secure_filename(imagem.filename)
            imagem.save(os.path.join(current_app.config['UPLOAD_FOLDER'], nome_arquivo))

        produto = Produto(
            nome=nome,
            codigo=codigo,
            categoria=categoria,
            preco=preco,
            quantidade=quantidade,
            imagem = nome_arquivo
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

@admin.route("/admin/produto/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_produto(id):
    if current_user.perfil != 'ADMIN':
        return redirect('/loja')

    produto = Produto.query.get_or_404(id)

    if request.method == 'POST':
        produto.nome = request.form.get("nome")
        produto.codigo = request.form.get("codigo")
        produto.categoria = request.form.get("categoria")
        produto.preco = float(request.form.get("preco"))
        produto.quantidade = int(request.form.get("quantidade"))

        imagem = request.files.get('imagem')
        nome_arquivo = None

        if imagem and imagem.filename != '':
            nome_arquivo = secure_filename(imagem.filename)
            imagem.save(os.path.join(current_app.config['UPLOAD_FOLDER'], nome_arquivo))
            produto.imagem = nome_arquivo

        db.session.commit()
        return redirect("/admin")

    return render_template("admin/editar_produto.html", produto=produto)

@admin.route("/admin/pedidos", methods=["GET"])
@login_required
def listar_pedidos():
    if current_user.perfil != 'ADMIN':
        return redirect('/loja')

    pedidos = Pedido.query.order_by(Pedido.data.desc()).all()

    return render_template('admin/pedidos.html', pedidos=pedidos)


@admin.route('/admin/devolucoes')
@login_required
def listar_devolucoes():
    if current_user.perfil != 'ADMIN':
        return redirect('/loja')

    devolucoes = Devolucao.query.order_by(Devolucao.data.desc()).all()
    return render_template('admin/devolucoes.html', devolucoes=devolucoes)


@admin.route('/admin/devolucoes/<int:id>/<acao>', methods=['POST'])
@login_required
def gerenciar_devolucao(id, acao):
    if current_user.perfil != 'ADMIN':
        return redirect('/loja')

    devolucao = Devolucao.query.get_or_404(id)

    if acao == 'aprovar':
        devolucao.status = 'APROVADA'
        devolucao.pedido.status = 'DEVOLVIDO'

        for item in devolucao.pedido.itens:
            item.produto.quantidade += item.quantidade
    elif acao == 'rejeitar':
        devolucao.status = 'RECUSADA'
        devolucao.pedido.status = 'CONFIRMADO'

    db.session.commit()
    return redirect('/admin/devolucoes')


@admin.route('/admin/clientes')
@login_required
def listar_clientes():
    if current_user.perfil != 'ADMIN':
        return redirect('/loja')

    clientes = Usuario.query.filter_by(perfil='CLIENTE').all()

    for cliente in clientes:
        if cliente.data_cadastro:
            diff = datetime.now() - cliente.data_cadastro

            dias = diff.days
            if dias > 0:
                cliente.tempo_cadastro = f"{dias} dias"
            else:
                horas = diff.seconds // 3600
                cliente.tempo_cadastro = f"{horas} horas"
        else:
            cliente.tempo_cadastro = "N/A"

        cliente.total_pedidos = len(cliente.pedidos)

    return render_template('admin/clientes.html', clientes=clientes)


@admin.route('/admin/clientes/<int:id>/pedidos')
@login_required
def pedidos_cliente(id):
    if current_user.perfil != 'ADMIN':
        return redirect('/loja')

    cliente = Usuario.query.get_or_404(id)
    pedidos = Pedido.query.filter_by(usuario_id=id).order_by(Pedido.data.desc()).all()
    return render_template('admin/pedidos_cliente.html', cliente=cliente, pedidos=pedidos)