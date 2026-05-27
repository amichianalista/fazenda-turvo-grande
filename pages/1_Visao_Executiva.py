from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from app_core.components import (
    apply_theme,
    chart_style,
    hero_panel,
    info_card,
    metric_card,
    section_header,
    sidebar_context,
    source_note,
    topline,
)
from app_core.data import (
    commercial_metrics,
    formatting_helpers,
    identity_context,
    market_context,
    operations_story,
    production_metrics,
    source_registry,
)


apply_theme(page_title="Turvo Grande | Visao Executiva", page_icon="🧀")
sidebar_context(
    page_title="Visao Executiva",
    page_copy="Panorama de negocio com operacao atual, posicionamento do produto e prioridades imediatas.",
)

fmt = formatting_helpers()
identity = identity_context()
production = production_metrics()
commercial = commercial_metrics()
operations = operations_story()
market = market_context()
sources = source_registry()

topline(
    [
        identity["operation_name"],
        identity["location"],
        "Planilha operacional + estudo de mercado",
    ]
)

hero_panel(
    kicker="Visao Executiva",
    title=operations["headline"],
    copy=operations["summary"],
    badges=[
        identity["product_name"],
        "IG Serro",
        "Premiacao 2019",
    ],
    stats=[
        {
            "label": "Producao mensal",
            "value": fmt["number"](production["queijos_mes"], suffix=" queijos"),
            "note": "Volume atual consolidado a partir da planilha da fazenda.",
        },
        {
            "label": "Escala fisica",
            "value": fmt["number"](production["kg_mes"], decimals=1, suffix=" kg"),
            "note": "Peso mensal equivalente com base no peso medio informado.",
        },
        {
            "label": "Receita bruta",
            "value": fmt["currency"](commercial["receita_bruta"]),
            "note": "Venda atual concentrada em cooperativa.",
        },
    ],
    note_title="Ativo premium, canal simples",
    note_copy=(
        "O produto ja carrega origem, premiacao e identidade visual forte. "
        "O gargalo hoje esta mais na captura de valor do que na narrativa de marca."
    ),
)

metric_cols = st.columns(4)
with metric_cols[0]:
    metric_card("Operacao", identity["operation_name"], "Leitura atual da fazenda")
with metric_cols[1]:
    metric_card("Produto", identity["product_name"], "Queijo artesanal com origem definida")
with metric_cols[2]:
    metric_card("Preco atual", fmt["currency"](commercial["preco_kg"]), "Recebimento por kg via cooperativa")
with metric_cols[3]:
    metric_card("Canal", commercial["canal"], "Dependencia comercial concentrada")

section_header(
    "Panorama",
    "Leitura executiva da operacao",
    "A pagina agora responde a tres perguntas: qual e a base operacional, qual e o ativo competitivo do produto e o que precisa ser resolvido primeiro para subir de patamar.",
)

panorama_cols = st.columns(3)
with panorama_cols[0]:
    info_card(
        "Canal atual",
        "Toda a venda hoje passa pela cooperativa.",
        "Isso reduz complexidade comercial no curto prazo, mas tambem limita margem, aprendizagem de mercado e construcao de canal proprio.",
    )
with panorama_cols[1]:
    info_card(
        "Ativo de valor",
        "Origem, IG e premiacao puxam o posicionamento para cima.",
        "O diferencial do Turvo Grande nao e volume industrial. E reputacao, territorio e percepcao de autenticidade.",
        tone="dark",
    )
with panorama_cols[2]:
    info_card(
        "Ponto critico",
        "A expansao depende de validacao operacional e familiar.",
        "Antes de discutir escala ou marca, a operacao precisa confirmar capacidade produtiva, governanca e regularizacao.",
    )

section_header(
    "Base atual",
    "Operacao real e concentracao de canal",
    "A leitura abaixo separa o que a fazenda efetivamente produz do modo como a receita esta organizada hoje.",
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
    title="Cadencia operacional",
    yaxis_title="Queijos",
    showlegend=False,
)

share = commercial["pct_cooperativa"] or 0
donut_rest = max(0.0, 100.0 - float(share))
channel_fig = go.Figure(
    data=[
        go.Pie(
            labels=["Cooperativa", "Outros canais"],
            values=[float(share), donut_rest if donut_rest > 0 else 0.001],
            hole=0.68,
            marker={"colors": ["#173e2d", "#d8c2a4"]},
            textinfo="label+percent",
            sort=False,
        )
    ]
)
channel_fig.update_layout(title="Concentracao de canal", showlegend=False)

chart_cols = st.columns(2)
with chart_cols[0]:
    st.plotly_chart(chart_style(cadence_fig), use_container_width=True, config={"displayModeBar": False})
with chart_cols[1]:
    st.plotly_chart(chart_style(channel_fig), use_container_width=True, config={"displayModeBar": False})

section_header(
    "Valorizadores",
    "O que sustenta um posicionamento mais premium",
    "Esses sinais vem do estudo estrategico e ajudam a enquadrar o produto como ativo de valor, nao como commodity regional.",
)

highlight_cols = st.columns(4)
for column, highlight in zip(highlight_cols, market["highlights"]):
    with column:
        metric_card(highlight["label"], highlight["value"], highlight["note"])

section_header(
    "Prioridades",
    "O que deveria acontecer nos proximos 15 dias",
    "O plano abaixo resume a sequencia sugerida pelo estudo: primeiro validar gente e capacidade, depois canal e regularizacao.",
)

plan_cols_top = st.columns(3)
for column, item in zip(plan_cols_top, market["action_plan"][:3]):
    with column:
        info_card(item["window"], item["title"], item["copy"])

plan_cols_bottom = st.columns(2)
for column, item in zip(plan_cols_bottom, market["action_plan"][3:]):
    with column:
        info_card(item["window"], item["title"], item["copy"], tone="dark")

source_note(
    f"Fontes da pagina: {sources['operational']} e {sources['market']}. "
    "Os blocos estrategicos desta tela sao sintetizados a partir do estudo em PDF de maio de 2026."
)
