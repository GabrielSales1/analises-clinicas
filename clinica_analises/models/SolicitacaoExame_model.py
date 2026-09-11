from db import db
from datetime import datetime


class SolicitacaoExame(db.Model):
    __tablename__ = 'solicitacoes_exames'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    recepcionista_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_agendada = db.Column(db.Date, nullable=True)        # ← Data (ex: 15/03/2025)
    hora_agendada = db.Column(db.Time, nullable=True)        # ← Hora (ex: 12:10)
    data_solicitacao = db.Column(db.DateTime, default=datetime.utcnow)
    prioridade = db.Column(db.String(20), nullable=False, default='baixa')
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pendente')
    valor_total = db.Column(db.Numeric(10, 2), default=0)

    paciente = db.relationship("Paciente", backref="solicitacoes")
    recepcionista = db.relationship("Usuario", foreign_keys=[recepcionista_id])
    itens = db.relationship("ItemSolicitacao", back_populates="solicitacao", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<SolicitacaoExame {self.id}>'

class ItemSolicitacao(db.Model):
    __tablename__ = 'itens_solicitacao'
    
    id = db.Column(db.Integer, primary_key=True)
    solicitacao_id = db.Column(db.Integer, db.ForeignKey('solicitacoes_exames.id'), nullable=False)
    exame_id = db.Column(db.Integer, db.ForeignKey('exames.id'), nullable=False)
    
    status = db.Column(db.String(20), default='pendente')
    valor = db.Column(db.Numeric(10, 2))
    
    solicitacao = db.relationship("SolicitacaoExame", back_populates="itens")
    exame = db.relationship("Exame")