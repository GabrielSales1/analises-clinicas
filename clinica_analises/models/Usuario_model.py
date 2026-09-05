from db import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    senha = db.Column(db.String(25), nullable =  False)
    tipo = db.Column(db.String(20)) #esse é para definir se é paciente ou funcionario 

    paciente = db.relationship("Paciente", back_populates="usuario", uselist=False, cascade="all, delete-orphan")

    funcionario = db.relationship("Funcionario", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
