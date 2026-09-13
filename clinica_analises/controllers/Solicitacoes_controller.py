from flask import Flask,render_template, request , redirect, url_for, flash, session
import flask_login
from db import db
from datetime import datetime
from main import app

from models.SolicitacaoExame_model import SolicitacaoExame,ItemSolicitacao
from models.Paciente_model import Paciente
from models.Usuario_model import Usuario
from models.Exame_model import Exame

@app.route('/solicitacao')
@flask_login.login_required
def solicitacao_listar(): 
    solicitacoes  = SolicitacaoExame.query.all()
    return render_template('solicitacoes/listar_solicitacoes.html',user=flask_login.current_user, solicitacoes = solicitacoes )


@app.route('/solicitacao/nova', methods=['GET', 'POST'])
@flask_login.login_required
def solicitacao_nova():
    if request.method == 'POST':
        paciente_id = request.form.get('paciente_id')
        prioridade = request.form.get('prioridade', 'normal')
        data_agendada_str = request.form.get('data_agendada') or None
        hora_agendada_str = request.form.get('hora_agendada') or None
        observacoes = request.form.get('observacoes', '')
        exames_ids = request.form.getlist('exames_ids')

        data_agendada = None
        hora_agendada = None

        if data_agendada_str:
            data_agendada = datetime.strptime(data_agendada_str, '%Y-%m-%d').date()

        if hora_agendada_str:
            hora_agendada = datetime.strptime(hora_agendada_str, '%H:%M').time()
        if not paciente_id or not exames_ids:
            flash('Selecione o paciente e pelo menos um exame.', 'danger')
            return redirect(url_for('solicitacao_nova'))

        solicitacao = SolicitacaoExame(
            paciente_id=paciente_id,
            recepcionista_id=flask_login.current_user.id,
            prioridade=prioridade,
            data_agendada=data_agendada,
            hora_agendada=hora_agendada,
            observacoes=observacoes,
            status='pendente'
        )
        db.session.add(solicitacao)
        db.session.flush()

        total = 0
        for exame_id in exames_ids:
            exame = Exame.query.get(exame_id)
            if exame:
                item = ItemSolicitacao(
                    solicitacao_id=solicitacao.id,
                    exame_id=exame.id,
                    valor=exame.preco or 0,
                    status='pendente'
                )
                db.session.add(item)
                total += float(exame.preco or 0)

        solicitacao.valor_total = total
        db.session.commit()

        flash('Solicitação criada com sucesso!', 'success')
        return redirect(url_for('solicitacao_listar'))

    pacientes = Paciente.query.all()
    exames = Exame.query.filter_by(ativo=True).all()

    return render_template('solicitacoes/nova_solicitacao.html',
                          user=flask_login.current_user,
                          pacientes=pacientes,
                          exames=exames) 

@app.route('/solicitacao/situacao/<int:id>')
@flask_login.login_required
def solicitacao_situacao(id):
    solicitacao = SolicitacaoExame.query.get_or_404(id)
    return render_template('solicitacoes/detalhes_solicitacao.html',user=flask_login.current_user,solicitacao=solicitacao)
#repensei e acredito que editar não seria muito viavel, acredito que pode dar um certo conflito, entt provavelmente o cancelamento é a melhor opção 

@app.route('/solicitacao/cancelar/<int:id>')
@flask_login.login_required
def solicitacao_cancelar(id): 
    db.session.delete(id)
    db.session.commit
    return redirect(url_for('solicitacao_listar'))   


