from flask import Flask,render_template, request , redirect, url_for, flash, session
import flask_login
from db import db
from main import app

from models.Exame_model import Exame

@app.route('/tipos_de_exames/listar')
@flask_login.login_required
def listar_exames(): 
    exame = Exame.query.all()
    return render_template('tipos_exames/listas_exames.html',user=flask_login.current_user, exames = exame)

@app.route('/tipos_de_exames/novo_tipo_exame', methods=['GET', 'POST'])
@flask_login.login_required
def novo_tipo_exame(): 
    if request.method == 'POST' : 
        exame = Exame(
            nome=request.form['nome'],
            categoria=request.form['categoria'],
            codigo=request.form.get('codigo', ''),
            descricao=request.form.get('descricao', ''),
            valor_referencia=request.form.get('valor_referencia', ''),
            unidade_medida=request.form.get('unidade_medida', ''),
            preco=request.form.get('preco', 0),
            tempo_resultado=request.form.get('tempo_resultado', ''),
            preparo_necessario=request.form.get('preparo_necessario', ''),
            ativo=True
        )
        db.session.add(exame)
        db.session.commit()
        return redirect(url_for('listar_exames',user=flask_login.current_user))
    return render_template('tipos_exames/novo_tipo_exame.html',user=flask_login.current_user)

@app.route('/tipos_de_exames/detalhes/<int:id>')
@flask_login.login_required
def detalhes_exame(id):
    exame = Exame.query.get_or_404(id) 
    return render_template('tipos_exames/detalhes_exame.html',user=flask_login.current_user, exame = exame )


@app.route('/tipos_de_exames/deletar/<int:id>')
@flask_login.login_required
def deletar_exame(id) :
    exame = Exame.query.get_or_404(id) 
    db.session.delete(exame)
    db.session.commit()
    return redirect(url_for('listar_exames',user=flask_login.current_user))

@app.route('/tipos_de_exames/editar/<int:id>', methods=['GET', 'POST'])
@flask_login.login_required
def editar_exame(id) : 
    exame = Exame.query.get_or_404(id)
    if request.method == 'POST' :
        exame.nome=request.form['nome']
        exame.categoria=request.form['categoria']
        exame.codigo=request.form.get('codigo', '')
        exame.descricao=request.form.get('descricao', '')
        exame.valor_referencia=request.form.get('valor_referencia', '')
        exame.unidade_medida=request.form.get('unidade_medida', '')
        exame.preco=request.form.get('preco', 0)
        exame.tempo_resultado=request.form.get('tempo_resultado', '')
        exame.preparo_necessario=request.form.get('preparo_necessario', '')
        exame.ativo = request.form.get('ativo') == 'on'
        db.session.commit()
        return redirect(url_for('listar_exames'))
    return render_template('tipos_exames/editar_exame.html',user=flask_login.current_user, exame=exame)