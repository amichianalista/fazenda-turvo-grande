from __future__ import annotations

from app_core.components import apply_theme, form_intro, render_page_nav, source_note, topline
from app_core.data import identity_context
from app_core.field_forms import render_field_group


apply_theme(page_title="Turvo Grande | Producao", page_icon="ðŸ§€")
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
        "produtivo. Cada caixa abaixo funciona com envio proprio."
    ),
    tags=["Rebanho", "Leite", "Queijo", "Processo"],
)

source_note("Cada campo abaixo tem sua propria caixa e seu proprio botao de envio. Cada envio gera um novo registro parcial.")

render_field_group(
    table="producao",
    title="Rebanho",
    fields=[
        {"name": "rebanho_quantidade_total_vacas", "label": "Quantidade total de vacas", "placeholder": "Ex.: 48", "form_key": "rebanho_quantidade_total_vacas"},
        {"name": "rebanho_vacas_lactacao", "label": "Vacas em lactacao", "placeholder": "Ex.: 22", "form_key": "rebanho_vacas_lactacao"},
        {"name": "rebanho_vacas_secas", "label": "Vacas secas", "placeholder": "Ex.: 10", "form_key": "rebanho_vacas_secas"},
        {"name": "rebanho_novilhas", "label": "Novilhas", "placeholder": "Ex.: 8", "form_key": "rebanho_novilhas"},
        {"name": "rebanho_bezerras", "label": "Bezerras", "placeholder": "Ex.: 6", "form_key": "rebanho_bezerras"},
        {"name": "rebanho_touros", "label": "Touros", "placeholder": "Ex.: 2", "form_key": "rebanho_touros"},
    ],
)

render_field_group(
    table="producao",
    title="Producao leiteira",
    fields=[
        {"name": "producao_leite_litros_dia", "label": "Litros de leite por dia", "placeholder": "Ex.: 420 litros/dia", "form_key": "producao_leite_litros_dia"},
        {"name": "producao_leite_media_vaca_dia", "label": "Producao media por vaca por dia", "placeholder": "Ex.: 19 litros/vaca/dia", "form_key": "producao_leite_media_vaca_dia"},
        {"name": "producao_leite_pico_producao", "label": "Pico de producao", "placeholder": "Ex.: 500 litros/dia", "form_key": "producao_leite_pico_producao"},
        {"name": "producao_leite_producao_seca", "label": "Producao na seca", "placeholder": "Ex.: 340 litros/dia", "form_key": "producao_leite_producao_seca"},
        {"name": "producao_leite_producao_aguas", "label": "Producao nas aguas", "placeholder": "Ex.: 470 litros/dia", "form_key": "producao_leite_producao_aguas"},
    ],
)

render_field_group(
    table="producao",
    title="Qualidade do leite",
    fields=[
        {"name": "qualidade_leite_gordura_pct", "label": "Gordura (%)", "placeholder": "Ex.: 3,8%", "form_key": "qualidade_leite_gordura_pct"},
        {"name": "qualidade_leite_proteina_pct", "label": "Proteina (%)", "placeholder": "Ex.: 3,2%", "form_key": "qualidade_leite_proteina_pct"},
        {"name": "qualidade_leite_ccs", "label": "CCS", "placeholder": "Ex.: 250.000", "form_key": "qualidade_leite_ccs"},
        {"name": "qualidade_leite_cbt", "label": "CBT", "placeholder": "Ex.: 20.000", "form_key": "qualidade_leite_cbt"},
        {"name": "qualidade_leite_temperatura_armazenamento", "label": "Temperatura de armazenamento", "placeholder": "Ex.: 4 C", "form_key": "qualidade_leite_temperatura_armazenamento"},
        {"name": "qualidade_leite_perdas_leite", "label": "Perdas de leite", "placeholder": "Ex.: 10 litros/semana", "form_key": "qualidade_leite_perdas_leite"},
    ],
)

render_field_group(
    table="producao",
    title="Alimentacao",
    fields=[
        {"name": "alimentacao_tipo_pastagem", "label": "Tipo de pastagem", "placeholder": "Ex.: Brachiaria", "form_key": "alimentacao_tipo_pastagem"},
        {"name": "alimentacao_usa_silagem", "label": "Usa silagem?", "placeholder": "Ex.: Sim", "form_key": "alimentacao_usa_silagem"},
        {"name": "alimentacao_usa_racao", "label": "Usa racao?", "placeholder": "Ex.: Sim", "form_key": "alimentacao_usa_racao"},
        {"name": "alimentacao_custo_mensal", "label": "Custo mensal da alimentacao", "placeholder": "Ex.: R$ 12.000", "form_key": "alimentacao_custo_mensal"},
        {"name": "alimentacao_producao_propria_ou_compra_insumos", "label": "Producao propria ou compra insumos?", "placeholder": "Ex.: Mistura de producao propria e compra", "form_key": "alimentacao_producao_propria_ou_compra_insumos"},
    ],
)

render_field_group(
    table="producao",
    title="Producao do queijo",
    fields=[
        {"name": "producao_queijo_dias_producao_semana", "label": "Dias de producao por semana", "placeholder": "Ex.: 7 dias/semana", "form_key": "producao_queijo_dias_producao_semana"},
        {"name": "producao_queijo_quantidade_queijos_dia", "label": "Quantidade de queijos por dia", "placeholder": "Ex.: 22 queijos/dia", "form_key": "producao_queijo_quantidade_queijos_dia"},
        {"name": "producao_queijo_peso_medio_por_queijo", "label": "Peso medio por queijo", "placeholder": "Ex.: 1,0 kg", "form_key": "producao_queijo_peso_medio_por_queijo"},
        {"name": "producao_queijo_producao_semanal", "label": "Producao semanal", "placeholder": "Ex.: 154 queijos/semana", "form_key": "producao_queijo_producao_semanal"},
        {"name": "producao_queijo_producao_mensal", "label": "Producao mensal", "placeholder": "Ex.: 616 queijos/mes", "form_key": "producao_queijo_producao_mensal"},
    ],
)

render_field_group(
    table="producao",
    title="Processo produtivo",
    fields=[
        {"name": "processo_produtivo_tempo_maturacao", "label": "Tempo de maturacao", "placeholder": "Ex.: 20 dias", "form_key": "processo_produtivo_tempo_maturacao"},
        {"name": "processo_produtivo_quantidade_perdida_maturacao", "label": "Quantidade perdida na maturacao", "placeholder": "Ex.: 6 queijos/mes", "form_key": "processo_produtivo_quantidade_perdida_maturacao"},
        {"name": "processo_produtivo_percentual_descartado", "label": "Percentual descartado", "placeholder": "Ex.: 3%", "form_key": "processo_produtivo_percentual_descartado"},
        {"name": "processo_produtivo_producao_diaria_ou_lotes", "label": "Producao diaria ou em lotes?", "placeholder": "Ex.: Diaria", "form_key": "processo_produtivo_producao_diaria_ou_lotes"},
        {"name": "processo_produtivo_usa_leite_cru", "label": "Usa leite cru?", "placeholder": "Ex.: Sim", "form_key": "processo_produtivo_usa_leite_cru"},
        {"name": "processo_produtivo_tipo_coalho", "label": "Tipo de coalho", "placeholder": "Ex.: Liquido", "form_key": "processo_produtivo_tipo_coalho"},
        {"name": "processo_produtivo_tipo_fermentacao_pingo", "label": "Tipo de fermentacao/pingo", "placeholder": "Ex.: Pingo tradicional", "form_key": "processo_produtivo_tipo_fermentacao_pingo"},
    ],
)
