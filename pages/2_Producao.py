from __future__ import annotations

import streamlit as st

from app_core.components import apply_theme, form_intro, render_page_nav, source_note, topline
from app_core.db import insert_row, payload_has_values
from app_core.data import identity_context


apply_theme(page_title="Turvo Grande | Producao", page_icon="🧀")
render_page_nav("pages/2_Producao.py")

identity = identity_context()

topline(
    [
        identity["operation_name"],
        identity["location"],
        "Pagina 2",
        "Formulario de campo",
    ]
)

form_intro(
    kicker="Pagina 2 | Producao",
    title="Formulario de Producao",
    copy=(
        "Estrutura inicial para a conversa de campo sobre rebanho, leite, queijo e processo "
        "produtivo. Cada bloco abaixo representa um trecho da entrevista."
    ),
    tags=["Rebanho", "Leite", "Queijo", "Processo"],
)

source_note("Esqueleto inicial do formulario. O proximo passo sera ligar este envio ao Supabase.")

with st.form("form_producao", clear_on_submit=True):
    st.markdown("### Rebanho")
    col1, col2 = st.columns(2)
    with col1:
        rebanho_quantidade_total_vacas = st.text_input("Quantidade total de vacas", placeholder="Ex.: 48")
        rebanho_vacas_lactacao = st.text_input("Vacas em lactacao", placeholder="Ex.: 22")
        rebanho_vacas_secas = st.text_input("Vacas secas", placeholder="Ex.: 10")
    with col2:
        rebanho_novilhas = st.text_input("Novilhas", placeholder="Ex.: 8")
        rebanho_bezerras = st.text_input("Bezerras", placeholder="Ex.: 6")
        rebanho_touros = st.text_input("Touros", placeholder="Ex.: 2")

    st.markdown("### Producao leiteira")
    col1, col2 = st.columns(2)
    with col1:
        producao_leite_litros_dia = st.text_input("Litros de leite por dia", placeholder="Ex.: 420 litros/dia")
        producao_leite_media_vaca_dia = st.text_input(
            "Producao media por vaca por dia",
            placeholder="Ex.: 19 litros/vaca/dia",
        )
        producao_leite_pico_producao = st.text_input("Pico de producao", placeholder="Ex.: 500 litros/dia")
    with col2:
        producao_leite_producao_seca = st.text_input("Producao na seca", placeholder="Ex.: 340 litros/dia")
        producao_leite_producao_aguas = st.text_input("Producao nas aguas", placeholder="Ex.: 470 litros/dia")

    st.markdown("### Qualidade do leite")
    col1, col2 = st.columns(2)
    with col1:
        qualidade_leite_gordura_pct = st.text_input("Gordura (%)", placeholder="Ex.: 3,8%")
        qualidade_leite_proteina_pct = st.text_input("Proteina (%)", placeholder="Ex.: 3,2%")
        qualidade_leite_ccs = st.text_input("CCS", placeholder="Ex.: 250.000")
    with col2:
        qualidade_leite_cbt = st.text_input("CBT", placeholder="Ex.: 20.000")
        qualidade_leite_temperatura_armazenamento = st.text_input(
            "Temperatura de armazenamento",
            placeholder="Ex.: 4 C",
        )
        qualidade_leite_perdas_leite = st.text_input("Perdas de leite", placeholder="Ex.: 10 litros/semana")

    st.markdown("### Alimentacao")
    col1, col2 = st.columns(2)
    with col1:
        alimentacao_tipo_pastagem = st.text_input("Tipo de pastagem", placeholder="Ex.: Brachiaria")
        alimentacao_usa_silagem = st.text_input("Usa silagem?", placeholder="Ex.: Sim")
        alimentacao_usa_racao = st.text_input("Usa racao?", placeholder="Ex.: Sim")
    with col2:
        alimentacao_custo_mensal = st.text_input("Custo mensal da alimentacao", placeholder="Ex.: R$ 12.000")
        alimentacao_producao_propria_ou_compra_insumos = st.text_input(
            "Producao propria ou compra insumos?",
            placeholder="Ex.: Mistura de producao propria e compra",
        )

    st.markdown("### Producao do queijo")
    col1, col2 = st.columns(2)
    with col1:
        producao_queijo_dias_producao_semana = st.text_input(
            "Dias de producao por semana",
            placeholder="Ex.: 7 dias/semana",
        )
        producao_queijo_quantidade_queijos_dia = st.text_input(
            "Quantidade de queijos por dia",
            placeholder="Ex.: 22 queijos/dia",
        )
    with col2:
        producao_queijo_peso_medio_por_queijo = st.text_input("Peso medio por queijo", placeholder="Ex.: 1,0 kg")
        producao_queijo_producao_semanal = st.text_input("Producao semanal", placeholder="Ex.: 154 queijos/semana")
        producao_queijo_producao_mensal = st.text_input("Producao mensal", placeholder="Ex.: 616 queijos/mes")

    st.markdown("### Processo produtivo")
    col1, col2 = st.columns(2)
    with col1:
        processo_produtivo_tempo_maturacao = st.text_input("Tempo de maturacao", placeholder="Ex.: 20 dias")
        processo_produtivo_quantidade_perdida_maturacao = st.text_input(
            "Quantidade perdida na maturacao",
            placeholder="Ex.: 6 queijos/mes",
        )
        processo_produtivo_percentual_descartado = st.text_input("Percentual descartado", placeholder="Ex.: 3%")
        processo_produtivo_producao_diaria_ou_lotes = st.text_input(
            "Producao diaria ou em lotes?",
            placeholder="Ex.: Diaria",
        )
    with col2:
        processo_produtivo_usa_leite_cru = st.text_input("Usa leite cru?", placeholder="Ex.: Sim")
        processo_produtivo_tipo_coalho = st.text_input("Tipo de coalho", placeholder="Ex.: Liquido")
        processo_produtivo_tipo_fermentacao_pingo = st.text_input(
            "Tipo de fermentacao/pingo",
            placeholder="Ex.: Pingo tradicional",
        )

    submitted = st.form_submit_button("Salvar estrutura de Producao")

if submitted:
    payload = {
        "rebanho_quantidade_total_vacas": rebanho_quantidade_total_vacas,
        "rebanho_vacas_lactacao": rebanho_vacas_lactacao,
        "rebanho_vacas_secas": rebanho_vacas_secas,
        "rebanho_novilhas": rebanho_novilhas,
        "rebanho_bezerras": rebanho_bezerras,
        "rebanho_touros": rebanho_touros,
        "producao_leite_litros_dia": producao_leite_litros_dia,
        "producao_leite_media_vaca_dia": producao_leite_media_vaca_dia,
        "producao_leite_pico_producao": producao_leite_pico_producao,
        "producao_leite_producao_seca": producao_leite_producao_seca,
        "producao_leite_producao_aguas": producao_leite_producao_aguas,
        "qualidade_leite_gordura_pct": qualidade_leite_gordura_pct,
        "qualidade_leite_proteina_pct": qualidade_leite_proteina_pct,
        "qualidade_leite_ccs": qualidade_leite_ccs,
        "qualidade_leite_cbt": qualidade_leite_cbt,
        "qualidade_leite_temperatura_armazenamento": qualidade_leite_temperatura_armazenamento,
        "qualidade_leite_perdas_leite": qualidade_leite_perdas_leite,
        "alimentacao_tipo_pastagem": alimentacao_tipo_pastagem,
        "alimentacao_usa_silagem": alimentacao_usa_silagem,
        "alimentacao_usa_racao": alimentacao_usa_racao,
        "alimentacao_custo_mensal": alimentacao_custo_mensal,
        "alimentacao_producao_propria_ou_compra_insumos": alimentacao_producao_propria_ou_compra_insumos,
        "producao_queijo_dias_producao_semana": producao_queijo_dias_producao_semana,
        "producao_queijo_quantidade_queijos_dia": producao_queijo_quantidade_queijos_dia,
        "producao_queijo_peso_medio_por_queijo": producao_queijo_peso_medio_por_queijo,
        "producao_queijo_producao_semanal": producao_queijo_producao_semanal,
        "producao_queijo_producao_mensal": producao_queijo_producao_mensal,
        "processo_produtivo_tempo_maturacao": processo_produtivo_tempo_maturacao,
        "processo_produtivo_quantidade_perdida_maturacao": processo_produtivo_quantidade_perdida_maturacao,
        "processo_produtivo_percentual_descartado": processo_produtivo_percentual_descartado,
        "processo_produtivo_producao_diaria_ou_lotes": processo_produtivo_producao_diaria_ou_lotes,
        "processo_produtivo_usa_leite_cru": processo_produtivo_usa_leite_cru,
        "processo_produtivo_tipo_coalho": processo_produtivo_tipo_coalho,
        "processo_produtivo_tipo_fermentacao_pingo": processo_produtivo_tipo_fermentacao_pingo,
    }

    if not payload_has_values(payload):
        st.warning("Preencha pelo menos um campo antes de enviar.")
    else:
        try:
            record_id = insert_row("producao", payload)
        except Exception as exc:
            st.error(f"Nao foi possivel salvar a producao no Supabase: {exc}")
        else:
            st.success(f"Producao salva no banco com sucesso. ID do registro: {record_id}")
