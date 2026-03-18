from flask import Blueprint, render_template

loja = Blueprint('loja', __name__)

@loja.route('/loja')
def loja_home():
    return "<h1>Bem vindo à loja!</h1>"