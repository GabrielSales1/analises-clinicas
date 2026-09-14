# seed.py
from db import db
from main import app
from models.Usuario_model import Usuario
from models.Paciente_model import Paciente
from models.Funcionario_model import Funcionario
from models.Exame_model import Exame
from models.SolicitacaoExame_model import SolicitacaoExame, ItemSolicitacao
from datetime import date, time, datetime


def popular_banco():
    with app.app_context():

        if not Usuario.query.filter_by(email='admin@admin.com').first():
            admin = Usuario(
                nome='Administrador',
                email='admin@admin.com',
                senha='admin123',
                tipo='admin',
                foto='avatar.jpg'
            )
            db.session.add(admin)
            print('✅ Admin criado: admin@admin.com / admin123')

        db.session.commit()

        pacientes_dados = [
            {'nome': 'João Silva', 'email': 'joao@test.com', 'cpf': '111.111.111-11', 'nasc': '15/03/1990', 'convenio': 'Unimed', 'foto': 'avatar-1.jpg'},
            {'nome': 'Maria Santos', 'email': 'maria@test.com', 'cpf': '222.222.222-22', 'nasc': '20/07/1985', 'convenio': 'Bradesco Saúde', 'foto': 'avatar-2.jpg'},
            {'nome': 'Carlos Oliveira', 'email': 'carlos@test.com', 'cpf': '333.333.333-33', 'nasc': '10/11/1978', 'convenio': 'SulAmérica', 'foto': 'avatar-3.jpg'},
            {'nome': 'Ana Lima', 'email': 'ana@test.com', 'cpf': '444.444.444-44', 'nasc': '05/06/1995', 'convenio': 'Amil', 'foto': 'avatar-4.jpg'},
            {'nome': 'Pedro Souza', 'email': 'pedro@test.com', 'cpf': '555.555.555-55', 'nasc': '30/09/2000', 'convenio': 'Particular', 'foto': 'avatar-5.jpg'},
        ]

        for dados in pacientes_dados:
            if Usuario.query.filter_by(email=dados['email']).first():
                continue

            usuario = Usuario(
                nome=dados['nome'],
                email=dados['email'],
                senha='123456',
                tipo='paciente',
                foto=dados['foto']
            )
            db.session.add(usuario)
            db.session.flush()

            paciente = Paciente(
                usuario_id=usuario.id,
                data_nascimento=dados['nasc'],
                cpf=dados['cpf'],
                convenio=dados['convenio']
            )
            db.session.add(paciente)
            print(f'✅ Paciente criado: {dados["nome"]}')

        db.session.commit()

        funcionarios_dados = [
            {'nome': 'Dr. Roberto Almeida', 'email': 'roberto@lab.com', 'tipo': 'analista', 'cargo': 'Biomédico', 'salario': '8500.00', 'data': '01/02/2023', 'registro': 'CRBM-12345', 'foto': 'avatar-6.jpg'},
            {'nome': 'Dra. Fernanda Costa', 'email': 'fernanda@lab.com', 'tipo': 'analista', 'cargo': 'Farmacêutica', 'salario': '9000.00', 'data': '15/03/2023', 'registro': 'CRF-54321', 'foto': 'avatar-7.jpg'},
            {'nome': 'Carlos Técnico', 'email': 'carlos.tecnico@lab.com', 'tipo': 'tecnico', 'cargo': 'Técnico de Coleta', 'salario': '3500.00', 'data': '10/04/2023', 'registro': 'TEC-98765', 'foto': 'avatar-8.jpg'},
            {'nome': 'Juliana Recepção', 'email': 'juliana@lab.com', 'tipo': 'recepcionista', 'cargo': 'Recepcionista', 'salario': '2800.00', 'data': '20/05/2023', 'registro': 'REC-11111', 'foto': 'avatar.jpg'},
        ]

        for dados in funcionarios_dados:
            if Usuario.query.filter_by(email=dados['email']).first():
                continue

            usuario = Usuario(
                nome=dados['nome'],
                email=dados['email'],
                senha='123456',
                tipo=dados['tipo'],
                foto=dados['foto']
            )
            db.session.add(usuario)
            db.session.flush()

            funcionario = Funcionario(
                usuario_id=usuario.id,
                cargo=dados['cargo'],
                salario=dados['salario'],
                data_contratacao=dados['data'],
                registro_profissional=dados['registro']
            )
            db.session.add(funcionario)
            print(f'✅ Funcionário criado: {dados["nome"]} ({dados["cargo"]})')

        db.session.commit()

        exames_dados = [
            {'categoria': 'Hematologia', 'nome': 'Hemograma Completo', 'codigo': 'HEM-001', 'descricao': 'Avalia glóbulos vermelhos, brancos e plaquetas', 'valor_ref': '4.5-5.5 milhões/mm³', 'unidade': 'mg/dL', 'preco': 80.00, 'tempo': '24h', 'preparo': 'Jejum 4h'},
            {'categoria': 'Bioquímica', 'nome': 'Glicemia em Jejum', 'codigo': 'GLI-001', 'descricao': 'Mede a glicose no sangue', 'valor_ref': '70-100 mg/dL', 'unidade': 'mg/dL', 'preco': 30.00, 'tempo': '4h', 'preparo': 'Jejum 8h'},
            {'categoria': 'Bioquímica', 'nome': 'Colesterol Total', 'codigo': 'COL-001', 'descricao': 'Mede o colesterol total', 'valor_ref': '< 190 mg/dL', 'unidade': 'mg/dL', 'preco': 40.00, 'tempo': '6h', 'preparo': 'Jejum 12h'},
            {'categoria': 'Bioquímica', 'nome': 'Triglicerídeos', 'codigo': 'TRI-001', 'descricao': 'Mede triglicerídeos', 'valor_ref': '< 150 mg/dL', 'unidade': 'mg/dL', 'preco': 35.00, 'tempo': '6h', 'preparo': 'Jejum 12h'},
            {'categoria': 'Endocrinologia', 'nome': 'Vitamina D', 'codigo': 'VIT-001', 'descricao': 'Avalia níveis de vitamina D', 'valor_ref': '30-100 ng/mL', 'unidade': 'ng/mL', 'preco': 120.00, 'tempo': '48h', 'preparo': 'Jejum 4h'},
            {'categoria': 'Endocrinologia', 'nome': 'TSH', 'codigo': 'TSH-001', 'descricao': 'Avalia função da tireoide', 'valor_ref': '0.4-4.0 mUI/L', 'unidade': 'mUI/L', 'preco': 85.00, 'tempo': '24h', 'preparo': 'Sem preparo'},
            {'categoria': 'Urinálise', 'nome': 'EAS (Urina Tipo 1)', 'codigo': 'URN-001', 'descricao': 'Exame de urina rotineiro', 'valor_ref': 'Densidade: 1.005-1.030', 'unidade': '-', 'preco': 45.00, 'tempo': '12h', 'preparo': 'Primeira urina'},
            {'categoria': 'Microbiologia', 'nome': 'Urocultura', 'codigo': 'URN-002', 'descricao': 'Identifica bactérias na urina', 'valor_ref': 'Negativo', 'unidade': 'UFC/mL', 'preco': 60.00, 'tempo': '72h', 'preparo': 'Assepsia'},
            {'categoria': 'Imunologia', 'nome': 'PCR (Proteína C Reativa)', 'codigo': 'PCR-001', 'descricao': 'Avalia processos inflamatórios', 'valor_ref': '< 3 mg/L', 'unidade': 'mg/L', 'preco': 35.00, 'tempo': '6h', 'preparo': 'Sem preparo'},
            {'categoria': 'Hematologia', 'nome': 'Coagulograma', 'codigo': 'HEM-002', 'descricao': 'Avalia coagulação sanguínea', 'valor_ref': 'INR: 0.8-1.2', 'unidade': '-', 'preco': 90.00, 'tempo': '24h', 'preparo': 'Jejum 4h'},
        ]

        for dados in exames_dados:
            if Exame.query.filter_by(nome=dados['nome']).first():
                continue

            exame = Exame(
                categoria=dados['categoria'],
                nome=dados['nome'],
                codigo=dados['codigo'],
                descricao=dados['descricao'],
                valor_referencia=dados['valor_ref'],
                unidade_medida=dados['unidade'],
                preco=dados['preco'],
                tempo_resultado=dados['tempo'],
                preparo_necessario=dados['preparo'],
                ativo=True
            )
            db.session.add(exame)
            print(f'✅ Exame criado: {dados["nome"]}')

        db.session.commit()

        if SolicitacaoExame.query.count() > 0:
            print('ℹ️ Já existem solicitações. Pulando.')
        else:
            pacientes = Paciente.query.all()
            exames = Exame.query.all()
            recepcionista = Usuario.query.filter_by(tipo='admin').first()

            if not pacientes or not exames:
                print('❌ Faltam pacientes ou exames para criar solicitações.')
            else:
                solicitacoes_dados = [
                    {'data': date(2025, 3, 15), 'hora': time(12, 10), 'prioridade': 'normal', 'status': 'pendente', 'qtd_exames': 2},
                    {'data': date(2025, 3, 15), 'hora': time(12, 40), 'prioridade': 'urgente', 'status': 'coletado', 'qtd_exames': 1},
                    {'data': date(2025, 3, 16), 'hora': time(9, 0), 'prioridade': 'normal', 'status': 'analisando', 'qtd_exames': 3},
                    {'data': date(2025, 3, 17), 'hora': time(14, 30), 'prioridade': 'baixa', 'status': 'concluido', 'qtd_exames': 2},
                    {'data': date(2025, 3, 18), 'hora': time(10, 15), 'prioridade': 'normal', 'status': 'cancelado', 'qtd_exames': 1},
                    {'data': date(2025, 3, 19), 'hora': time(11, 0), 'prioridade': 'urgente', 'status': 'pendente', 'qtd_exames': 2},
                    {'data': date(2025, 3, 20), 'hora': time(8, 30), 'prioridade': 'normal', 'status': 'pendente', 'qtd_exames': 1},
                ]

                for i, dados in enumerate(solicitacoes_dados):
                    paciente = pacientes[i % len(pacientes)]

                    solicitacao = SolicitacaoExame(
                        paciente_id=paciente.id,
                        recepcionista_id=recepcionista.id,
                        data_agendada=dados['data'],
                        hora_agendada=dados['hora'],
                        prioridade=dados['prioridade'],
                        status=dados['status'],
                        observacoes=''
                    )
                    db.session.add(solicitacao)
                    db.session.flush()

                    total = 0
                    for j in range(dados['qtd_exames']):
                        exame = exames[(i + j) % len(exames)]
                        item = ItemSolicitacao(
                            solicitacao_id=solicitacao.id,
                            exame_id=exame.id,
                            valor=exame.preco or 0,
                            status=dados['status']
                        )
                        db.session.add(item)
                        total += float(exame.preco or 0)

                    solicitacao.valor_total = total
                    print(f'✅ Solicitação #{solicitacao.id} criada para {paciente.usuario.nome}')

                db.session.commit()

        print('\n' + '=' * 50)
        print('🎉 BANCO POPULADO COM SUCESSO!')
        print('=' * 50)
        print(f'👤 Usuários: {Usuario.query.count()}')
        print(f'👥 Pacientes: {Paciente.query.count()}')
        print(f'🧑‍💼 Funcionários: {Funcionario.query.count()}')
        print(f'🧪 Exames: {Exame.query.count()}')
        print(f'📋 Solicitações: {SolicitacaoExame.query.count()}')
        print(f'📝 Itens: {ItemSolicitacao.query.count()}')
        print('=' * 50)
        print('\n🔐 LOGINS PARA TESTE:')
        print('   Admin:       admin@admin.com / admin123')
        print('   Analista:    roberto@lab.com / 123456')
        print('   Técnico:     carlos.tecnico@lab.com / 123456')
        print('   Recepção:    juliana@lab.com / 123456')
        print('   Paciente:    joao@test.com / 123456')


if __name__ == '__main__':
    popular_banco()