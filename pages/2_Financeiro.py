from __future__ import annotations

import plotly.express as px
import streamlit as st

from app_core.components import apply_theme, empty_state, insight_card, kpi_card, section_header
from app_core.data import financial_availability_chart, financial_metrics, financial_page_status, formatting_helpers


apply_theme(
    page_title="Financeiro | Automacao Pecuaria",
    page_icon="💰",
)

fmt = formatting_helpers()
metrics = financial_metrics()
status_df = financial_page_status()
availability_df = financial_availability_chart()

st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-kicker">Pagina 2</div>
        <h1 class="hero-title">Financeiro</h1>
        <p class="hero-copy">
            Receita, custos, lucro liquido e margem em uma leitura que respeita o
            estagio atual da base, sem inventar numero onde ainda nao existe dado.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(4)
with metric_cols[0]:
    kpi_card("Receita bruta", fmt["currency"](metrics["receita_bruta"]), "Estimativa atual da planilha")
with metric_cols[1]:
    kpi_card("Custos", fmt["currency"](metrics["custos"]), "Dependente do preenchimento dos custos")
with metric_cols[2]:
    kpi_card("Lucro liquido", fmt["currency"](metrics["lucro_liquido"]), "Calculado apenas com custo real")
with metric_cols[3]:
    kpi_card("Margem", fmt["percent"](metrics["margem"]), "Nao fecha enquanto os custos estiverem vazios")

section_header(
    "Leitura financeira",
    "Hoje a pagina ja entrega receita real e mostra com clareza por que o restante ainda nao pode ser calculado.",
)

chart_cols = st.columns([1.7, 1])
with chart_cols[0]:
    receita = metrics["receita_bruta"]
    if receita is None:
        empty_state(
            "Receita ainda indisponivel",
            "Sem a receita preenchida, esta pagina perde sua ancora principal de leitura.",
        )
    else:
        finance_fig = px.bar(
            [{"indicador": "Receita bruta mensal", "valor": receita}],
            x="indicador",
            y="valor",
            color="indicador",
            color_discrete_sequence=["#2d7a54"],
        )
        finance_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(l=10, r=10, t=20, b=10),
            yaxis_title="R$",
            xaxis_title="Indicador",
        )
        st.plotly_chart(finance_fig, use_container_width=True)
with chart_cols[1]:
    availability_fig = px.pie(
        availability_df,
        names="status",
        values="quantidade",
        hole=0.58,
        color="status",
        color_discrete_map={"ok": "#2d7a54", "faltando": "#c88d2d"},
    )
    availability_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=True,
    )
    st.plotly_chart(availability_fig, use_container_width=True)

section_header(
    "Mensagem executiva",
    "A comunicacao aqui precisa manter impacto visual sem esconder que a base financeira ainda esta incompleta.",
)

card_cols = st.columns(2)
with card_cols[0]:
    insight_card(
        "Receita real ja disponivel",
        "A base ja sustenta um numero comercial relevante para apresentar: a receita bruta mensal estimada.",
        tone="green",
        kicker="Resultado",
    )
with card_cols[1]:
    empty_state(
        "Custos, lucro e margem ainda nao fecham",
        "Esses campos continuam bloqueados ate que os custos operacionais saiam do status de preenchimento pendente.",
    )

status_df["valor"] = status_df["valor"].apply(
    lambda value: "Nao mapeado" if value is None else value
)
st.dataframe(status_df, use_container_width=True, hide_index=True)
