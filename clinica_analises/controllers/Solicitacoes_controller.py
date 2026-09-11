from flask import Flask,render_template, request , redirect, url_for, flash, session
import flask_login
from db import db
from main import app

@app.route('/solicitacao')
@flask_login.login_required
def solicitacao_listar(): 
    return render_template('<p>teste</p>')

@app.route('/solicitacao/nova',  methods=['GET', 'POST'])
@flask_login.login_required
def solicitacao_nova(): 

    return render_template('<p>teste</p>')

@app.route('/solicitacao/situacao/id')
@flask_login.login_required
def lsolicitacao_situacao(): 
    return render_template('<p>teste</p>')

@app.route('/solicitacao/situacao/id')
@flask_login.login_required
def solicitacao_editar(): 
    return render_template('<p>teste</p>')

@app.route('/solicitacao/cancelar/id')
@flask_login.login_required
def solicitacao_cancelar(): 
    return render_template('<p>teste</p>')

