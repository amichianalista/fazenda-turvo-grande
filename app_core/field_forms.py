from __future__ import annotations

import streamlit as st

from app_core.db import insert_row, payload_has_values


def render_field_form(
    *,
    table: str,
    field_name: str,
    label: str,
    placeholder: str,
    form_key: str,
    submit_label: str = "Enviar",
) -> None:
    with st.form(form_key, clear_on_submit=True):
        value = st.text_input(label, placeholder=placeholder, key=f"{form_key}_input")
        submitted = st.form_submit_button(submit_label)

    if not submitted:
        return

    payload = {field_name: value}
    if not payload_has_values(payload):
        st.warning(f"Preencha o campo {label.lower()} antes de enviar.")
        return

    try:
        record_id = insert_row(table, payload)
    except Exception as exc:
        st.error(f"Nao foi possivel salvar {label.lower()} no Supabase: {exc}")
    else:
        st.success(f"{label} enviado com sucesso. ID do registro: {record_id}")


def render_field_group(
    *,
    table: str,
    title: str,
    fields: list[dict[str, str]],
    columns: int = 2,
) -> None:
    st.markdown(f"### {title}")
    grid = st.columns(columns)

    for index, field in enumerate(fields):
        with grid[index % columns]:
            render_field_form(
                table=table,
                field_name=field["name"],
                label=field["label"],
                placeholder=field["placeholder"],
                form_key=field["form_key"],
                submit_label=field.get("submit_label", "Enviar"),
            )
