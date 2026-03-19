from flask import Blueprint, session, redirect, request, render_template
from flask_login import login_required
from app.models import Produto

carrinho = Blueprint('carrinho', __name__)

@carrinho.route('/carrinho')
@login_required
def ver_carrinho():
    cart = session.get('carrinho', {})
    itens = []
    total = 0

    for produto_id, quantidade in cart.items():
        produto = Produto.query.get(int(produto_id))
        if produto:
            subtotal = produto.preco * quantidade
            total += subtotal
            itens.append({
                'produto': produto,
                'quantidade': quantidade,
                'subtotal': subtotal
            })

    return render_template(
        'carrinho.html',
        itens=itens,
        total=total
    )

@carrinho.route('/carrinho/adicionar', methods=['POST'])
@login_required
def adicionar_ao_carrinho():
    produto_id = request.form.get('produto_id', type=int)

    produto = Produto.query.get_or_404(produto_id)

    cart = session.get('carrinho', {})

    produto_id_str = str(produto.id)
    if produto_id_str in cart:
        cart[produto_id_str] += 1
    else:
        cart[produto_id_str] = 1

    session['carrinho'] = cart
    session.modified = True

    return redirect('/loja')

@carrinho.route('/carrinho/remover', methods=['POST'])
@login_required
def remover_carrinho():
    produto_id = request.form.get('produto_id', type=int)

    produto = Produto.query.get_or_404(produto_id)

    cart = session.get('carrinho', {})

    produto_id_str = str(produto.id)
    if produto_id_str in cart:
        del cart[produto_id_str]

    session['carrinho'] = cart
    session.modified = True

    return redirect('/carrinho')