from db import db

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True)
    data_nascimento = db.Column(db.String(20))
    cpf = db.Column(db.String(14), unique=True)
    convenio = db.Column(db.String(100))
    historico_medico = db.Column(db.String(500))
    alergias = db.Column(db.String(200))
    
    usuario = db.relationship("Usuario", back_populates="paciente")