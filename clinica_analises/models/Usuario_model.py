from db import db
from flask_login import UserMixin


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(25), nullable=False)
    tipo = db.Column(db.String(20))
    foto = db.Column(db.String(200), nullable=True)

    paciente = db.relationship("Paciente", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    funcionario = db.relationship("Funcionario", back_populates="usuario", uselist=False, cascade="all, delete-orphan")

    def get_foto_url(self):
        if self.foto:
            if self.foto.startswith('user_'):
                return f'/static/uploads/usuarios/{self.foto}'
            return f'/static/img/avatar/{self.foto}'
        return '/static/img/avatar/avatar-fallback.jpg'