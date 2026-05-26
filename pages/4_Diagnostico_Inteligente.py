from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from app_core.components import apply_theme, insight_card, kpi_card, section_header
from app_core.data import action_priorities, cost_coverage_metrics, diagnosis_cards


apply_theme(
    page_title="Diagnostico Inteligente | Automacao Pecuaria",
    page_icon="🧠",
)

cards = diagnosis_cards()
actions = action_priorities()
coverage = cost_coverage_metrics()

st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-kicker">Pagina 4</div>
        <h1 class="hero-title">Diagnostico inteligente</h1>
        <p class="hero-copy">
            Camada de leitura automatizada para transformar numero em mensagem, prioridade
            e acao sugerida, mas sempre respeitando a profundidade real da base.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(3)
with metric_cols[0]:
    kpi_card("Alertas criticos", str(len(actions[actions["prioridade"] >= 88])), "Itens mais urgentes da coleta")
with metric_cols[1]:
    kpi_card("Oportunidades", str(len(cards)), "Leituras geradas pela base atual")
with metric_cols[2]:
    kpi_card("Cobertura analitica", f"{coverage['percentual_preenchido']:.0f}%", "Custos monetizados na base")

section_header(
    "Mensagens do sistema",
    "O objetivo aqui e soar consultivo e util, sem prometer uma inteligencia que a base ainda nao sustenta.",
)

card_cols = st.columns(2)
for idx, card in enumerate(cards):
    with card_cols[idx % 2]:
        insight_card(card["title"], card["copy"], tone=card["tone"], kicker="Diagnostico")

section_header(
    "Prioridade de acao",
    "O ranking abaixo organiza as proximas coletas para fazer o painel ganhar densidade gerencial rapidamente.",
)

priority_fig = px.bar(
    actions.sort_values("prioridade"),
    x="prioridade",
    y="frente",
    orientation="h",
    color="prioridade",
    color_continuous_scale=["#d5b577", "#1f5c3f"],
)
priority_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    coloraxis_showscale=False,
    margin=dict(l=10, r=10, t=20, b=10),
    xaxis_title="Score de prioridade",
    yaxis_title="Frente",
)

st.plotly_chart(priority_fig, use_container_width=True)

section_header(
    "Leitura pronta para consultoria",
    "Mesmo antes de todos os custos entrarem, a tela ja ajuda a orientar a conversa com o cliente.",
)

st.dataframe(actions.sort_values("prioridade", ascending=False), use_container_width=True, hide_index=True)
