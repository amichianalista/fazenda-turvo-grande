from __future__ import annotations

from app_core.components import apply_theme, form_intro, render_page_nav, source_note, topline
from app_core.data import identity_context
from app_core.field_forms import render_field_group


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
        "Tela para consolidar os numeros que resumem o mes. Agora cada caixa de digitacao "
        "tem envio proprio."
    ),
    tags=["Receita", "Custos", "Lucro", "Margem"],
)

source_note("Cada campo abaixo tem sua propria caixa e seu proprio botao de envio. Cada envio gera um novo registro parcial.")

render_field_group(
    table="resultado_financeiro",
    title="Volume e receita",
    fields=[
        {"name": "queijos_por_semana", "label": "Queijos por semana", "placeholder": "Ex.: 154 queijos/semana", "form_key": "queijos_por_semana"},
        {"name": "queijos_por_mes", "label": "Queijos por mes", "placeholder": "Ex.: 616 queijos/mes", "form_key": "queijos_por_mes"},
        {"name": "kg_queijo_por_mes", "label": "Kg de queijo por mes", "placeholder": "Ex.: 616,0 kg/mes", "form_key": "kg_queijo_por_mes"},
        {"name": "receita_bruta_mes", "label": "Receita bruta do mes", "placeholder": "Ex.: R$ 21.560,00", "form_key": "receita_bruta_mes"},
    ],
)

render_field_group(
    table="resultado_financeiro",
    title="Custos, lucro e margem",
    fields=[
        {"name": "custos_que_ja_sabemos", "label": "Custos que ja sabemos", "placeholder": "Ex.: R$ 8.400,00", "form_key": "custos_que_ja_sabemos"},
        {"name": "custos_a_descobrir", "label": "Custos a descobrir", "placeholder": "Ex.: R$ 2.100,00", "form_key": "custos_a_descobrir"},
        {"name": "custo_total_atual", "label": "Custo total atual", "placeholder": "Ex.: R$ 10.500,00", "form_key": "custo_total_atual"},
        {"name": "lucro_liquido_mes", "label": "Lucro liquido do mes", "placeholder": "Ex.: R$ 11.060,00", "form_key": "lucro_liquido_mes"},
        {"name": "margem_lucro_atual", "label": "Margem de lucro atual", "placeholder": "Ex.: 51,3%", "form_key": "margem_lucro_atual"},
    ],
)
