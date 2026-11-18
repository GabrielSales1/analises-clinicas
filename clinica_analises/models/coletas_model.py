from db import db
from datetime import datetime


class Coleta(db.Model):
    __tablename__ = 'coletas'
    
    id = db.Column(db.Integer, primary_key=True)
    solicitacao_id = db.Column(db.Integer, db.ForeignKey('solicitacoes_exames.id'), nullable=False)
    tecnico_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_coleta = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    tipo_material = db.Column(db.String(50), nullable=False)
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), default='realizada', nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    solicitacao = db.relationship("SolicitacaoExame", backref=db.backref("coletas", lazy=True, cascade="all, delete-orphan"))
    tecnico = db.relationship("Usuario", foreign_keys=[tecnico_id])
    
    def __repr__(self):
        return f'<Coleta {self.id} - Material: {self.tipo_material} - Status: {self.status}>'
    
    @property
    def total_itens(self):
        return len(self.itens_coletados)