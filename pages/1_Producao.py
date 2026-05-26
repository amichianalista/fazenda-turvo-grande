from __future__ import annotations

import plotly.express as px
import streamlit as st

from app_core.components import apply_theme, empty_state, insight_card, kpi_card, section_header
from app_core.data import formatting_helpers, production_metrics, production_page_status, production_snapshot_chart


apply_theme(
    page_title="Producao | Automacao Pecuaria",
    page_icon="🥛",
)

fmt = formatting_helpers()
metrics = production_metrics()
status_df = production_page_status()
snapshot_df = production_snapshot_chart()

st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-kicker">Pagina 1</div>
        <h1 class="hero-title">Producao</h1>
        <p class="hero-copy">
            Visao executiva da operacao produtiva conectada a base real, separando claramente
            o que ja foi medido do que ainda precisa ser coletado.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(4)
with metric_cols[0]:
    kpi_card("Queijos por dia", fmt["number"](metrics["queijos_dia"], suffix=" un."), "Base atual da planilha")
with metric_cols[1]:
    kpi_card("Kg por mes", fmt["number"](metrics["kg_mes"], decimals=1, suffix=" kg"), "Volume mensal calculado")
with metric_cols[2]:
    kpi_card("Evolucao", fmt["percent"](metrics["evolucao_pct"]), "Serie historica ainda ausente")
with metric_cols[3]:
    kpi_card("Capacidade produtiva", fmt["percent"](metrics["capacidade_produtiva"]), "Meta/capacidade nao mapeada")

section_header(
    "Fotografia atual da producao",
    "Como ainda nao existe historico, a melhor leitura hoje e um snapshot operacional honesto e bem apresentado.",
)

chart_cols = st.columns([1.7, 1])
with chart_cols[0]:
    if snapshot_df.empty:
        empty_state(
            "Sem volume disponivel",
            "A base ainda nao traz indicadores suficientes para desenhar a fotografia da producao.",
        )
    else:
        snapshot_fig = px.bar(
            snapshot_df,
            x="indicador",
            y="valor",
            color="indicador",
            color_discrete_sequence=["#1f5c3f", "#2d7a54", "#c88d2d"],
        )
        snapshot_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(l=10, r=10, t=20, b=10),
            yaxis_title="Quantidade",
            xaxis_title="Indicador",
        )
        st.plotly_chart(snapshot_fig, use_container_width=True)
with chart_cols[1]:
    insight_card(
        "Peso medio por queijo",
        (
            f"{fmt['number'](metrics['peso_medio_kg'], decimals=1, suffix=' kg')} por unidade. "
            f"O volume vendido para a cooperativa esta em {fmt['number'](metrics['pct_cooperativa'], suffix='%')}."
        ),
        tone="green",
        kicker="Leitura atual",
    )

section_header(
    "Leituras de apoio",
    "Aqui a pagina ja mistura indicador real com transparencia sobre as lacunas da operacao.",
)

note_cols = st.columns(2)
with note_cols[0]:
    insight_card(
        "Snapshot produtivo pronto",
        "Ja conseguimos mostrar producao diaria, semanal, mensal e peso medio por queijo com base real.",
        tone="green",
        kicker="Leitura",
    )
with note_cols[1]:
    empty_state(
        "Historico e capacidade ainda faltando",
        "Para transformar esta tela em painel executivo completo, precisamos de serie historica e capacidade instalada.",
    )

status_df["valor"] = status_df["valor"].apply(
    lambda value: "Nao mapeado" if value is None else value
)
st.dataframe(status_df, use_container_width=True, hide_index=True)
