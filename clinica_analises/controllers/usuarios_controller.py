from flask import Flask,render_template, request , redirect, url_for, flash, session
import flask_login
from db import db
from main import app

from models.Usuario_model import Usuario
from models.Paciente_model import Paciente
from models.Funcionario_model import Funcionario


#rotas de usuario base ---  de forma que ultiliza como fluxo == usuario + funcionario ou usuario + paciente
@app.route('/usuario/listar')
@flask_login.login_required
def usuario_listar() : 
    usuarios = Usuario.query.all()
    return render_template('usuario/listar_usuarios.html',user=flask_login.current_user,usuarios = usuarios)


@app.route('/usuario/novo', methods=['GET', 'POST'])
@flask_login.login_required
def usuario_novo():
    if request.method == 'POST' : 
        tipo = request.form['tipo']

        usuario = Usuario(
            nome = request.form['nome'], 
            email = request.form['email'],
            tipo = tipo,
            senha = request.form['senha']
        )
        db.session.add(usuario)
        db.session.commit()

        if tipo == 'funcionario':
            return redirect(url_for('funcionario_novo', usuario_id=usuario.id))
        elif tipo == 'paciente':
            return redirect(url_for('paciente_novo', usuario_id=usuario.id))
        else:
            return redirect(url_for('usuario_listar'))
    return render_template('usuario/usuario_novo.html',user=flask_login.current_user)






@app.route('/usuario/editar/<int:id>',methods=['GET', 'POST'])
@flask_login.login_required
def usuario_editar(id) : 
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST' : 
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.tipo = request.form['tipo']
        usuario.senha = request.form['senha']
        db.session.commit()
        return redirect(url_for('usuario_listar')) # temporario ate editar funcionario e paciente estiver funcional 
    return render_template('usuario/usuario_editar.html',user=flask_login.current_user,usuario = usuario)

@app.route('/usuario/excluir/<int:id>')
@flask_login.login_required
def usuario_excluir(id) : 
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuario_listar'))


#não mexer por hora 

@app.route('/funcionario/novo')
@flask_login.login_required
def funcionario_novo():
    return "<p>Em breve - Funcionário</p>"

