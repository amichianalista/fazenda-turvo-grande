from __future__ import annotations

import streamlit as st

from app_core.components import apply_theme, form_intro, render_page_nav, source_note, topline
from app_core.db import insert_row, payload_has_values
from app_core.data import identity_context


apply_theme(page_title="Turvo Grande | Comercial", page_icon="ðŸ§€")
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


def save_comercial_block(block_title: str, payload: dict[str, str | None]) -> None:
    if not payload_has_values(payload):
        st.warning(f"Preencha pelo menos um campo em {block_title.lower()} antes de enviar.")
        return

    try:
        record_id = insert_row("comercial", payload)
    except Exception as exc:
        st.error(f"Nao foi possivel salvar o bloco {block_title.lower()} no Supabase: {exc}")
    else:
        st.success(f"{block_title} enviado com sucesso. ID do registro: {record_id}")


source_note("Cada bloco abaixo pode ser enviado separadamente. Cada envio gera um novo registro parcial.")

with st.form("form_comercial_preco", clear_on_submit=True):
    st.markdown("### Preco atual")
    preco_cooperativa_por_kg = st.text_input("Preco cooperativa por kg", placeholder="Ex.: R$ 35,00/kg")
    submitted_preco = st.form_submit_button("Enviar Preco atual")

if submitted_preco:
    save_comercial_block(
        "Preco atual",
        {
            "preco_cooperativa_por_kg": preco_cooperativa_por_kg,
        },
    )

with st.form("form_comercial_dependencia", clear_on_submit=True):
    st.markdown("### Dependencia da cooperativa")
    percentual_venda_cooperativa = st.text_input(
        "Percentual de venda para cooperativa",
        placeholder="Ex.: 100%",
    )
    submitted_dependencia = st.form_submit_button("Enviar Dependencia da cooperativa")

if submitted_dependencia:
    save_comercial_block(
        "Dependencia da cooperativa",
        {
            "percentual_venda_cooperativa": percentual_venda_cooperativa,
        },
    )
