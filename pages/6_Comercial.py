from __future__ import annotations

from app_core.components import apply_theme, form_intro, render_page_nav, source_note, topline
from app_core.data import identity_context
from app_core.field_forms import render_field_group


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
        "Estrutura inicial para registrar preco recebido e dependencia da cooperativa. "
        "Agora cada caixa faz envio individual."
    ),
    tags=["Preco", "Cooperativa", "Canal", "Venda"],
)

source_note("Cada campo abaixo tem sua propria caixa e seu proprio botao de envio. Cada envio gera um novo registro parcial.")

render_field_group(
    table="comercial",
    title="Comercial atual",
    fields=[
        {"name": "preco_cooperativa_por_kg", "label": "Preco cooperativa por kg", "placeholder": "Ex.: R$ 35,00/kg", "form_key": "preco_cooperativa_por_kg"},
        {"name": "percentual_venda_cooperativa", "label": "Percentual de venda para cooperativa", "placeholder": "Ex.: 100%", "form_key": "percentual_venda_cooperativa"},
    ],
)
