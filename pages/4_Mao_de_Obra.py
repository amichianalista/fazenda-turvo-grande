from __future__ import annotations

import streamlit as st

from app_core.components import apply_theme, form_intro, render_page_nav, source_note, topline
from app_core.db import insert_row, payload_has_values
from app_core.data import identity_context


apply_theme(page_title="Turvo Grande | Mao de Obra", page_icon="🧀")
render_page_nav("pages/4_Mao_de_Obra.py")

identity = identity_context()

topline(
    [
        identity["operation_name"],
        identity["location"],
        "Pagina 4",
        "Formulario de campo",
    ]
)

form_intro(
    kicker="Pagina 4 | Mao de Obra",
    title="Formulario de Mao de Obra",
    copy=(
        "Estrutura inicial para entender quem toca a operacao no dia a dia, qual o peso da "
        "familia no trabalho e quanto tempo vai para a producao."
    ),
    tags=["Equipe", "Familia", "Funcionarios", "Rotina"],
)

source_note("Este formulario cobre os campos ja modelados na tabela de mao de obra.")

with st.form("form_mao_de_obra", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        quantas_pessoas_trabalham = st.text_input("Quantas pessoas trabalham?", placeholder="Ex.: 4")
        quantas_pessoas_da_familia = st.text_input("Quantas da familia?", placeholder="Ex.: 2")
    with col2:
        quantos_funcionarios = st.text_input("Quantos funcionarios?", placeholder="Ex.: 2")
        horas_por_dia_na_producao = st.text_input("Horas por dia na producao?", placeholder="Ex.: 8 horas")

    submitted = st.form_submit_button("Salvar estrutura de Mao de Obra")

if submitted:
    payload = {
        "quantas_pessoas_trabalham": quantas_pessoas_trabalham,
        "quantas_pessoas_da_familia": quantas_pessoas_da_familia,
        "quantos_funcionarios": quantos_funcionarios,
        "horas_por_dia_na_producao": horas_por_dia_na_producao,
    }

    if not payload_has_values(payload):
        st.warning("Preencha pelo menos um campo antes de enviar.")
    else:
        try:
            record_id = insert_row("mao_de_obra", payload)
        except Exception as exc:
            st.error(f"Nao foi possivel salvar a mao de obra no Supabase: {exc}")
        else:
            st.success(f"Mao de obra salva no banco com sucesso. ID do registro: {record_id}")
