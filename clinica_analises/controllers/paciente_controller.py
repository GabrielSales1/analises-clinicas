from flask import Flask,render_template, request , redirect, url_for, flash, session
import flask_login
from db import db
from main import app

from models.Exame_model import Exame
from models.Usuario_model import Usuario
from models.Paciente_model import Paciente
from models.Funcionario_model import Funcionario


@app.route('/paciente/paciente_novo')
@flask_login.login_required
def paciente_novo():
    return render_template('paciente_novo.html',user=flask_login.current_user)