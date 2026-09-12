from flask import Flask, render_template, request, redirect, url_for, flash, session
import flask_login
import os
from werkzeug.utils import secure_filename
from db import db
from main import app

from models.Usuario_model import Usuario
from models.Paciente_model import Paciente
from models.Funcionario_model import Funcionario


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/paciente/listar')
@flask_login.login_required
def paciente_listar():
    pacientes = Paciente.query.all()
    return render_template('paciente/lista_pacientes.html',
                          user=flask_login.current_user,
                          pacientes=pacientes)


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

        usuario = Usuario.query.get(usuario_id)
        arquivo = request.files.get('foto')

        if arquivo and arquivo.filename:
            if allowed_file(arquivo.filename):
                ext = arquivo.filename.rsplit('.', 1)[1].lower()
                foto_nome = secure_filename(f"user_{usuario.email}_{os.urandom(4).hex()}.{ext}")
                caminho = os.path.join(app.config['UPLOAD_FOLDER'], foto_nome)
                arquivo.save(caminho)
                usuario.foto = foto_nome
            else:
                flash('Formato de imagem inválido.', 'warning')
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

@app.route('/paciente/editar/<int:id>', methods=['GET', 'POST'])
@flask_login.login_required
def paciente_editar(id):
    paciente = Paciente.query.get_or_404(id)

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        nova_senha = request.form.get('senha', '').strip()
        confirmar = request.form.get('confirmar_senha', '').strip()

        data_nascimento = request.form.get('data_nascimento', '')
        cpf = request.form.get('cpf', '')
        convenio = request.form.get('convenio', '')
        historico_medico = request.form.get('historico_medico', '')
        alergias = request.form.get('alergias', '')

        if not nome or not email or not data_nascimento or not cpf:
            flash('Preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('paciente_editar', id=id))

        email_existente = Usuario.query.filter(
            Usuario.email == email,
            Usuario.id != paciente.usuario.id
        ).first()

        if email_existente:
            flash('Este email já está em uso.', 'warning')
            return redirect(url_for('paciente_editar', id=id))

        cpf_existente = Paciente.query.filter(
            Paciente.cpf == cpf,
            Paciente.id != id
        ).first()

        if cpf_existente:
            flash('Já existe outro paciente com este CPF.', 'warning')
            return redirect(url_for('paciente_editar', id=id))

        if nova_senha and nova_senha != confirmar:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('paciente_editar', id=id))

        arquivo = request.files.get('foto')

        if arquivo and arquivo.filename:
            if allowed_file(arquivo.filename):
                if paciente.usuario.foto:
                    caminho_antigo = os.path.join(app.config['UPLOAD_FOLDER'], paciente.usuario.foto)
                    if os.path.exists(caminho_antigo):
                        os.remove(caminho_antigo)

                ext = arquivo.filename.rsplit('.', 1)[1].lower()
                foto_nome = secure_filename(f"user_{email}_{os.urandom(4).hex()}.{ext}")
                caminho = os.path.join(app.config['UPLOAD_FOLDER'], foto_nome)
                arquivo.save(caminho)

                paciente.usuario.foto = foto_nome
            else:
                flash('Formato de imagem inválido.', 'warning')
                return redirect(url_for('paciente_editar', id=id))

        paciente.usuario.nome = nome
        paciente.usuario.email = email

        if nova_senha:
            paciente.usuario.senha = nova_senha

        paciente.data_nascimento = data_nascimento
        paciente.cpf = cpf
        paciente.convenio = convenio
        paciente.historico_medico = historico_medico
        paciente.alergias = alergias

        db.session.commit()
        flash('Paciente atualizado com sucesso!', 'success')
        return redirect(url_for('paciente_detalhes', id=paciente.id))

    return render_template('paciente/paciente_editar.html',
                          user=flask_login.current_user,
                          paciente=paciente)


@app.route('/paciente/detalhes/<int:id>')
@flask_login.login_required
def paciente_detalhes(id):
    paciente = Paciente.query.get_or_404(id)
    return render_template('paciente/detalhes_paciente.html',
                          user=flask_login.current_user,
                          paciente=paciente)


@app.route('/paciente/excluir/<int:id>')
@flask_login.login_required
def paciente_excluir(id):
    paciente = Paciente.query.get_or_404(id)
    usuario = paciente.usuario
    nome = usuario.nome if usuario else 'Paciente'

    if usuario and usuario.id == flask_login.current_user.id:
        flash('Você não pode excluir a si mesmo.', 'warning')
        return redirect(url_for('paciente_listar'))

    db.session.delete(paciente)

    if usuario:
        db.session.delete(usuario)

    db.session.commit()
    flash(f'"{nome}" excluído com sucesso.', 'info')
    return redirect(url_for('paciente_listar'))