from flask import Flask,render_template, request , redirect, url_for, flash, session
import flask_login
from db import db
from main import app

from models.Usuario_model import Usuario
from models.Paciente_model import Paciente
from models.Funcionario_model import Funcionario

@app.route('/paciente/listar')
@flask_login.login_required
def paciente_listar() : 
    pacientes = Paciente.query.all()
    return render_template('paciente/lista_pacientes.html',user=flask_login.current_user,pacientes = pacientes)

@app.route('/paciente/novo', methods=['GET', 'POST'])
@flask_login.login_required
def paciente_novo():
    usuario_id = request.args.get('usuario_id')
    usuario_pre_selecionado = Usuario.query.get(usuario_id) if usuario_id else None

    if request.method == 'POST':
        usuario_id = request.form.get('usuario_id')
        data_nascimento = request.form.get('data_nascimento', '')
        cpf = request.form.get('cpf', '')
        convenio = request.form.get('convenio', '')
        historico_medico = request.form.get('historico_medico', '')
        alergias = request.form.get('alergias', '')

        if not usuario_id or not data_nascimento or not cpf:
            flash('Preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('paciente_novo'))

        if Paciente.query.filter_by(usuario_id=usuario_id).first():
            flash('Este usuário já está cadastrado como paciente.', 'warning')
            return redirect(url_for('paciente_listar'))

        if Paciente.query.filter_by(cpf=cpf).first():
            flash('Já existe um paciente com este CPF.', 'warning')
            return redirect(url_for('paciente_novo'))

        paciente = Paciente(
            usuario_id=usuario_id,
            data_nascimento=data_nascimento,
            cpf=cpf,
            convenio=convenio,
            historico_medico=historico_medico,
            alergias=alergias
        )
        db.session.add(paciente)
        db.session.commit()

        flash('Paciente cadastrado com sucesso!', 'success')
        return redirect(url_for('paciente_listar'))

    usuarios = Usuario.query.filter_by(tipo='paciente').all()
    usuarios_sem_paciente = [u for u in usuarios if not u.paciente]

    return render_template('paciente/paciente_novo.html',
                          user=flask_login.current_user,
                          usuarios=usuarios_sem_paciente,
                          usuario_pre_selecionado=usuario_pre_selecionado)

