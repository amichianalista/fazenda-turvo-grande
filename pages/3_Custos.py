from __future__ import annotations

import plotly.express as px
import streamlit as st

from app_core.components import apply_theme, empty_state, insight_card, kpi_card, section_header
from app_core.data import cost_breakdown, cost_coverage_metrics, cost_group_chart, cost_items, cost_visibility


apply_theme(
    page_title="Custos | Automacao Pecuaria",
    page_icon="📦",
)

costs = cost_breakdown()
catalog = cost_items()
visibility = cost_visibility()
group_df = cost_group_chart()
coverage = cost_coverage_metrics()

st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-kicker">Pagina 3</div>
        <h1 class="hero-title">Custos</h1>
        <p class="hero-copy">
            Distribuicao dos custos, cobertura da base e visibilidade explicita do que
            ainda falta monetizar para o painel ficar realmente gerencial.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(3)
with metric_cols[0]:
    kpi_card("Categorias de custo", str(coverage["total_categorias"]), "Estrutura ja mapeada")
with metric_cols[1]:
    kpi_card("Custos com valor", str(coverage["categorias_com_valor"]), "Categorias ja monetizadas")
with metric_cols[2]:
    kpi_card("Custos pendentes", str(coverage["categorias_sem_valor"]), "Prioridade de preenchimento")

section_header(
    "Cobertura dos custos",
    "Como a planilha ainda nao traz valores, o foco aqui passa a ser cobertura da base e prontidao para analise.",
)

visibility_fig = px.bar(
    visibility,
    x="status",
    y="valor",
    color="status",
    color_discrete_map={"Conhecidos": "#2d7a54", "Desconhecidos": "#c88d2d"},
)
visibility_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
    margin=dict(l=10, r=10, t=20, b=10),
    yaxis_title="% da base",
    xaxis_title="Status",
)

chart_cols = st.columns([1.15, 1])
with chart_cols[0]:
    group_fig = px.pie(
        group_df,
        names="grupo",
        values="quantidade",
        hole=0.55,
        color="grupo",
        color_discrete_map={"Conhecidos": "#2d7a54", "A descobrir": "#c88d2d"},
    )
    group_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(group_fig, use_container_width=True)
with chart_cols[1]:
    st.plotly_chart(visibility_fig, use_container_width=True)

section_header(
    "Leitura da base de custos",
    "Sem valores preenchidos, a camada inteligente precisa focar em cobertura, e nao em distribuicao financeira.",
)

alert_cols = st.columns(3)
with alert_cols[0]:
    empty_state(
        "Distribuicao financeira indisponivel",
        "O grafico pizza por valor ainda nao pode ser exibido porque nenhuma categoria trouxe numero monetario.",
        tone="earth",
    )
with alert_cols[1]:
    insight_card(
        "Quatro custos ja estao identificados",
        "Sal e coalho, embalagem, mao de obra e frete ja existem como estrutura, faltando apenas os valores.",
        tone="slate",
        kicker="Mapeamento",
    )
with alert_cols[2]:
    insight_card(
        "Cinco frentes seguem a descobrir",
        "Energia, alimentacao, manutencao, sanidade e contrato/cooperativa ainda precisam ganhar numero real.",
        tone="amber",
        kicker="Prioridade",
    )

section_header(
    "Catalogo de custos",
    "Esta tabela deixa claro para a equipe o que ja existe como categoria e o que ainda precisa de valor.",
)

if costs.empty:
    empty_state(
        "Sem custos monetizados",
        "Assim que as categorias receberem valores mensais, esta tela passa a exibir o peso financeiro real de cada uma.",
    )

st.dataframe(
    catalog[["categoria", "grupo", "valor", "status", "observacao"]],
    use_container_width=True,
    hide_index=True,
)
