from __future__ import annotations

from app_core.components import apply_theme, form_intro, render_page_nav, source_note, topline
from app_core.data import identity_context
from app_core.field_forms import render_field_group


apply_theme(page_title="Turvo Grande | Mao de Obra", page_icon="ðŸ§€")
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
        "Estrutura inicial para entender quem toca a operacao no dia a dia. Agora cada "
        "campo pode ser enviado separadamente."
    ),
    tags=["Equipe", "Familia", "Funcionarios", "Rotina"],
)

source_note("Cada campo abaixo tem sua propria caixa e seu proprio botao de envio. Cada envio gera um novo registro parcial.")

render_field_group(
    table="mao_de_obra",
    title="Equipe atual",
    fields=[
        {"name": "quantas_pessoas_trabalham", "label": "Quantas pessoas trabalham?", "placeholder": "Ex.: 4", "form_key": "quantas_pessoas_trabalham"},
        {"name": "quantas_pessoas_da_familia", "label": "Quantas da familia?", "placeholder": "Ex.: 2", "form_key": "quantas_pessoas_da_familia"},
        {"name": "quantos_funcionarios", "label": "Quantos funcionarios?", "placeholder": "Ex.: 2", "form_key": "quantos_funcionarios"},
        {"name": "horas_por_dia_na_producao", "label": "Horas por dia na producao?", "placeholder": "Ex.: 8 horas", "form_key": "horas_por_dia_na_producao"},
    ],
)
