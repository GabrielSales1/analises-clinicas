from db import db

#resolvi simplificar a tabela, pelomenos por hora, nas proximas etapas pode haver mudanças 
class Exame(db.Model):
    __tablename__ = 'exames'
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    codigo = db.Column(db.String(20), unique=True)
    descricao = db.Column(db.Text)
    valor_referencia = db.Column(db.String(100))
    unidade_medida = db.Column(db.String(20))
    preco = db.Column(db.Numeric(10, 2))
    tempo_resultado = db.Column(db.String(50))
    preparo_necessario = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Exame {self.nome}>'