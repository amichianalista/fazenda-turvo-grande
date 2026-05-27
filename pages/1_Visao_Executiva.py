from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from app_core.components import (
    apply_theme,
    chart_style,
    hero_panel,
    insight_card,
    metric_card,
    section_header,
    sidebar_context,
    topline,
)
from app_core.data import (
    commercial_metrics,
    formatting_helpers,
    identity_context,
    producer_messages,
    production_metrics,
)


apply_theme(page_title="Turvo Grande | Visão Atual do Negócio", page_icon="🧀")
sidebar_context(
    page_title="Visão Atual do Negócio",
    page_copy=(
        "Leitura rápida da fazenda para entender produção, dinheiro que entra, "
        "dependência comercial e espaço para valorizar melhor o produto."
    ),
)

fmt = formatting_helpers()
identity = identity_context()
production = production_metrics()
commercial = commercial_metrics()
practical_messages = producer_messages()

topline(
    [
        identity["operation_name"],
        identity["location"],
        "Página 1",
        "Leitura para o produtor",
    ]
)

hero_panel(
    kicker="Página 1 | Visão atual do negócio",
    title="O retrato de hoje da Fazenda Turvo Grande",
    copy=(
        "Aqui a ideia é simples: mostrar, de um jeito claro, como a fazenda gira hoje, "
        "quanto ela entrega por mês, por onde o dinheiro entra e onde está o principal "
        "ponto de atenção antes de pensar em crescer."
    ),
    badges=[
        identity["product_name"],
        "Materlândia, Serro (MG)",
        "Venda atual em cooperativa",
    ],
    stats=[
        {
            "label": "Produção por mês",
            "value": fmt["number"](production["queijos_mes"], suffix=" queijos"),
            "note": "Volume já calculado na planilha da fazenda.",
        },
        {
            "label": "Receita bruta atual",
            "value": fmt["currency"](commercial["receita_bruta"]),
            "note": "Entrada bruta mensal no modelo atual de venda.",
        },
        {
            "label": "Canal atual",
            "value": commercial["canal"],
            "note": "Hoje toda a saída comercial passa por um único caminho.",
        },
    ],
    note_title="Leitura bem direta",
    note_copy=(
        "A fazenda já tem produção, ritmo e produto com nome. O que falta agora é "
        "enxergar melhor o espaço de valorização e reduzir a dependência de um canal só."
    ),
)

kpi_cols = st.columns(5)
with kpi_cols[0]:
    metric_card("Queijos por dia", fmt["number"](production["queijos_dia"]), "Saída média diária")
with kpi_cols[1]:
    metric_card("Queijos por semana", fmt["number"](production["queijos_semana"]), "Ritmo semanal da produção")
with kpi_cols[2]:
    metric_card("Kg por mês", fmt["number"](production["kg_mes"], decimals=1, suffix=" kg"), "Escala física mensal")
with kpi_cols[3]:
    metric_card("Preço atual", fmt["currency"](commercial["preco_kg"]), "Recebimento por kg hoje")
with kpi_cols[4]:
    metric_card("Dependência do canal", fmt["percent"](commercial["pct_cooperativa"]), "Parcela vendida para cooperativa")

section_header(
    "Raio-x rápido",
    "Hoje o negócio está assim",
    "Esses cards resumem o que mais importa para quem está no dia a dia da fazenda: rotina, venda e clareza de resultado.",
)

message_cols = st.columns(3)
for column, message in zip(message_cols, practical_messages):
    with column:
        insight_card(message["title"], message["copy"])

section_header(
    "Números que contam a história",
    "Gráficos para bater o olho e entender",
    "Aqui o foco é simples: enxergar o ritmo da produção e o quanto a venda ainda está concentrada em um único canal.",
)

cadence_fig = go.Figure(
    data=[
        go.Bar(
            x=["Dia", "Semana", "Mês"],
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
cadence_fig.update_layout(title="Ritmo da produção", yaxis_title="Quantidade de queijos", showlegend=False)

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
channel_fig.update_layout(title="Por onde a venda passa hoje", showlegend=False)

chart_row_top = st.columns(2)
with chart_row_top[0]:
    st.plotly_chart(chart_style(cadence_fig), use_container_width=True, config={"displayModeBar": False})
with chart_row_top[1]:
    st.plotly_chart(chart_style(channel_fig), use_container_width=True, config={"displayModeBar": False})
