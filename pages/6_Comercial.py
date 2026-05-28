from __future__ import annotations

import streamlit as st

from app_core.components import apply_theme, form_intro, render_page_nav, source_note, topline
from app_core.db import insert_row, payload_has_values
from app_core.data import identity_context


apply_theme(page_title="Turvo Grande | Comercial", page_icon="🧀")
render_page_nav("pages/6_Comercial.py")

identity = identity_context()

topline(
    [
        identity["operation_name"],
        identity["location"],
        "Pagina 6",
        "Formulario de campo",
    ]
)

form_intro(
    kicker="Pagina 6 | Comercial",
    title="Formulario Comercial",
    copy=(
        "Estrutura inicial para registrar o preco recebido e o grau de dependencia da cooperativa. "
        "E o bloco mais direto da leitura comercial atual."
    ),
    tags=["Preco", "Cooperativa", "Canal", "Venda"],
)

source_note("Formulario alinhado aos campos da tabela comercial criada no Supabase.")

with st.form("form_comercial", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        preco_cooperativa_por_kg = st.text_input("Preco cooperativa por kg", placeholder="Ex.: R$ 35,00/kg")
    with col2:
        percentual_venda_cooperativa = st.text_input(
            "Percentual de venda para cooperativa",
            placeholder="Ex.: 100%",
        )

    submitted = st.form_submit_button("Salvar estrutura Comercial")

if submitted:
    payload = {
        "preco_cooperativa_por_kg": preco_cooperativa_por_kg,
        "percentual_venda_cooperativa": percentual_venda_cooperativa,
    }

    if not payload_has_values(payload):
        st.warning("Preencha pelo menos um campo antes de enviar.")
    else:
        try:
            record_id = insert_row("comercial", payload)
        except Exception as exc:
            st.error(f"Nao foi possivel salvar o comercial no Supabase: {exc}")
        else:
            st.success(f"Comercial salvo no banco com sucesso. ID do registro: {record_id}")
