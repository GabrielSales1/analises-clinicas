
from flask import render_template, request, send_file, abort
from db import db
from io import BytesIO
from decimal import Decimal
from main import app
from models.Exame_model import Exame
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)



@app.route('/relatorios/exames', methods=['GET'])
def relatorio_exames():
    # Consulta inicial ao banco
    consulta = Exame.query

    # Filtros enviados pela tela
    busca = request.args.get('busca', '').strip()
    categoria = request.args.get('categoria', '').strip()
    situacao = request.args.get('situacao', 'todos').strip()

    if busca:
        consulta = consulta.filter(
            db_or(
                Exame.nome.ilike(f'%{busca}%'),
                Exame.codigo.ilike(f'%{busca}%'),
                Exame.categoria.ilike(f'%{busca}%')
            )
        )

    if categoria:
        consulta = consulta.filter(
            Exame.categoria == categoria
        )

    if situacao == 'ativos':
        consulta = consulta.filter(Exame.ativo.is_(True))
    elif situacao == 'inativos':
        consulta = consulta.filter(Exame.ativo.is_(False))

    
    # Lista filtrada
    exames = consulta.order_by(Exame.nome.asc()).all()

    # Quantidade de exames por categoria, considerando os filtros
    quantitativo_categorias = (
        db.session.query(
            Exame.categoria,
            db.func.count(Exame.id).label('quantidade')
        )
        .filter(Exame.id.in_([exame.id for exame in exames]))
        .group_by(Exame.categoria)
        .order_by(Exame.categoria.asc())
        .all()
    )

    # Dados preparados para os gráficos
    grafico_categorias = [
        categoria_nome
        for categoria_nome, quantidade in quantitativo_categorias
    ]

    grafico_quantidades = [
        quantidade
        for categoria_nome, quantidade in quantitativo_categorias
    ]

    # Indicadores gerais do catálogo completo
    total_exames = Exame.query.count()

    total_ativos = Exame.query.filter(
        Exame.ativo.is_(True)
    ).count()

    total_inativos = Exame.query.filter(
        Exame.ativo.is_(False)
    ).count()

    # Categorias existentes no banco
    categorias = [
        resultado[0]
        for resultado in
        Exame.query.with_entities(Exame.categoria)
        .distinct()
        .order_by(Exame.categoria.asc())
        .all()
    ]

    return render_template(
        'relatorios/relatorio_exames.html',
        exames=exames,
        categorias=categorias,
        busca=busca,
        categoria_selecionada=categoria,
        situacao=situacao,
        total_exames=total_exames,
        total_ativos=total_ativos,
        total_inativos=total_inativos,
        grafico_categorias=grafico_categorias,
        grafico_quantidades=grafico_quantidades
    )



# Combina os critérios de pesquisa com OR
from sqlalchemy import or_ as db_or

@app.route(
    '/relatorios/exames/pdf/<int:id>',
    methods=['GET'],
    endpoint='imprimir_exame_pdf'
)
def imprimir_exame_pdf(id):
    exame = Exame.query.get_or_404(id)

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title=f'Relatório do exame - {exame.nome}',
        author='Laboratório de Análises Clínicas'
    )

    estilos = getSampleStyleSheet()

    titulo = ParagraphStyle(
        'TituloRelatorio',
        parent=estilos['Title'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#245bb5'),
        spaceAfter=8
    )

    subtitulo = ParagraphStyle(
        'SubtituloRelatorio',
        parent=estilos['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#667085'),
        spaceAfter=18
    )

    texto = ParagraphStyle(
        'TextoRelatorio',
        parent=estilos['Normal'],
        fontSize=10,
        leading=15,
        alignment=TA_LEFT,
        wordWrap='CJK'
    )

    conteudo = [
        Paragraph(
            'LABORATÓRIO DE ANÁLISES CLÍNICAS',
            titulo
        ),
        Paragraph(
            'RELATÓRIO INDIVIDUAL DE EXAME',
            subtitulo
        ),
        Spacer(1, 5 * mm),
    ]

    preco = (
        f'R$ {Decimal(str(exame.preco)):.2f}'.replace('.', ',')
        if exame.preco is not None
        else 'Não informado'
    )

    dados = [
        [
            Paragraph('<b>Identificação</b>', texto),
            Paragraph(str(exame.id), texto)
        ],
        [
            Paragraph('<b>Código</b>', texto),
            Paragraph(exame.codigo or 'Não informado', texto)
        ],
        [
            Paragraph('<b>Nome do exame</b>', texto),
            Paragraph(exame.nome or 'Não informado', texto)
        ],
        [
            Paragraph('<b>Categoria</b>', texto),
            Paragraph(exame.categoria or 'Não informada', texto)
        ],
        [
            Paragraph('<b>Descrição</b>', texto),
            Paragraph(exame.descricao or 'Não informada', texto)
        ],
        [
            Paragraph('<b>Preço</b>', texto),
            Paragraph(preco, texto)
        ],
        [
            Paragraph('<b>Valor de referência</b>', texto),
            Paragraph(
                exame.valor_referencia or 'Não informado',
                texto
            )
        ],
        [
            Paragraph('<b>Unidade de medida</b>', texto),
            Paragraph(
                exame.unidade_medida or 'Não informada',
                texto
            )
        ],
        [
            Paragraph('<b>Tempo para resultado</b>', texto),
            Paragraph(
                exame.tempo_resultado or 'Não informado',
                texto
            )
        ],
        [
            Paragraph('<b>Preparo necessário</b>', texto),
            Paragraph(
                exame.preparo_necessario or 'Não informado',
                texto
            )
        ],
        [
            Paragraph('<b>Situação</b>', texto),
            Paragraph(
                'Ativo' if exame.ativo else 'Inativo',
                texto
            )
        ],
    ]

    tabela = Table(
        dados,
        colWidths=[50 * mm, 110 * mm],
        repeatRows=0,
        hAlign='LEFT'
    )

    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1),
         colors.HexColor('#edf4ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1),
         colors.HexColor('#263238')),
        ('GRID', (0, 0), (-1, -1),
         0.5, colors.HexColor('#d8e0eb')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
    ]))

    conteudo.append(tabela)

    documento.build(conteudo)

    buffer.seek(0)

    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'exame_{exame.id}.pdf'
    )
