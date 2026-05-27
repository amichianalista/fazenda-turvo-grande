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
from app_core.data import identity_context, market_context


apply_theme(page_title="Turvo Grande | Mercado e Expansao", page_icon="🧀")
sidebar_context(
    page_title="Mercado e Expansao",
    page_copy="Panorama de mercado, sazonalidade, concorrencia, oportunidades e riscos da expansao premium.",
)

identity = identity_context()
market = market_context()

topline(
    [
        identity["location"],
        "Estudo estrategico | maio de 2026",
        "Leitura de mercado e canal",
    ]
)

hero_panel(
    kicker="Mercado e Expansao",
    title=market["hero_title"],
    copy=market["hero_copy"],
    badges=[
        "IG Serro desde 2011",
        "Premiacao internacional",
        "Canais premium ativos",
    ],
    stats=[
        {
            "label": "Ticket premium",
            "value": "R$ 96-R$ 140",
            "note": "Faixa observada para pecas premium de 700g a 1kg.",
        },
        {
            "label": "Base regional",
            "value": "~800 produtores",
            "note": "O territorio tem densidade produtiva e narrativa forte.",
        },
        {
            "label": "Pico de demanda",
            "value": "Q4",
            "note": "O estudo estima o maior apetite de mercado no fim do ano.",
        },
    ],
    note_title="Valor vem de atributo, nao de desconto",
    note_copy=(
        "A tese premium so faz sentido se a fazenda preservar origem, consistencia e regularizacao. "
        "Competir por preco contra industrial destrava volume, mas destrava o valor errado."
    ),
)

metric_cols = st.columns(4)
for column, highlight in zip(metric_cols, market["highlights"]):
    with column:
        metric_card(highlight["label"], highlight["value"], highlight["note"])

section_header(
    "Mercado",
    "Sazonalidade e pressao competitiva",
    "O estudo mostra janelas mais fortes de demanda e tambem quais grupos realmente disputam o mesmo espaco mental e comercial.",
)

seasonality_fig = go.Figure()
seasonality_fig.add_trace(
    go.Scatter(
        x=[item["quarter"] for item in market["seasonality"]],
        y=[item["index"] for item in market["seasonality"]],
        mode="lines+markers+text",
        line={"color": "#173e2d", "width": 4},
        marker={"size": 10, "color": "#b98433"},
        text=[str(item["index"]) for item in market["seasonality"]],
        textposition="top center",
        name="Indice estimado",
    )
)
seasonality_fig.update_layout(title="Sazonalidade estimada de demanda", yaxis_title="Indice")

competitor_fig = go.Figure(
    data=[
        go.Bar(
            x=[item["score"] for item in market["competitors"]],
            y=[item["name"] for item in market["competitors"]],
            orientation="h",
            marker_color=["#2c6b4b", "#173e2d", "#b98433", "#d8c2a4"],
            text=[item["threat"] for item in market["competitors"]],
            textposition="outside",
        )
    ]
)
competitor_fig.update_layout(
    title="Intensidade competitiva",
    xaxis_title="Score sintetico de ameaca",
    yaxis={"categoryorder": "total ascending"},
    showlegend=False,
)

market_cols = st.columns(2)
with market_cols[0]:
    st.plotly_chart(chart_style(seasonality_fig), use_container_width=True, config={"displayModeBar": False})
with market_cols[1]:
    st.plotly_chart(chart_style(competitor_fig), use_container_width=True, config={"displayModeBar": False})

section_header(
    "Expansao",
    "Frentes com maior potencial de captura de valor",
    "Os scores abaixo sintetizam o estudo em duas dimensoes: potencial de valor e complexidade de execucao.",
)

opportunity_fig = go.Figure()
opportunity_fig.add_trace(
    go.Bar(
        x=[item["title"] for item in market["opportunities"]],
        y=[item["potential_score"] for item in market["opportunities"]],
        name="Potencial",
        marker_color="#173e2d",
    )
)
opportunity_fig.add_trace(
    go.Bar(
        x=[item["title"] for item in market["opportunities"]],
        y=[item["complexity_score"] for item in market["opportunities"]],
        name="Complexidade",
        marker_color="#c9a66b",
    )
)
opportunity_fig.update_layout(
    title="Potencial x complexidade",
    barmode="group",
    yaxis_title="Score sintetico",
)

op_cols = st.columns([1.1, 0.9])
with op_cols[0]:
    st.plotly_chart(chart_style(opportunity_fig), use_container_width=True, config={"displayModeBar": False})
with op_cols[1]:
    list_card(
        title="Como ler o grafico",
        copy="O melhor caminho nao e o maior score bruto, e sim a combinacao entre retorno, risco e capacidade de execucao da fazenda.",
        rows=[
            {"label": item["title"], "value": item["ticket"]} for item in market["opportunities"]
        ],
        callout=market["opportunity_note"],
    )

opportunity_cards_top = st.columns(2)
for column, item in zip(opportunity_cards_top, market["opportunities"][:2]):
    with column:
        info_card(item["title"], item["next_step"], item["detail"])

opportunity_cards_bottom = st.columns(2)
for column, item in zip(opportunity_cards_bottom, market["opportunities"][2:]):
    with column:
        info_card(item["title"], item["next_step"], item["detail"], tone="dark")

section_header(
    "Riscos",
    "O que precisa ser resolvido antes de escalar",
    "A expansao fica mais forte quando a fazenda trata os gargalos estruturais antes de abrir novos canais ou investir em marketing.",
)

risk_cols = st.columns(4)
for column, item in zip(risk_cols, market["risks"]):
    with column:
        metric_card(item["title"], "Atencao", item["copy"])

section_header(
    "Proximos 15 dias",
    "Sequencia pratica sugerida pelo estudo",
    "A agenda abaixo organiza a validacao do negocio antes de qualquer movimento maior de expansao.",
)

plan_cols = st.columns(5)
for column, item in zip(plan_cols, market["action_plan"]):
    with column:
        info_card(item["window"], item["title"], item["copy"])

source_note(
    "Fonte da pagina: Analise estrategica de mercado Turvo Grande, maio de 2026. "
    "Os graficos de concorrencia e de potencial x complexidade sao sinteses analiticas produzidas a partir do estudo."
)
