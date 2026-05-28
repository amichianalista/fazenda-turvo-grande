from __future__ import annotations

import streamlit as st

from app_core.components import apply_theme, form_intro, render_page_nav, source_note, topline
from app_core.db import insert_row, payload_has_values
from app_core.data import identity_context


apply_theme(page_title="Turvo Grande | Resultado Financeiro", page_icon="🧀")
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

source_note("Campos organizados de acordo com a tabela resultado_financeiro que ja foi criada no banco.")

with st.form("form_resultado_financeiro", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        queijos_por_semana = st.text_input("Queijos por semana", placeholder="Ex.: 154 queijos/semana")
        queijos_por_mes = st.text_input("Queijos por mes", placeholder="Ex.: 616 queijos/mes")
        kg_queijo_por_mes = st.text_input("Kg de queijo por mes", placeholder="Ex.: 616,0 kg/mes")
        receita_bruta_mes = st.text_input("Receita bruta do mes", placeholder="Ex.: R$ 21.560,00")
        custos_que_ja_sabemos = st.text_input("Custos que ja sabemos", placeholder="Ex.: R$ 8.400,00")
    with col2:
        custos_a_descobrir = st.text_input("Custos a descobrir", placeholder="Ex.: R$ 2.100,00")
        custo_total_atual = st.text_input("Custo total atual", placeholder="Ex.: R$ 10.500,00")
        lucro_liquido_mes = st.text_input("Lucro liquido do mes", placeholder="Ex.: R$ 11.060,00")
        margem_lucro_atual = st.text_input("Margem de lucro atual", placeholder="Ex.: 51,3%")

    submitted = st.form_submit_button("Salvar estrutura de Resultado Financeiro")

if submitted:
    payload = {
        "queijos_por_semana": queijos_por_semana,
        "queijos_por_mes": queijos_por_mes,
        "kg_queijo_por_mes": kg_queijo_por_mes,
        "receita_bruta_mes": receita_bruta_mes,
        "custos_que_ja_sabemos": custos_que_ja_sabemos,
        "custos_a_descobrir": custos_a_descobrir,
        "custo_total_atual": custo_total_atual,
        "lucro_liquido_mes": lucro_liquido_mes,
        "margem_lucro_atual": margem_lucro_atual,
    }

    if not payload_has_values(payload):
        st.warning("Preencha pelo menos um campo antes de enviar.")
    else:
        try:
            record_id = insert_row("resultado_financeiro", payload)
        except Exception as exc:
            st.error(f"Nao foi possivel salvar o resultado financeiro no Supabase: {exc}")
        else:
            st.success(f"Resultado financeiro salvo no banco com sucesso. ID do registro: {record_id}")
