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


@app.route('/usuario/listar')
@flask_login.login_required
def usuario_listar():
    usuarios = Usuario.query.all()
    return render_template('usuario/listar_usuarios.html',
                          user=flask_login.current_user,
                          usuarios=usuarios)


@app.route('/usuario/novo', methods=['GET', 'POST'])
@flask_login.login_required
def usuario_novo():
    if request.method == 'POST':
        tipo = request.form['tipo']
        nome = request.form['nome'].strip()
        email = request.form['email'].strip()
        senha = request.form['senha'].strip()

        if Usuario.query.filter_by(email=email).first():
            flash('Já existe um usuário com este email.', 'warning')
            return redirect(url_for('usuario_novo'))

        foto_nome = None
        arquivo = request.files.get('foto')

        if arquivo and arquivo.filename:
            if allowed_file(arquivo.filename):
                ext = arquivo.filename.rsplit('.', 1)[1].lower()
                foto_nome = secure_filename(f"user_{email}_{os.urandom(4).hex()}.{ext}")
                caminho = os.path.join(app.config['UPLOAD_FOLDER'], foto_nome)
                arquivo.save(caminho)
            else:
                flash('Formato de imagem inválido. Use PNG, JPG ou WEBP.', 'warning')
                return redirect(url_for('usuario_novo'))

        usuario = Usuario(
            nome=nome,
            email=email,
            tipo=tipo,
            senha=senha,
            foto=foto_nome
        )

        db.session.add(usuario)
        db.session.commit()

        if tipo == 'funcionario':
            return redirect(url_for('funcionario_novo', usuario_id=usuario.id))
        elif tipo == 'paciente':
            return redirect(url_for('paciente_novo', usuario_id=usuario.id))
        else:
            return redirect(url_for('usuario_listar'))

    return render_template('usuario/usuario_novo.html', user=flask_login.current_user)

