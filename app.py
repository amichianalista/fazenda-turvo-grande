from app_core.components import apply_theme, insight_card, kpi_card, section_header
from app_core.data import cost_coverage_metrics, diagnosis_cards, overview_metrics

import streamlit as st


apply_theme(
    page_title="Automacao Pecuaria | Painel do Produtor",
    page_icon="🐄",
)

st.sidebar.success("Use o menu lateral para navegar pelas paginas.")
overview = overview_metrics()
coverage = cost_coverage_metrics()
diagnostics = diagnosis_cards()

st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-kicker">Painel do produtor</div>
        <h1 class="hero-title">Centro de comando da operacao rural</h1>
        <p class="hero-copy">
            A home agora le a fonte real do projeto e mostra, com transparencia,
            o que ja podemos apresentar ao cliente e o que ainda precisa de preenchimento.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

section_header(
    "Visao geral",
    "A home concentra o tom visual do projeto e prepara a navegacao para as paginas detalhadas.",
)

overview_cols = st.columns(4)
with overview_cols[0]:
    kpi_card("Queijos por dia", overview["queijos_dia"], overview["queijos_dia_delta"])
with overview_cols[1]:
    kpi_card("Receita bruta", overview["receita_bruta"], overview["receita_bruta_delta"])
with overview_cols[2]:
    kpi_card("Margem liquida", overview["margem"], overview["margem_delta"])
with overview_cols[3]:
    kpi_card("Custos com valor", overview["custos_cobertura"], overview["custos_cobertura_delta"])

section_header(
    "Estado atual da base",
    "As paginas abaixo ja usam o CSV real e deixam visivel o nivel de maturidade de cada frente.",
)

grid_cols = st.columns(2)
with grid_cols[0]:
    insight_card(
        "Pagina 1 | Producao",
        "Ja consegue mostrar snapshot real de producao, mas ainda depende de historico e capacidade para ficar completa.",
        tone="green",
        kicker="Cobertura real",
    )
    insight_card(
        "Pagina 3 | Custos",
        f"Estrutura de {coverage['total_categorias']} categorias mapeada, mas so {coverage['categorias_com_valor']} com valor monetizado.",
        tone="earth",
        kicker="Cobertura real",
    )
with grid_cols[1]:
    insight_card(
        "Pagina 2 | Financeiro",
        "Receita bruta ja existe; custos, lucro e margem ainda dependem do preenchimento financeiro.",
        tone="amber",
        kicker="Cobertura real",
    )
    insight_card(
        "Pagina 4 | Diagnostico inteligente",
        "O diagnostico ja aponta lacunas reais da operacao e prioriza a proxima coleta de dados.",
        tone="slate",
        kicker="Cobertura real",
    )

section_header(
    "Diagnosticos imediatos",
    "Essas leituras ja nascem da fonte atual e ajudam a orientar a proxima rodada de preenchimento.",
)

diag_cols = st.columns(2)
for idx, card in enumerate(diagnostics[:4]):
    with diag_cols[idx % 2]:
        insight_card(card["title"], card["copy"], tone=card["tone"], kicker="Leitura")
