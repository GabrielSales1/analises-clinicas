from db import db

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True)
    cargo = db.Column(db.String(50))
    salario = db.Column(db.String(20))
    data_contratacao = db.Column(db.String(20))
    registro_profissional = db.Column(db.String(50))

    usuario = db.relationship("Usuario", back_populates="funcionario")