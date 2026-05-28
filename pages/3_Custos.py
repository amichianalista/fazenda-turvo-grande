from __future__ import annotations

from app_core.components import apply_theme, form_intro, render_page_nav, source_note, topline
from app_core.data import identity_context
from app_core.field_forms import render_field_group


apply_theme(page_title="Turvo Grande | Custos", page_icon="ðŸ§€")
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
        "Pagina pensada para registrar o retrato dos custos da operacao. Aqui cada campo "
        "ganha sua propria caixa com envio individual."
    ),
    tags=["Custos Fixos", "Custos Variaveis", "Estrutura", "Alimentacao"],
)

source_note("Cada campo abaixo tem sua propria caixa e seu proprio botao de envio. Cada envio gera um novo registro parcial.")

render_field_group(
    table="custos_fixos",
    title="Custos fixos | Estrutura",
    fields=[
        {"name": "estrutura_energia_eletrica_mensal", "label": "Energia eletrica mensal", "placeholder": "Ex.: R$ 1.250", "form_key": "estrutura_energia_eletrica_mensal"},
        {"name": "estrutura_agua_mensal", "label": "Agua mensal", "placeholder": "Ex.: R$ 180", "form_key": "estrutura_agua_mensal"},
        {"name": "estrutura_internet_telefone", "label": "Internet/telefone", "placeholder": "Ex.: R$ 150", "form_key": "estrutura_internet_telefone"},
        {"name": "estrutura_manutencao", "label": "Manutencao", "placeholder": "Ex.: R$ 600", "form_key": "estrutura_manutencao"},
        {"name": "estrutura_combustivel", "label": "Combustivel", "placeholder": "Ex.: R$ 900", "form_key": "estrutura_combustivel"},
        {"name": "estrutura_financiamentos", "label": "Financiamentos", "placeholder": "Ex.: R$ 2.300", "form_key": "estrutura_financiamentos"},
        {"name": "estrutura_impostos", "label": "Impostos", "placeholder": "Ex.: R$ 400", "form_key": "estrutura_impostos"},
        {"name": "estrutura_funcionarios_fixos", "label": "Funcionarios fixos", "placeholder": "Ex.: R$ 3.200", "form_key": "estrutura_funcionarios_fixos"},
    ],
)

render_field_group(
    table="custos_variaveis",
    title="Custos variaveis | Producao",
    fields=[
        {"name": "producao_sal", "label": "Sal", "placeholder": "Ex.: R$ 180/mes", "form_key": "producao_sal"},
        {"name": "producao_coalho", "label": "Coalho", "placeholder": "Ex.: R$ 140/mes", "form_key": "producao_coalho"},
        {"name": "producao_embalagem", "label": "Embalagem", "placeholder": "Ex.: R$ 220/mes", "form_key": "producao_embalagem"},
        {"name": "producao_etiqueta", "label": "Etiqueta", "placeholder": "Ex.: R$ 90/mes", "form_key": "producao_etiqueta"},
        {"name": "producao_transporte", "label": "Transporte", "placeholder": "Ex.: R$ 350/mes", "form_key": "producao_transporte"},
        {"name": "producao_frete", "label": "Frete", "placeholder": "Ex.: R$ 500/mes", "form_key": "producao_frete"},
        {"name": "producao_insumos_limpeza", "label": "Insumos de limpeza", "placeholder": "Ex.: R$ 160/mes", "form_key": "producao_insumos_limpeza"},
    ],
)

render_field_group(
    table="custos_variaveis",
    title="Custos variaveis | Alimentacao",
    fields=[
        {"name": "alimentacao_racao", "label": "Racao", "placeholder": "Ex.: R$ 4.500/mes", "form_key": "alimentacao_racao_custos"},
        {"name": "alimentacao_milho", "label": "Milho", "placeholder": "Ex.: R$ 1.800/mes", "form_key": "alimentacao_milho_custos"},
        {"name": "alimentacao_silagem", "label": "Silagem", "placeholder": "Ex.: R$ 2.200/mes", "form_key": "alimentacao_silagem_custos"},
        {"name": "alimentacao_suplemento_mineral", "label": "Suplemento mineral", "placeholder": "Ex.: R$ 480/mes", "form_key": "alimentacao_suplemento_mineral"},
        {"name": "alimentacao_pastagem_arrendada", "label": "Pastagem arrendada", "placeholder": "Ex.: R$ 1.200/mes", "form_key": "alimentacao_pastagem_arrendada"},
    ],
)
