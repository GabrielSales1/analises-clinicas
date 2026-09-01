from db import db
from datetime import datetime

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(15))
    funcao = db.Column(db.String(30), nullable=False )
    senha = db.Column(db.String(128), nullable=False)
    data_do_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    nivel_acesso = db.Column(db.String(20), default='admin') 
    