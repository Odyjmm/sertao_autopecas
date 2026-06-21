from flask import Blueprint, render_template, redirect, request, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.models import Produto, Pedido, Devolucao, Usuario, ItemPedido
from app import db
from app.utils import admin_required, extensao_permitida
import os
import uuid

admin = Blueprint('admin', __name__)


def _salvar_imagem(arquivo):
    nome_seguro = secure_filename(arquivo.filename)
    extensao = nome_seguro.rsplit('.', 1)[1].lower() if '.' in nome_seguro else ''
    nome_final = f"{uuid.uuid4().hex}.{extensao}"
    arquivo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], nome_final))
    return nome_final


@admin.route('/admin')
@login_required
@admin_required
def painel_admin():
    produtos = Produto.query.all()
    return render_template('admin/inventario.html', produtos=produtos)

@admin.route('/admin/produto/novo', methods=['GET','POST'])
@login_required
@admin_required
def novo_produto():
    if request.method == 'POST':
        nome = (request.form.get('nome') or '').strip()
        codigo = (request.form.get('codigo') or '').strip()
        categoria = (request.form.get('categoria') or '').strip()
        preco = request.form.get('preco', type=float)
        quantidade = request.form.get('quantidade', type=int)

        if not all([nome, codigo, categoria]) or preco is None or quantidade is None:
            flash('Preencha todos os campos corretamente.', 'erro')
            return render_template('admin/novo_produto.html')

        if preco < 0 or quantidade < 0:
            flash('Preço e quantidade não podem ser negativos.', 'erro')
            return render_template('admin/novo_produto.html')

        if Produto.query.filter_by(codigo=codigo).first():
            flash('Já existe um produto com esse código.', 'erro')
            return render_template('admin/novo_produto.html')

        imagem = request.files.get('imagem')
        nome_arquivo = None

        if imagem and imagem.filename != '':
            if not extensao_permitida(imagem.filename):
                flash('Formato de imagem não permitido. Use JPG, JPEG, PNG, WEBP ou GIF.', 'erro')
                return render_template('admin/novo_produto.html')
            nome_arquivo = _salvar_imagem(imagem)

        produto = Produto(
            nome=nome,
            codigo=codigo,
            categoria=categoria,
            preco=preco,
            quantidade=quantidade,
            imagem=nome_arquivo
        )

        try:
            db.session.add(produto)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Já existe um produto com esse código.', 'erro')
            return render_template('admin/novo_produto.html')

        flash('Produto cadastrado com sucesso!', 'sucesso')
        return redirect('/admin')
    return render_template('admin/novo_produto.html')

@admin.route('/admin/produto/remover', methods=['POST'])
@login_required
@admin_required
def remover_produto():
    produto_id = request.form.get('produto_id', type=int)
    produto = Produto.query.get_or_404(produto_id)

    if produto.quantidade > 0:
        flash('Não é possível remover um produto com estoque disponível!', 'erro')
        return redirect('/admin')

    if ItemPedido.query.filter_by(produto_id=produto.id).first():
        flash('Não é possível remover um produto que já possui pedidos no histórico.', 'erro')
        return redirect('/admin')

    db.session.delete(produto)
    db.session.commit()

    flash('Produto removido com sucesso!', 'sucesso')
    return redirect('/admin')

@admin.route("/admin/produto/editar/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar_produto(id):
    produto = Produto.query.get_or_404(id)

    if request.method == 'POST':
        nome = (request.form.get('nome') or '').strip()
        codigo = (request.form.get('codigo') or '').strip()
        categoria = (request.form.get('categoria') or '').strip()
        preco = request.form.get('preco', type=float)
        quantidade = request.form.get('quantidade', type=int)

        if not all([nome, codigo, categoria]) or preco is None or quantidade is None:
            flash('Preencha todos os campos corretamente.', 'erro')
            return render_template('admin/editar_produto.html', produto=produto)

        if preco < 0 or quantidade < 0:
            flash('Preço e quantidade não podem ser negativos.', 'erro')
            return render_template('admin/editar_produto.html', produto=produto)

        if Produto.query.filter(Produto.codigo == codigo, Produto.id != produto.id).first():
            flash('Já existe outro produto com esse código.', 'erro')
            return render_template('admin/editar_produto.html', produto=produto)

        produto.nome = nome
        produto.codigo = codigo
        produto.categoria = categoria
        produto.preco = preco
        produto.quantidade = quantidade

        imagem = request.files.get('imagem')
        if imagem and imagem.filename != '':
            if not extensao_permitida(imagem.filename):
                flash('Formato de imagem não permitido. Use JPG, JPEG, PNG, WEBP ou GIF.', 'erro')
                return render_template('admin/editar_produto.html', produto=produto)
            produto.imagem = _salvar_imagem(imagem)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Já existe outro produto com esse código.', 'erro')
            return render_template('admin/editar_produto.html', produto=produto)

        flash('Produto atualizado com sucesso!', 'sucesso')
        return redirect("/admin")

    return render_template("admin/editar_produto.html", produto=produto)

@admin.route("/admin/pedidos", methods=["GET"])
@login_required
@admin_required
def listar_pedidos():
    pedidos = Pedido.query.order_by(Pedido.data.desc()).all()
    return render_template('admin/pedidos.html', pedidos=pedidos)


@admin.route('/admin/devolucoes')
@login_required
@admin_required
def listar_devolucoes():
    devolucoes = Devolucao.query.order_by(Devolucao.data.desc()).all()
    return render_template('admin/devolucoes.html', devolucoes=devolucoes)


@admin.route('/admin/devolucoes/<int:id>/<acao>', methods=['POST'])
@login_required
@admin_required
def gerenciar_devolucao(id, acao):
    if acao not in ('aprovar', 'rejeitar'):
        flash('Ação inválida.', 'erro')
        return redirect('/admin/devolucoes')

    devolucao = Devolucao.query.get_or_404(id)

    if devolucao.status != 'PENDENTE':
        flash('Esta devolução já foi avaliada.', 'aviso')
        return redirect('/admin/devolucoes')

    if acao == 'aprovar':
        devolucao.status = 'APROVADA'
        devolucao.pedido.status = 'DEVOLVIDO'

        for item in devolucao.pedido.itens:
            if item.produto:
                item.produto.quantidade += item.quantidade
    elif acao == 'rejeitar':
        devolucao.status = 'RECUSADA'
        devolucao.pedido.status = 'CONFIRMADO'

    db.session.commit()
    flash('Devolução atualizada com sucesso!', 'sucesso')
    return redirect('/admin/devolucoes')


@admin.route('/admin/clientes')
@login_required
@admin_required
def listar_clientes():
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
@admin_required
def pedidos_cliente(id):
    cliente = Usuario.query.get_or_404(id)
    pedidos = Pedido.query.filter_by(usuario_id=id).order_by(Pedido.data.desc()).all()
    return render_template('admin/pedidos_cliente.html', cliente=cliente, pedidos=pedidos)
