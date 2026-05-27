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
from app_core.data import cost_metrics, cost_readiness, cost_summary, discover_costs, known_costs


def render_cost_cards(items: list[dict[str, object]]) -> None:
    for index in range(0, len(items), 2):
        row = st.columns(2)
        for offset, item in enumerate(items[index : index + 2]):
            with row[offset]:
                list_card(
                    title=str(item["category"]),
                    copy=f"Status atual: {item['status_text']}",
                    rows=[
                        {"label": "Valor atual", "value": str(item["value_text"])},
                        {"label": "Como levantar", "value": str(item["method_text"])},
                        {"label": "Grupo", "value": "Custos conhecidos" if item["group"] == "known" else "Custos a descobrir"},
                    ],
                    callout=str(item["note_text"]) if item["note_text"] else None,
                )


apply_theme(page_title="Turvo Grande | Custos e Prontidao", page_icon="🧀")
sidebar_context(
    page_title="Custos e Prontidao",
    page_copy="Maturidade da base de custos, status de preenchimento e proximos levantamentos necessarios.",
)

metrics = cost_metrics()
summary = cost_summary()
readiness = cost_readiness()
known = known_costs()
discover = discover_costs()

topline(
    [
        "Base de custos da planilha",
        "Leitura de prontidao",
        "Sem DRE confiavel ainda",
    ]
)

hero_panel(
    kicker="Custos e Prontidao",
    title="A estrutura de custos existe, mas a base ainda nao fecha margem nem lucro com seguranca",
    copy=(
        "A pagina deixa de fingir um resultado financeiro que nao existe. "
        "O foco aqui e mostrar nivel de maturidade, lacunas de preenchimento e a ordem correta de levantamento."
    ),
    badges=[
        f"{metrics['known_count']} custos conhecidos",
        f"{metrics['discover_count']} a descobrir",
        f"{metrics['filled_count']} com valor",
    ],
    stats=[
        {
            "label": "Custos listados",
            "value": str(metrics["total_count"]),
            "note": "Categorias que ja aparecem estruturadas na planilha.",
        },
        {
            "label": "Prontos com valor",
            "value": str(metrics["filled_count"]),
            "note": "Itens que realmente podem entrar em conta hoje.",
        },
        {
            "label": "Resultado atual",
            "value": summary["current_total_text"],
            "note": "Total ainda zerado por falta de preenchimento consistente.",
        },
    ],
    note_title="Prontidao antes de lucro",
    note_copy=(
        "Sem energia, alimentacao, manutencao, veterinario e taxa da cooperativa, qualquer margem mostrada seria mais efeito visual do que verdade financeira."
    ),
    image_path=None,
)

metric_cols = st.columns(4)
with metric_cols[0]:
    metric_card("Conhecidos", str(metrics["known_count"]), "Custos ja nomeados")
with metric_cols[1]:
    metric_card("Com valor", str(metrics["filled_count"]), "Podem entrar em conta")
with metric_cols[2]:
    metric_card("Sem valor", str(metrics["pending_count"]), "Ainda dependem de coleta")
with metric_cols[3]:
    metric_card("A descobrir", str(metrics["discover_count"]), "Dependem de apuracao")

section_header(
    "Prontidao",
    "Nivel atual de maturidade da base",
    "Os dois graficos abaixo deixam claro que a discussao financeira ainda e sobre preenchimento e organizacao, nao sobre margem final.",
)

status_fig = go.Figure(
    data=[
        go.Pie(
            labels=[item["label"] for item in readiness["status_split"]],
            values=[item["value"] for item in readiness["status_split"]],
            hole=0.68,
            marker={"colors": ["#173e2d", "#d8c2a4"]},
            textinfo="label+value",
        )
    ]
)
status_fig.update_layout(title="Preenchimento da base", showlegend=False)

group_fig = go.Figure(
    data=[
        go.Bar(
            x=[item["label"] for item in readiness["group_split"]],
            y=[item["value"] for item in readiness["group_split"]],
            marker_color=["#173e2d", "#b98433"],
            text=[str(item["value"]) for item in readiness["group_split"]],
            textposition="outside",
        )
    ]
)
group_fig.update_layout(title="Estrutura de custos", yaxis_title="Categorias", showlegend=False)

readiness_cols = st.columns(2)
with readiness_cols[0]:
    st.plotly_chart(chart_style(status_fig), use_container_width=True, config={"displayModeBar": False})
with readiness_cols[1]:
    st.plotly_chart(chart_style(group_fig), use_container_width=True, config={"displayModeBar": False})

section_header(
    "Custos conhecidos",
    "O que ja esta estruturado para preenchimento",
    "Esses itens ja aparecem bem definidos na planilha. O trabalho agora e converter estrutura em valor mensal confiavel.",
)

render_cost_cards(known)

section_header(
    "Custos a descobrir",
    "O que ainda precisa de levantamento real",
    "Esses itens travam a leitura de custo total e precisam ser apurados antes de qualquer decisao sobre margem ou expansao.",
)

render_cost_cards(discover)

section_header(
    "Proxima coleta",
    "O que falta para essa pagina virar resultado financeiro real",
    "Com a sequencia correta de coleta, esta tela sai do modo de organizacao e passa a sustentar decisao economica de verdade.",
)

next_cols = st.columns([1, 1])
with next_cols[0]:
    list_card(
        title="Sequencia recomendada",
        copy="A ordem importa porque alguns custos sao simples de preencher e liberam a primeira leitura financeira rapidamente.",
        rows=[{"label": f"Passo {index + 1}", "value": step} for index, step in enumerate(readiness["next_steps"])],
        callout="Enquanto os valores nao entrarem, lucro e margem devem continuar fora da narrativa principal do app.",
    )
with next_cols[1]:
    info_card(
        "Resumo financeiro",
        f"Custos conhecidos: {summary['known_total_text']}",
        "Hoje a base ainda nao sustenta custo total, lucro liquido ou margem com credibilidade. A funcao desta pagina e mostrar maturidade da informacao.",
        tone="dark",
    )

source_note("Fonte da pagina: planilha de gestao da fazenda. Nenhum numero de lucro ou margem foi inferido onde a base ainda nao sustenta esse calculo.")
