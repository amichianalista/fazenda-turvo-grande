from __future__ import annotations

import streamlit as st

from app_core.components import apply_theme, form_intro, render_page_nav, source_note, topline
from app_core.db import insert_row, payload_has_values
from app_core.data import identity_context


apply_theme(page_title="Turvo Grande | Resultado Financeiro", page_icon="ðŸ§€")
render_page_nav("pages/5_Resultado_Financeiro.py")

identity = identity_context()

topline(
    [
        identity["operation_name"],
        identity["location"],
        "Pagina 5",
        "Formulario de campo",
    ]
)

form_intro(
    kicker="Pagina 5 | Resultado Financeiro",
    title="Formulario de Resultado Financeiro",
    copy=(
        "Tela para consolidar os numeros que resumem o mes: volume, receita, custos e margem. "
        "Aqui a ideia e fechar o retrato economico da operacao."
    ),
    tags=["Receita", "Custos", "Lucro", "Margem"],
)


def save_financeiro_block(block_title: str, payload: dict[str, str | None]) -> None:
    if not payload_has_values(payload):
        st.warning(f"Preencha pelo menos um campo em {block_title.lower()} antes de enviar.")
        return

    try:
        record_id = insert_row("resultado_financeiro", payload)
    except Exception as exc:
        st.error(f"Nao foi possivel salvar o bloco {block_title.lower()} no Supabase: {exc}")
    else:
        st.success(f"{block_title} enviado com sucesso. ID do registro: {record_id}")


source_note("Cada bloco abaixo pode ser enviado separadamente. Cada envio gera um novo registro parcial.")

with st.form("form_resultado_financeiro_volume_receita", clear_on_submit=True):
    st.markdown("### Volume e receita")
    col1, col2 = st.columns(2)
    with col1:
        queijos_por_semana = st.text_input("Queijos por semana", placeholder="Ex.: 154 queijos/semana")
        queijos_por_mes = st.text_input("Queijos por mes", placeholder="Ex.: 616 queijos/mes")
    with col2:
        kg_queijo_por_mes = st.text_input("Kg de queijo por mes", placeholder="Ex.: 616,0 kg/mes")
        receita_bruta_mes = st.text_input("Receita bruta do mes", placeholder="Ex.: R$ 21.560,00")
    submitted_volume_receita = st.form_submit_button("Enviar Volume e receita")

if submitted_volume_receita:
    save_financeiro_block(
        "Volume e receita",
        {
            "queijos_por_semana": queijos_por_semana,
            "queijos_por_mes": queijos_por_mes,
            "kg_queijo_por_mes": kg_queijo_por_mes,
            "receita_bruta_mes": receita_bruta_mes,
        },
    )

with st.form("form_resultado_financeiro_margem", clear_on_submit=True):
    st.markdown("### Custos, lucro e margem")
    col1, col2 = st.columns(2)
    with col1:
        custos_que_ja_sabemos = st.text_input("Custos que ja sabemos", placeholder="Ex.: R$ 8.400,00")
        custos_a_descobrir = st.text_input("Custos a descobrir", placeholder="Ex.: R$ 2.100,00")
    with col2:
        custo_total_atual = st.text_input("Custo total atual", placeholder="Ex.: R$ 10.500,00")
        lucro_liquido_mes = st.text_input("Lucro liquido do mes", placeholder="Ex.: R$ 11.060,00")
        margem_lucro_atual = st.text_input("Margem de lucro atual", placeholder="Ex.: 51,3%")
    submitted_margem = st.form_submit_button("Enviar Custos, lucro e margem")

if submitted_margem:
    save_financeiro_block(
        "Custos, lucro e margem",
        {
            "custos_que_ja_sabemos": custos_que_ja_sabemos,
            "custos_a_descobrir": custos_a_descobrir,
            "custo_total_atual": custo_total_atual,
            "lucro_liquido_mes": lucro_liquido_mes,
            "margem_lucro_atual": margem_lucro_atual,
        },
    )
