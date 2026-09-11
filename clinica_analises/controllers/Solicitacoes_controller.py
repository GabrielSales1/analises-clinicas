from flask import Flask,render_template, request , redirect, url_for, flash, session
import flask_login
from db import db
from main import app

from models.SolicitacaoExame_model import SolicitacaoExame,ItemSolicitacao

@app.route('/solicitacao')
@flask_login.login_required
def solicitacao_listar(): 
    solicitacoes  = SolicitacaoExame.query.all()
    return render_template('solicitacoes/listar_solicitacoes.html',user=flask_login.current_user, solicitacoes = solicitacoes )


@app.route('/solicitacao/nova',  methods=['GET', 'POST'])
@flask_login.login_required
def solicitacao_nova(): 

    return "<p>teste</p>"   

@app.route('/solicitacao/situacao/<int:id>')
@flask_login.login_required
def solicitacao_situacao(id): 
    return "<p>teste</p>"  

#repensei e acredito que editar não seria muito viavel, acredito que pode dar um certo conflito, entt provavelmente o cancelamento é a melhor opção 

@app.route('/solicitacao/cancelar/<int:id>')
@flask_login.login_required
def solicitacao_cancelar(id): 
    return "<p>teste</p>"   


