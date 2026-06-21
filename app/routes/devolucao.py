from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import uuid

from app import db
from app.models import Pedido, Devolucao

devolucao = Blueprint('devolucao', __name__, url_prefix='/devolucao')

MOTIVOS_VALIDOS = ["Produto com defeito", "Produto errado", "Desistência"]

@devolucao.route('/<numero_pedido>', methods=['GET', 'POST'])
@login_required
def solicitar_devolucao(numero_pedido):
    pedido = Pedido.query.filter_by(numero=numero_pedido).first_or_404()

    if pedido.usuario_id != current_user.id:
        flash('Você não tem permissão para acessar este pedido.', 'erro')
        return redirect(url_for('pedido.meus_pedidos'))

    devolucao_ativa = Devolucao.query.filter(
        Devolucao.pedido_id == pedido.id,
        Devolucao.status.in_(['PENDENTE', 'APROVADA'])
    ).first()

    if devolucao_ativa:
        flash(
            f'Já existe uma devolução em andamento para este pedido (protocolo {devolucao_ativa.protocolo}).',
            'aviso'
        )
        return redirect(url_for('pedido.detalhe_pedido', numero=numero_pedido))

    if request.method == 'POST':
        motivo = request.form.get('motivo')

        if motivo not in MOTIVOS_VALIDOS:
            flash('Selecione um motivo válido.', 'erro')
            return render_template('devolucao/formulario.html', pedido=pedido, motivos=MOTIVOS_VALIDOS)

        protocolo = str(uuid.uuid4())[:8].upper()

        nova_devolucao = Devolucao(
            pedido_id=pedido.id,
            motivo=motivo,
            protocolo=protocolo,
            status='PENDENTE'
        )

        db.session.add(nova_devolucao)

        pedido.status = 'DEVOLUÇÃO SOLICITADA'

        db.session.commit()

        flash(f'Devolução registrada com sucesso. Protocolo: {protocolo}', 'sucesso')
        return redirect(url_for('pedido.detalhe_pedido', numero=numero_pedido))

    return render_template('devolucao/formulario.html', pedido=pedido, motivos=MOTIVOS_VALIDOS)
