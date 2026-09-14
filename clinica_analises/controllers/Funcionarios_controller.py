from flask import render_template, request, redirect, url_for, flash
import flask_login
import os
from werkzeug.utils import secure_filename
from db import db
from main import app

from models.Usuario_model import Usuario
from models.Funcionario_model import Funcionario
from models.Paciente_model import Paciente


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ============================================
# LISTAR
# ============================================
@app.route('/funcionarios')
@flask_login.login_required
def listar_funcionarios():
    funcionarios = Funcionario.query.all()
    return render_template('funcionarios/listar.html',
                          user=flask_login.current_user,
                          funcionarios=funcionarios)


# ============================================
# NOVO
# ============================================
@app.route('/funcionarios/novo', methods=['GET', 'POST'])
@flask_login.login_required
def novo_funcionario():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '').strip()
        confirmar = request.form.get('confirmar_senha', '').strip()
        tipo = 'funcionario'

        cargo = request.form.get('cargo', '').strip()
        salario = request.form.get('salario', '').strip()
        data_contratacao = request.form.get('data_contratacao', '').strip()
        registro_profissional = request.form.get('registro_profissional', '').strip()

        if not nome or not email or not senha:
            flash('Nome, e-mail e senha são obrigatórios.', 'danger')
            return redirect(url_for('novo_funcionario'))

        if senha != confirmar:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('novo_funcionario'))

        if Usuario.query.filter_by(email=email).first():
            flash('Este e-mail já está cadastrado.', 'warning')
            return redirect(url_for('novo_funcionario'))

        foto_nome = None
        arquivo = request.files.get('foto')

        if arquivo and arquivo.filename:
            if allowed_file(arquivo.filename):
                ext = arquivo.filename.rsplit('.', 1)[1].lower()
                foto_nome = secure_filename(f"user_{email}_{os.urandom(4).hex()}.{ext}")
                caminho = os.path.join(app.config['UPLOAD_FOLDER'], foto_nome)
                arquivo.save(caminho)
            else:
                flash('Formato de imagem inválido.', 'warning')
                return redirect(url_for('novo_funcionario'))

        try:
            novo_usuario = Usuario(
                nome=nome,
                email=email,
                senha=senha,
                tipo=tipo,
                foto=foto_nome
            )
            db.session.add(novo_usuario)
            db.session.flush()

            novo_func = Funcionario(
                usuario_id=novo_usuario.id,
                cargo=cargo,
                salario=salario,
                data_contratacao=data_contratacao,
                registro_profissional=registro_profissional
            )
            db.session.add(novo_func)
            db.session.commit()

            flash('Funcionário cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_funcionarios'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar funcionário: {str(e)}', 'danger')

    return render_template('funcionarios/novo.html', user=flask_login.current_user)


# ============================================
# EDITAR
# ============================================
@app.route('/funcionarios/editar/<int:id>', methods=['GET', 'POST'])
@flask_login.login_required
def editar_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    usuario = funcionario.usuario

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        nova_senha = request.form.get('senha', '').strip()
        confirmar = request.form.get('confirmar_senha', '').strip()

        cargo = request.form.get('cargo', '').strip()
        salario = request.form.get('salario', '').strip()
        data_contratacao = request.form.get('data_contratacao', '').strip()
        registro_profissional = request.form.get('registro_profissional', '').strip()

        if not nome or not email:
            flash('Nome e e-mail são obrigatórios.', 'danger')
            return redirect(url_for('editar_funcionario', id=id))

        email_existente = Usuario.query.filter(
            Usuario.email == email,
            Usuario.id != usuario.id
        ).first()

        if email_existente:
            flash('Este e-mail já está em uso por outro usuário.', 'warning')
            return redirect(url_for('editar_funcionario', id=id))

        if nova_senha and nova_senha != confirmar:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('editar_funcionario', id=id))

        arquivo = request.files.get('foto')

        if arquivo and arquivo.filename:
            if allowed_file(arquivo.filename):
                if usuario.foto:
                    caminho_antigo = os.path.join(app.config['UPLOAD_FOLDER'], usuario.foto)
                    if os.path.exists(caminho_antigo):
                        os.remove(caminho_antigo)

                ext = arquivo.filename.rsplit('.', 1)[1].lower()
                foto_nome = secure_filename(f"user_{email}_{os.urandom(4).hex()}.{ext}")
                caminho = os.path.join(app.config['UPLOAD_FOLDER'], foto_nome)
                arquivo.save(caminho)

                usuario.foto = foto_nome
            else:
                flash('Formato de imagem inválido.', 'warning')
                return redirect(url_for('editar_funcionario', id=id))

        try:
            usuario.nome = nome
            usuario.email = email
            if nova_senha:
                usuario.senha = nova_senha

            funcionario.cargo = cargo
            funcionario.salario = salario
            funcionario.data_contratacao = data_contratacao
            funcionario.registro_profissional = registro_profissional

            db.session.commit()
            flash('Funcionário atualizado com sucesso!', 'success')
            return redirect(url_for('listar_funcionarios'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar funcionário: {str(e)}', 'danger')

    return render_template('funcionarios/editar.html',
                          user=flask_login.current_user,
                          funcionario=funcionario,
                          usuario=usuario)


# ============================================
# DELETAR
# ============================================
@app.route('/funcionarios/deletar/<int:id>', methods=['POST'])
@flask_login.login_required
def deletar_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    usuario = funcionario.usuario

    try:
        db.session.delete(funcionario)
        if usuario:
            db.session.delete(usuario)

        db.session.commit()
        flash('Funcionário removido com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao remover funcionário: {str(e)}', 'danger')

    return redirect(url_for('listar_funcionarios'))