from flask import Flask,render_template, request , redirect, url_for, flash, session
from db import db

from models.Usuario_model import Usuario
from models.Paciente_model import Paciente
from models.Funcionario_model import Funcionario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'clinica_analises_segredo'
db.init_app(app)

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
    if request.method == 'POST': 
        usuario = request.form.get('nome')
        senha = request.form.get('senha')

        user = Usuario.query.filter(
            Usuario.nome == usuario,
            Usuario.senha == senha
        ).first()

        if user:
            session['usuario_id'] = user.id
            session['tipo'] = user.tipo
            session['usuario_nome'] = user.nome
            session['usuario_email'] = user.email
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html", error="Credenciais inválidas")
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard(): 
    return render_template('index.html')

if __name__ == '__main__' : 
    with app.app_context(): 
        db.create_all()
        criar_usuario_padrao
    app.run(debug=True)
