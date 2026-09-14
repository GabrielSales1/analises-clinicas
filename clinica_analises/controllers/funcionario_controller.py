from flask import Flask,render_template, request , redirect, url_for, flash, session
import flask_login
from db import db
from main import app

from models.Usuario_model import Usuario
from models.Paciente_model import Paciente
from models.Funcionario_model import Funcionario


@app.route('/funcionario/listar')
@flask_login.login_required
def funcionario_listar() : 
    funcionarios = Funcionario.query.all()
    return render_template('paciente/lista_pacientes.html',user=flask_login.current_user,funcionarios = funcionarios)

@app.route('/funcionario/novo')
@flask_login.login_required
def funcionario_novo():
    return "<p>Em breve - Funcionário</p>"