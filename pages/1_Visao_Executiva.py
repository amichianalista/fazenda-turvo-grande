from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from app_core.components import (
    apply_theme,
    chart_style,
    hero_panel,
    insight_card,
    metric_card,
    note_card,
    section_header,
    sidebar_context,
    source_note,
    topline,
)
from app_core.data import (
    commercial_metrics,
    cost_metrics,
    formatting_helpers,
    identity_context,
    management_readiness,
    missing_costs,
    opportunities,
    producer_messages,
    production_metrics,
    source_registry,
)


apply_theme(page_title="Turvo Grande | Visao Atual do Negocio", page_icon="🧀")
sidebar_context(
    page_title="Visao Atual do Negocio",
    page_copy=(
        "Leitura rapida da fazenda para entender producao, dinheiro que entra, "
        "dependencia comercial e o que ainda falta fechar na gestao."
    ),
)

fmt = formatting_helpers()
identity = identity_context()
production = production_metrics()
commercial = commercial_metrics()
costs = cost_metrics()
readiness = management_readiness()
pending_costs = missing_costs()
practical_messages = producer_messages()
next_moves = opportunities()
sources = source_registry()

topline(
    [
        identity["operation_name"],
        identity["location"],
        "Pagina 1",
        "Leitura para o produtor",
    ]
)

hero_panel(
    kicker="Pagina 1 | Visao atual do negocio",
    title="O retrato de hoje da Fazenda Turvo Grande",
    copy=(
        "Aqui a ideia e simples: mostrar, de um jeito claro, como a fazenda gira hoje, "
        "quanto ela entrega por mes, por onde o dinheiro entra e onde esta o principal "
        "ponto de atencao antes de pensar em crescer."
    ),
    badges=[
        identity["product_name"],
        "Materlandia, Serro (MG)",
        "Venda atual em cooperativa",
    ],
    stats=[
        {
            "label": "Producao por mes",
            "value": fmt["number"](production["queijos_mes"], suffix=" queijos"),
            "note": "Volume ja calculado na planilha da fazenda.",
        },
        {
            "label": "Receita bruta atual",
            "value": fmt["currency"](commercial["receita_bruta"]),
            "note": "Entrada bruta mensal no modelo atual de venda.",
        },
        {
            "label": "Custos fechados",
            "value": f"{readiness['filled_count']}/{costs['total_count']}",
            "note": "Hoje a gestao ainda esta incompleta no lado dos custos.",
        },
    ],
    note_title="Leitura bem direta",
    note_copy=(
        "A fazenda ja tem producao, ritmo e produto com nome. O que falta agora e "
        "enxergar melhor o lucro real e reduzir a dependencia de um canal so."
    ),
)

kpi_cols = st.columns(5)
with kpi_cols[0]:
    metric_card("Queijos por dia", fmt["number"](production["queijos_dia"]), "Saida media diaria")
with kpi_cols[1]:
    metric_card("Queijos por semana", fmt["number"](production["queijos_semana"]), "Ritmo semanal da producao")
with kpi_cols[2]:
    metric_card("Kg por mes", fmt["number"](production["kg_mes"], decimals=1, suffix=" kg"), "Escala fisica mensal")
with kpi_cols[3]:
    metric_card("Preco atual", fmt["currency"](commercial["preco_kg"]), "Recebimento por kg hoje")
with kpi_cols[4]:
    metric_card("Dependencia do canal", fmt["percent"](commercial["pct_cooperativa"]), "Parcela vendida para cooperativa")

section_header(
    "Raio-x rapido",
    "Hoje o negocio esta assim",
    "Esses cards resumem o que mais importa para quem esta no dia a dia da fazenda: rotina, venda e clareza de resultado.",
)

message_cols = st.columns(3)
for column, message in zip(message_cols, practical_messages):
    with column:
        insight_card(message["title"], message["copy"])

section_header(
    "Numeros que contam a historia",
    "Graficos para bater o olho e entender",
    "Os dois primeiros mostram escala e concentracao de venda. Os dois seguintes mostram o quanto da gestao ja esta organizado e quanto ainda falta fechar.",
)

cadence_fig = go.Figure(
    data=[
        go.Bar(
            x=["Dia", "Semana", "Mes"],
            y=[
                production["queijos_dia"] or 0,
                production["queijos_semana"] or 0,
                production["queijos_mes"] or 0,
            ],
            marker_color=["#2d6542", "#47855c", "#c79a47"],
            text=[
                f"{int(production['queijos_dia'] or 0)}",
                f"{int(production['queijos_semana'] or 0)}",
                f"{int(production['queijos_mes'] or 0)}",
            ],
            textposition="outside",
        )
    ]
)
cadence_fig.update_layout(
    title="Ritmo da producao",
    yaxis_title="Quantidade de queijos",
    showlegend=False,
)

cooperativa_share = float(commercial["pct_cooperativa"] or 0)
outros_share = max(0.0, 100.0 - cooperativa_share)
channel_fig = go.Figure(
    data=[
        go.Pie(
            labels=["Cooperativa", "Outros canais"],
            values=[cooperativa_share, outros_share if outros_share > 0 else 0.001],
            hole=0.68,
            marker={"colors": ["#214a2d", "#d9c39d"]},
            textinfo="label+percent",
            sort=False,
        )
    ]
)
channel_fig.update_layout(
    title="Por onde a venda passa hoje",
    showlegend=False,
)

readiness_fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=readiness["readiness_pct"],
        number={"suffix": "%"},
        title={"text": "Prontidao da gestao de custos"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#c79a47"},
            "bgcolor": "#efe4d1",
            "steps": [
                {"range": [0, 35], "color": "#d99a73"},
                {"range": [35, 70], "color": "#d9c39d"},
                {"range": [70, 100], "color": "#7aa16c"},
            ],
        },
    )
)

costs_fig = go.Figure()
costs_fig.add_trace(
    go.Bar(
        y=["Custos conhecidos", "Custos a descobrir"],
        x=[costs["known_count"], costs["discover_count"]],
        orientation="h",
        marker_color=["#2d6542", "#c79a47"],
        text=[str(costs["known_count"]), str(costs["discover_count"])],
        textposition="outside",
    )
)
costs_fig.update_layout(
    title="Mapa de custos ja previsto",
    xaxis_title="Quantidade de linhas de custo",
    showlegend=False,
)

chart_row_top = st.columns(2)
with chart_row_top[0]:
    st.plotly_chart(chart_style(cadence_fig), use_container_width=True, config={"displayModeBar": False})
with chart_row_top[1]:
    st.plotly_chart(chart_style(channel_fig), use_container_width=True, config={"displayModeBar": False})

chart_row_bottom = st.columns(2)
with chart_row_bottom[0]:
    st.plotly_chart(chart_style(readiness_fig), use_container_width=True, config={"displayModeBar": False})
with chart_row_bottom[1]:
    st.plotly_chart(chart_style(costs_fig), use_container_width=True, config={"displayModeBar": False})

section_header(
    "O que ainda falta fechar",
    "Pontos que precisam entrar no caderno",
    "Sem esses valores, a fazenda ate sabe quanto produz e quanto vende, mas ainda nao enxerga com seguranca quanto realmente sobra.",
)

pending_rows = [
    {
        "label": item["category"],
        "value": f"{item['method']} | Status: {item['status']}",
    }
    for item in pending_costs
]

note_cols = st.columns([1.1, 0.9])
with note_cols[0]:
    note_card(
        "Custos sem valor mensal informado",
        "Esses sao os primeiros itens para fechar se a ideia e ter uma visao mais firme do lucro real.",
        rows=pending_rows,
    )
with note_cols[1]:
    note_card(
        "Leitura pratica da situacao",
        readiness["message"],
        rows=[
            {"label": "Linhas com valor", "value": str(readiness["filled_count"])},
            {"label": "Linhas sem valor", "value": str(readiness["pending_count"])},
            {"label": "Mensagem do momento", "value": "Primeiro fechar custo. Depois acelerar."},
        ],
    )

section_header(
    "Proximo passo sem enrolacao",
    "Onde vale mexer primeiro",
    "A ideia aqui nao e complicar a lida. E escolher movimentos simples que deem mais clareza e mais valor para o negocio.",
)

opportunity_cols = st.columns(3)
for column, opportunity in zip(opportunity_cols, next_moves):
    with column:
        insight_card(opportunity["title"], opportunity["copy"])

source_note(
    f"Fontes desta tela: {sources['operational']} e apoio estrategico de {sources['market']}. "
    "Os numeros exibidos como fato atual saem da planilha da fazenda."
)
