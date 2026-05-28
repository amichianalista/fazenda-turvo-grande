from __future__ import annotations

import streamlit as st

from app_core.components import apply_theme, form_intro, render_page_nav, source_note, topline
from app_core.db import insert_batch, payload_has_values
from app_core.data import identity_context


apply_theme(page_title="Turvo Grande | Custos", page_icon="🧀")
render_page_nav("pages/3_Custos.py")

identity = identity_context()

topline(
    [
        identity["operation_name"],
        identity["location"],
        "Pagina 3",
        "Formulario de campo",
    ]
)

form_intro(
    kicker="Pagina 3 | Custos",
    title="Formulario de Custos",
    copy=(
        "Pagina pensada para registrar o retrato dos custos da operacao. Aqui a leitura "
        "fica dividida entre custos fixos da estrutura e custos variaveis ligados a producao."
    ),
    tags=["Custos Fixos", "Custos Variaveis", "Estrutura", "Alimentacao"],
)

source_note("A estrutura abaixo prepara uma unica tela para os dois blocos de custos que ja estao no banco.")

with st.form("form_custos", clear_on_submit=True):
    st.markdown("### Custos fixos | Estrutura")
    col1, col2 = st.columns(2)
    with col1:
        estrutura_energia_eletrica_mensal = st.text_input("Energia eletrica mensal", placeholder="Ex.: R$ 1.250")
        estrutura_agua_mensal = st.text_input("Agua mensal", placeholder="Ex.: R$ 180")
        estrutura_internet_telefone = st.text_input("Internet/telefone", placeholder="Ex.: R$ 150")
        estrutura_manutencao = st.text_input("Manutencao", placeholder="Ex.: R$ 600")
    with col2:
        estrutura_combustivel = st.text_input("Combustivel", placeholder="Ex.: R$ 900")
        estrutura_financiamentos = st.text_input("Financiamentos", placeholder="Ex.: R$ 2.300")
        estrutura_impostos = st.text_input("Impostos", placeholder="Ex.: R$ 400")
        estrutura_funcionarios_fixos = st.text_input("Funcionarios fixos", placeholder="Ex.: R$ 3.200")

    st.markdown("### Custos variaveis | Producao")
    col1, col2 = st.columns(2)
    with col1:
        producao_sal = st.text_input("Sal", placeholder="Ex.: R$ 180/mes")
        producao_coalho = st.text_input("Coalho", placeholder="Ex.: R$ 140/mes")
        producao_embalagem = st.text_input("Embalagem", placeholder="Ex.: R$ 220/mes")
        producao_etiqueta = st.text_input("Etiqueta", placeholder="Ex.: R$ 90/mes")
    with col2:
        producao_transporte = st.text_input("Transporte", placeholder="Ex.: R$ 350/mes")
        producao_frete = st.text_input("Frete", placeholder="Ex.: R$ 500/mes")
        producao_insumos_limpeza = st.text_input("Insumos de limpeza", placeholder="Ex.: R$ 160/mes")

    st.markdown("### Custos variaveis | Alimentacao")
    col1, col2 = st.columns(2)
    with col1:
        alimentacao_racao = st.text_input("Racao", placeholder="Ex.: R$ 4.500/mes")
        alimentacao_milho = st.text_input("Milho", placeholder="Ex.: R$ 1.800/mes")
        alimentacao_silagem = st.text_input("Silagem", placeholder="Ex.: R$ 2.200/mes")
    with col2:
        alimentacao_suplemento_mineral = st.text_input("Suplemento mineral", placeholder="Ex.: R$ 480/mes")
        alimentacao_pastagem_arrendada = st.text_input("Pastagem arrendada", placeholder="Ex.: R$ 1.200/mes")

    submitted = st.form_submit_button("Salvar estrutura de Custos")

if submitted:
    payload_fixos = {
        "estrutura_energia_eletrica_mensal": estrutura_energia_eletrica_mensal,
        "estrutura_agua_mensal": estrutura_agua_mensal,
        "estrutura_internet_telefone": estrutura_internet_telefone,
        "estrutura_manutencao": estrutura_manutencao,
        "estrutura_combustivel": estrutura_combustivel,
        "estrutura_financiamentos": estrutura_financiamentos,
        "estrutura_impostos": estrutura_impostos,
        "estrutura_funcionarios_fixos": estrutura_funcionarios_fixos,
    }
    payload_variaveis = {
        "producao_sal": producao_sal,
        "producao_coalho": producao_coalho,
        "producao_embalagem": producao_embalagem,
        "producao_etiqueta": producao_etiqueta,
        "producao_transporte": producao_transporte,
        "producao_frete": producao_frete,
        "producao_insumos_limpeza": producao_insumos_limpeza,
        "alimentacao_racao": alimentacao_racao,
        "alimentacao_milho": alimentacao_milho,
        "alimentacao_silagem": alimentacao_silagem,
        "alimentacao_suplemento_mineral": alimentacao_suplemento_mineral,
        "alimentacao_pastagem_arrendada": alimentacao_pastagem_arrendada,
    }

    if not (payload_has_values(payload_fixos) or payload_has_values(payload_variaveis)):
        st.warning("Preencha pelo menos um campo antes de enviar.")
    else:
        rows_to_insert: list[tuple[str, dict[str, str | None]]] = []
        if payload_has_values(payload_fixos):
            rows_to_insert.append(("custos_fixos", payload_fixos))
        if payload_has_values(payload_variaveis):
            rows_to_insert.append(("custos_variaveis", payload_variaveis))

        try:
            saved_ids = insert_batch(rows_to_insert)
        except Exception as exc:
            st.error(f"Nao foi possivel salvar os custos no Supabase: {exc}")
        else:
            labels = ", ".join(f"{table}: {record_id}" for table, record_id in saved_ids.items())
            st.success(f"Custos salvos no banco com sucesso. IDs: {labels}")
