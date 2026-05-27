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


apply_theme(page_title="Turvo Grande | Visao Atual do Negocio", page_icon="🧀")
sidebar_context(
    page_title="Visao Atual do Negocio",
    page_copy=(
        "Leitura rapida da fazenda para entender producao, dinheiro que entra, "
        "dependencia comercial e espaco para valorizar melhor o produto."
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
            "label": "Canal atual",
            "value": commercial["canal"],
            "note": "Hoje toda a saida comercial passa por um unico caminho.",
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
    "Aqui o foco e simples: enxergar o ritmo da producao e o quanto a venda ainda esta concentrada em um unico canal.",
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

chart_row_top = st.columns(2)
with chart_row_top[0]:
    st.plotly_chart(chart_style(cadence_fig), use_container_width=True, config={"displayModeBar": False})
with chart_row_top[1]:
    st.plotly_chart(chart_style(channel_fig), use_container_width=True, config={"displayModeBar": False})
