from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from app_core.components import (
    apply_theme,
    chart_style,
    hero_panel,
    info_card,
    list_card,
    metric_card,
    section_header,
    sidebar_context,
    source_note,
    topline,
)
from app_core.data import commercial_metrics, formatting_helpers, identity_context, operations_story, production_metrics


apply_theme(page_title="Turvo Grande | Operacao e Producao", page_icon="🧀")
sidebar_context(
    page_title="Operacao e Producao",
    page_copy="Cadencia, escala fisica, formula operacional e dependencias atuais da producao.",
)

fmt = formatting_helpers()
identity = identity_context()
production = production_metrics()
commercial = commercial_metrics()
operations = operations_story()

topline(
    [
        identity["product_name"],
        "Base operacional da fazenda",
        "Leitura derivada da planilha",
    ]
)

hero_panel(
    kicker="Operacao e Producao",
    title="Base produtiva clara, mas ainda sem historico e sem aprofundamento de eficiencia",
    copy=(
        "A fazenda ja informa ritmo, peso medio e resultado mensal. Isso sustenta uma boa leitura inicial de escala, "
        "mas ainda nao responde rendimento, perdas, maturacao e variacao ao longo do tempo."
    ),
    badges=[
        fmt["number"](production["dias_semana"], suffix=" dias/semana"),
        fmt["number"](production["queijos_dia"], suffix=" queijos/dia"),
        fmt["number"](production["peso_medio_kg"], decimals=1, suffix=" kg/peca"),
    ],
    stats=[
        {
            "label": "Dia",
            "value": fmt["number"](production["queijos_dia"], suffix=" queijos"),
            "note": "Saida informada por dia de producao.",
        },
        {
            "label": "Semana",
            "value": fmt["number"](production["queijos_semana"], suffix=" queijos"),
            "note": "Volume semanal consolidado na propria base.",
        },
        {
            "label": "Mes",
            "value": fmt["number"](production["queijos_mes"], suffix=" queijos"),
            "note": "Fechamento mensal derivado da operacao atual.",
        },
    ],
    note_title="O dado ja conta uma historia",
    note_copy=(
        "Mesmo com base enxuta, ja e possivel enxergar uma rotina produtiva estavel. "
        "O proximo salto de maturidade vem com historico, custo e controle de variacao."
    ),
)

metric_cols = st.columns(4)
with metric_cols[0]:
    metric_card("Dias ativos", fmt["number"](production["dias_semana"], suffix=" dias"), "Ritmo semanal da queijaria")
with metric_cols[1]:
    metric_card("Peso medio", fmt["number"](production["peso_medio_kg"], decimals=1, suffix=" kg"), "Padrao medio por peca")
with metric_cols[2]:
    metric_card("Kg por mes", fmt["number"](production["kg_mes"], decimals=1, suffix=" kg"), "Escala fisica consolidada")
with metric_cols[3]:
    metric_card("Receita atual", fmt["currency"](commercial["receita_bruta"]), "Sem leitura de margem ainda")

section_header(
    "Escala",
    "Cadencia da producao e formula operacional",
    "O bloco abaixo combina grafico e formula para mostrar de onde vem o volume mensal da operacao.",
)

cadence_fig = go.Figure(
    data=[
        go.Bar(
            x=[item["label"] for item in operations["cadence"]],
            y=[item["value"] for item in operations["cadence"]],
            marker_color=["#173e2d", "#2c6b4b", "#b98433"],
            text=[f"{int(item['value'])}" for item in operations["cadence"]],
            textposition="outside",
        )
    ]
)
cadence_fig.update_layout(
    title="Escala produtiva",
    yaxis_title="Queijos",
    showlegend=False,
)

scale_cols = st.columns([1.2, 0.8])
with scale_cols[0]:
    st.plotly_chart(chart_style(cadence_fig), use_container_width=True, config={"displayModeBar": False})
with scale_cols[1]:
    list_card(
        title="Formula operacional",
        copy="Leitura sintetica dos fatores que hoje sustentam o resultado mensal.",
        rows=[
            {"label": item["label"], "value": item["value"]} for item in operations["formula_steps"]
        ],
        callout="Sem historico mensal, ainda nao da para medir sazonalidade interna, perdas ou ganho de produtividade.",
    )

section_header(
    "Comercializacao",
    "Canal atual e implicacoes para a operacao",
    "A fazenda tem uma operacao produtiva organizada, mas a captura de valor continua limitada pela concentracao em um unico canal.",
)

share = commercial["pct_cooperativa"] or 0
channel_fig = go.Figure(
    data=[
        go.Pie(
            labels=["Cooperativa", "Outros canais"],
            values=[float(share), max(0.001, 100 - float(share))],
            hole=0.68,
            marker={"colors": ["#173e2d", "#d8c2a4"]},
            textinfo="label+percent",
            sort=False,
        )
    ]
)
channel_fig.update_layout(title="Composicao do canal", showlegend=False)

channel_cols = st.columns([1, 1])
with channel_cols[0]:
    st.plotly_chart(chart_style(channel_fig), use_container_width=True, config={"displayModeBar": False})
with channel_cols[1]:
    list_card(
        title="Leitura operacional",
        copy="O modelo atual simplifica o escoamento, mas tambem posterga aprendizado comercial proprio.",
        rows=[
            {"label": "Preco por kg", "value": fmt["currency"](commercial["preco_kg"])},
            {"label": "Receita bruta mensal", "value": fmt["currency"](commercial["receita_bruta"])},
            {"label": "Participacao da cooperativa", "value": fmt["percent"](commercial["pct_cooperativa"])},
            {"label": "Implicacao", "value": "Baixa complexidade comercial, baixa captura de margem"},
        ],
        callout="Hoje a operacao vende com simplicidade, mas ainda nao testa canal, ticket final ou narrativa de marca no varejo premium.",
    )

section_header(
    "Lacunas",
    "O que a operacao ainda nao mede",
    "Essas ausencias impedem uma leitura mais profunda de eficiencia, rentabilidade e capacidade de evolucao da queijaria.",
)

gap_cols = st.columns(3)
with gap_cols[0]:
    info_card(
        "Controle tecnico",
        "Nao ha leitura de perdas, rendimento ou consistencia por lote.",
        "Sem isso, o app enxerga volume, mas nao enxerga eficiencia de producao.",
    )
with gap_cols[1]:
    info_card(
        "Historico",
        "Ainda nao existe serie mensal para comparar desempenho.",
        "A falta de historico trava leitura de tendencia, sazonalidade interna e capacidade real de crescimento.",
        tone="dark",
    )
with gap_cols[2]:
    info_card(
        "Pos-producao",
        "Nao ha bloco estruturado para estoque, maturacao ou linhas premium.",
        "Hoje a operacao e lida como fluxo direto de producao e venda, sem camada de valor adicional.",
    )

source_note("Fonte da pagina: planilha operacional da fazenda. Todas as leituras desta tela sao diretamente derivadas da base atual.")
