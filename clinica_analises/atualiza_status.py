from db import db
from models.SolicitacaoExame_model import ItemSolicitacao
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'
db.init_app(app)

with app.app_context():
    itens = ItemSolicitacao.query.all()
    for item in itens:
        item.status = 'concluido'
    db.session.commit()
    print(f"Atualizado com sucesso! Total de itens: {len(itens)}")
