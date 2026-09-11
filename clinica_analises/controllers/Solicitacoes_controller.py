from flask import Flask,render_template, request , redirect, url_for, flash, session
import flask_login
from db import db
from main import app

@app.route('/solicitacao')
@flask_login.login_required
def solicitacao_listar(): 
    return render_template('<p>teste</p>')

@app.route('/solicitacao/nova')
@flask_login.login_required
def listar_nova(): 
    return render_template('<p>teste</p>')

@app.route('/solicitacao/situacao/id')
@flask_login.login_required
def listar_situacao(): 
    return render_template('<p>teste</p>')

@app.route('/solicitacao/situacao/id')
@flask_login.login_required
def listar_situacao(): 
    return render_template('<p>teste</p>')

@app.route('/solicitacao/cancelar/id')
@flask_login.login_required
def listar_cancelar(): 
    return render_template('<p>teste</p>')

