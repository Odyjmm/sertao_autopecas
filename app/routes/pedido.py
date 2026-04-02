from flask import Blueprint, session, redirect, render_template
from flask_login import current_user, login_required
from app.models import Produto, Pedido, ItemPedido
from app import db
import uuid


pedido = Blueprint('pedido', __name__)

@pedido.route('/pedido/finalizar', methods=['POST'])
@login_required
def finalizar_compra():
    cart = session.get('carrinho', {})

    numero = 'P-' + str(uuid.uuid4())[:8].upper()

    novo_pedido = Pedido(
        numero=numero,
        status='CONFIRMADO',
        usuario_id=current_user.id
    )

    db.session.add(novo_pedido)
    db.session.flush()
    total = 0

    for produto_id, quantidade in cart.items():
        produto = Produto.query.get(int(produto_id))

        if not produto:
            continue

        subtotal = produto.preco * quantidade
        total += subtotal

        item = ItemPedido(
            pedido_id=novo_pedido.id,
            produto_id=produto.id,
            quantidade=quantidade,
            preco_unitario=produto.preco
        )

        db.session.add(item)

        produto.quantidade -= quantidade

    db.session.commit()

    session.pop('carrinho', None)

    return redirect(f'/pedido/confirmacao/{numero}')

@pedido.route('/pedido/confirmacao/<numero>')
@login_required
def confirmacao(numero):
    p = Pedido.query.filter_by(numero=numero).first_or_404()
    return render_template('pedido/confirmacao.html', pedido=p, current_user=current_user)

@pedido.route('/meus-pedidos', methods=['GET'])
@login_required
def meus_pedidos():
    pedidos = Pedido.query.filter_by(usuario_id=current_user.id).order_by(Pedido.data.desc()).all()
    return render_template('pedido/meus_pedidos.html', pedidos=pedidos)

@pedido.route('/meus-pedidos/<numero>', methods=['GET'])
@login_required
def detalhe_pedido(numero):
    pedido_especifico = Pedido.query.filter_by(numero=numero).first_or_404()

    itens = ItemPedido.query.filter_by(pedido_id=pedido_especifico.id).all()

    itens_detalhados = []
    for item in itens:
        produto = Produto.query.get(item.produto_id)
        itens_detalhados.append({
            'nome': produto.nome,
            'quantidade': item.quantidade,
            'preco_unitario': item.preco_unitario,
            'subtotal': item.quantidade * item.preco_unitario
        })

    return render_template('pedido/detalhe.html', pedido=pedido_especifico, itens=itens_detalhados)