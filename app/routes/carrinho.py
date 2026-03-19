from flask import Blueprint, session, redirect, request, render_template
from app.models import Produto

carrinho = Blueprint('carrinho', __name__)

@carrinho.route('/carrinho')
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