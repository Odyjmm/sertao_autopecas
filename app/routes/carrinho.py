from flask import Blueprint, session, redirect, request, render_template, jsonify, flash
from flask_login import login_required
from app.models import Produto

carrinho = Blueprint('carrinho', __name__)

@carrinho.route('/carrinho')
@login_required
def ver_carrinho():
    cart = session.get('carrinho', {})
    itens = []
    total = 0
    alterado = False

    for produto_id in list(cart.keys()):
        quantidade = cart[produto_id]
        produto = Produto.query.get(int(produto_id))

        if not produto or produto.quantidade <= 0:
            del cart[produto_id]
            alterado = True
            continue

        if quantidade > produto.quantidade:
            quantidade = produto.quantidade
            cart[produto_id] = quantidade
            alterado = True

        subtotal = produto.preco * quantidade
        total += subtotal
        itens.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal
        })

    if alterado:
        session['carrinho'] = cart
        session.modified = True
        flash('Alguns itens do seu carrinho foram ajustados por falta de estoque.', 'aviso')

    return render_template(
        'carrinho.html',
        itens=itens,
        total=total
    )

@carrinho.route('/carrinho/adicionar', methods=['POST'])
@login_required
def adicionar_ao_carrinho():
    produto_id = request.form.get('produto_id', type=int)
    quantidade = request.form.get('quantidade', type=int, default=1)

    if not produto_id or not quantidade or quantidade < 1:
        return jsonify({'erro': 'Quantidade inválida.'}), 400

    produto = Produto.query.get_or_404(produto_id)

    cart = session.get('carrinho', {})
    produto_id_str = str(produto.id)
    quantidade_no_carrinho = cart.get(produto_id_str, 0)

    if quantidade_no_carrinho + quantidade > produto.quantidade:
        disponivel = max(produto.quantidade - quantidade_no_carrinho, 0)
        return jsonify({
            'erro': f'Estoque insuficiente para "{produto.nome}". Disponível: {disponivel} unidade(s).'
        }), 400

    cart[produto_id_str] = quantidade_no_carrinho + quantidade
    session['carrinho'] = cart
    session.modified = True

    return jsonify({'ok': True}), 200

@carrinho.route('/carrinho/remover', methods=['POST'])
@login_required
def remover_carrinho():
    produto_id = request.form.get('produto_id', type=int)
    quantidade = request.form.get('quantidade', type=int, default=1)

    if not quantidade or quantidade < 1:
        quantidade = 1

    cart = session.get('carrinho', {})
    produto_id_str = str(produto_id)

    if produto_id_str in cart:
        cart[produto_id_str] -= quantidade
        if cart[produto_id_str] <= 0:
            del cart[produto_id_str]

    session['carrinho'] = cart
    session.modified = True

    return redirect('/carrinho')

@carrinho.route('/carrinho/quantidade')
@login_required
def quantidade_carrinho():
    cart = session.get('carrinho', {})
    total = sum(cart.values())
    return jsonify({'total': total})

@carrinho.route('/carrinho/limpar', methods=['POST'])
@login_required
def limpar_carrinho():
    session.pop('carrinho', None)
    session.modified = True
    return redirect('/carrinho')
