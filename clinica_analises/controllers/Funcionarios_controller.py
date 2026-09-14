from flask import render_template, request, redirect, url_for, flash
from db import db
from models.Funcionario_model import Funcionario
from models.Usuario_model import Usuario
import flask_login

from main import app


@app.route('/funcionarios')
@flask_login.login_required
def listar_funcionarios():
    funcionarios = Funcionario.query.all()
    return render_template('funcionarios/listar.html', funcionarios=funcionarios)


@app.route('/funcionarios/novo', methods=['GET', 'POST'])
@flask_login.login_required
def novo_funcionario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = 'funcionario'

        cargo = request.form.get('cargo')
        salario = request.form.get('salario')
        data_contratacao = request.form.get('data_contratacao')
        registro_profissional = request.form.get('registro_profissional')

        if not nome or not email or not senha:
            flash('Nome, e-mail e senha são obrigatórios.', 'danger')
            return redirect(url_for('novo_funcionario'))

        if Usuario.query.filter_by(email=email).first():
            flash('Este e-mail já está cadastrado.', 'warning')
            return redirect(url_for('novo_funcionario'))

        try:
            novo_usuario = Usuario(
                nome=nome,
                email=email,
                senha=senha,
                tipo=tipo
            )
            db.session.add(novo_usuario)
            db.session.flush()  

            novo_funcionario = Funcionario(
                usuario_id=novo_usuario.id,
                cargo=cargo,
                salario=salario,
                data_contratacao=data_contratacao,
                registro_profissional=registro_profissional
            )
            db.session.add(novo_funcionario)
            db.session.commit()

            flash('Funcionário cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_funcionarios'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar funcionário: {str(e)}', 'danger')

    return render_template('funcionarios/novo.html')

@app.route('/funcionarios/editar/<int:id>', methods=['GET', 'POST'])
@flask_login.login_required
def editar_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    usuario = funcionario.usuario

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha') 

        cargo = request.form.get('cargo')
        salario = request.form.get('salario')
        data_contratacao = request.form.get('data_contratacao')
        registro_profissional = request.form.get('registro_profissional')

        if not nome or not email:
            flash('Nome e e-mail são obrigatórios.', 'danger')
            return redirect(url_for('editar_funcionario', id=id))

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente and usuario_existente.id != usuario.id:
            flash('Este e-mail já está em uso por outro usuário.', 'warning')
            return redirect(url_for('editar_funcionario', id=id))

        try:
            usuario.nome = nome
            usuario.email = email
            if senha:  
                usuario.senha = senha

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

    return render_template('funcionarios/editar.html', funcionario=funcionario, usuario=usuario)

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