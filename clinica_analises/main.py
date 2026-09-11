from flask import Flask,render_template, request , redirect, url_for, flash, session
import flask_login
from db import db

from models.Exame_model import Exame
from models.Usuario_model import Usuario
from models.Paciente_model import Paciente
from models.Funcionario_model import Funcionario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'clinica_analises_segredo'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'loguin'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """Recarrega o usuário a partir do ID armazenado na sessão"""
    return Usuario.query.get(int(user_id))

#função so para criar um usuario padrão de forma funcional antes de uma real criação de usuario 
def criar_usuario_padrao():
    if not Usuario.query.filter_by(email='admin@admin.com').first():
        usuario = Usuario(
            nome='Administrador',
            email='admin@admin.com',
            senha='admin123',
            tipo='admin'
        )
        db.session.add(usuario)
        db.session.commit()
        print('✅ Usuário admin criado: admin@admin.com / admin123')

@app.route('/', methods=["GET", "POST"])
def loguin():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST': 
        usuario = request.form.get('nome')
        senha = request.form.get('senha')

        user = Usuario.query.filter(
            Usuario.nome == usuario,
            Usuario.senha == senha
        ).first()

        if user and user.senha == senha:  
            flask_login.login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            return render_template("login.html", error="Credenciais inválidas")
    
    return render_template('login.html')

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    flash('Você foi desconectado com sucesso.', 'success')
    return redirect(url_for('loguin'))

@app.route('/dashboard')
@flask_login.login_required
def dashboard(): 
    return render_template('index.html',user=flask_login.current_user)


from controllers.Exames_controller import *
from controllers.usuarios_controller import *
from controllers.paciente_controller import *

if __name__ == '__main__' : 
    with app.app_context(): 
        db.create_all()
        criar_usuario_padrao()
    app.run(debug=True)
