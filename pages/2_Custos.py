from __future__ import annotations

from html import escape

import streamlit as st

from app_core.components import apply_theme, kpi_card, section_header
from app_core.data import cost_metrics, cost_summary, discover_costs, formatting_helpers, known_costs


apply_theme(
    page_title="Turvo Grande: Custos",
    page_icon="🌾",
)

fmt = formatting_helpers()
known = known_costs()
discover = discover_costs()
metrics = cost_metrics()
summary = cost_summary()


def two_up_cards(left_card: str, right_card: str) -> None:
    st.markdown(
        f"""
        <div class="paired-section">
            {left_card}
            {right_card}
        </div>
        """,
        unsafe_allow_html=True,
    )


def cost_card(item: dict[str, str | bool | None], tone: str = "light") -> str:
    tone_class = "cost-card dark" if tone == "dark" else "cost-card"
    note_html = ""
    if item["note_text"]:
        note_html = f"""
        <div class="cost-note">
            <div class="cost-note-label">Observacao</div>
            <div class="cost-note-copy">{escape(str(item["note_text"]))}</div>
        </div>
        """

    return f"""
    <div class="{tone_class}">
        <div class="cost-card-head">
            <div class="cost-card-kicker">Custo mapeado</div>
            <div class="cost-card-status">{escape(str(item["status_text"]))}</div>
        </div>
        <div class="cost-card-title">{escape(str(item["category"]))}</div>
        <div class="cost-card-copy">
            Valor atual: <strong>{escape(str(item["value_text"]))}</strong>
        </div>
        <div class="cost-step">
            <div class="cost-step-label">Como levantar</div>
            <div class="cost-step-copy">{escape(str(item["method_text"]))}</div>
        </div>
        {note_html}
    </div>
    """


st.markdown(
    """
    <style>
        .hero-grid {
            display: grid;
            gap: 1.25rem;
            grid-template-columns: minmax(0, 1.45fr) minmax(290px, 0.75fr);
            position: relative;
            z-index: 1;
        }

        .hero-subline {
            color: rgba(255, 248, 240, 0.74);
            font-size: 0.92rem;
            letter-spacing: 0.16em;
            margin-top: 1.25rem;
            text-transform: uppercase;
        }

        .hero-summary {
            color: rgba(255, 248, 240, 0.86);
            font-size: 1.02rem;
            line-height: 1.75;
            margin-top: 1.05rem;
            max-width: 720px;
        }

        .hero-rail {
            background: linear-gradient(180deg, rgba(255, 248, 239, 0.08), rgba(255, 248, 239, 0.03));
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 26px;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
            display: grid;
            gap: 0.95rem;
            padding: 1.2rem;
            position: relative;
        }

        .hero-rail::before {
            background: linear-gradient(180deg, rgba(217, 192, 125, 0.50), transparent);
            border-radius: 999px;
            content: "";
            height: 72px;
            left: 1.15rem;
            position: absolute;
            top: 1.15rem;
            width: 2px;
        }

        .hero-rail-label {
            color: #f3ddaa;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.18em;
            padding-left: 1rem;
            text-transform: uppercase;
        }

        .hero-rail-card {
            background: linear-gradient(180deg, rgba(255, 248, 239, 0.08), rgba(255, 248, 239, 0.03));
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 22px;
            padding: 1rem 1rem 1.05rem 1rem;
        }

        .hero-rail-kicker {
            color: rgba(243, 221, 170, 0.86);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }

        .hero-rail-value {
            color: #fff8ef;
            font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif;
            font-size: 2.05rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 0.98;
            margin-top: 0.5rem;
        }

        .hero-rail-copy {
            color: rgba(255, 248, 239, 0.78);
            font-size: 0.92rem;
            line-height: 1.6;
            margin-top: 0.45rem;
        }

        .cost-grid {
            display: grid;
            gap: 1rem;
            grid-auto-rows: 1fr;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            margin-top: 1rem;
        }

        .cost-card {
            background: linear-gradient(180deg, rgba(255, 250, 243, 0.64), rgba(248, 241, 232, 0.42));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 30px;
            box-shadow: 0 16px 40px rgba(8, 20, 13, 0.12);
            display: flex;
            flex-direction: column;
            min-height: 100%;
            padding: 1.35rem;
        }

        .cost-card.dark {
            background: linear-gradient(145deg, rgba(18, 49, 34, 0.62), rgba(33, 79, 54, 0.54));
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 18px 44px rgba(7, 16, 11, 0.18);
        }

        .cost-card-head {
            align-items: start;
            display: grid;
            gap: 0.8rem;
            grid-template-columns: minmax(0, 1fr) auto;
        }

        .cost-card-kicker {
            color: #687567;
            font-size: 0.74rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }

        .cost-card.dark .cost-card-kicker {
            color: #e6cc8d;
        }

        .cost-card-status {
            background: rgba(47, 108, 77, 0.10);
            border: 1px solid rgba(47, 108, 77, 0.16);
            border-radius: 999px;
            color: #2f6c4d;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.32rem 0.64rem;
        }

        .cost-card.dark .cost-card-status {
            background: rgba(230, 204, 141, 0.12);
            border: 1px solid rgba(230, 204, 141, 0.18);
            color: #f0dca9;
        }

        .cost-card-title {
            color: #172218;
            font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif;
            font-size: clamp(1.55rem, 2vw, 1.95rem);
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.02;
            margin-top: 0.9rem;
            overflow-wrap: anywhere;
        }

        .cost-card.dark .cost-card-title {
            color: #fff8ef;
        }

        .cost-card-copy {
            color: #4f5d4e;
            font-size: 0.98rem;
            line-height: 1.72;
            margin-top: 0.8rem;
            min-height: 3.6rem;
        }

        .cost-card.dark .cost-card-copy {
            color: rgba(255, 248, 239, 0.80);
        }

        .cost-step,
        .cost-note {
            border-top: 1px solid rgba(22, 34, 23, 0.08);
            margin-top: 1rem;
            padding-top: 0.9rem;
        }

        .cost-step {
            margin-top: auto;
        }

        .cost-card.dark .cost-step,
        .cost-card.dark .cost-note {
            border-top: 1px solid rgba(255, 255, 255, 0.08);
        }

        .cost-step-label,
        .cost-note-label {
            color: #6d786b;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .cost-card.dark .cost-step-label,
        .cost-card.dark .cost-note-label {
            color: rgba(230, 204, 141, 0.78);
        }

        .cost-step-copy,
        .cost-note-copy {
            color: #182319;
            font-size: 1rem;
            font-weight: 600;
            line-height: 1.55;
            margin-top: 0.3rem;
        }

        .cost-card.dark .cost-step-copy,
        .cost-card.dark .cost-note-copy {
            color: #fff8ef;
        }

        .paired-section {
            display: grid;
            gap: 1rem;
            grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
            margin-top: 1rem;
        }

        .editorial-card {
            background: linear-gradient(180deg, rgba(255, 250, 243, 0.64), rgba(248, 241, 232, 0.42));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 30px;
            box-shadow: 0 16px 40px rgba(8, 20, 13, 0.12);
            min-height: 100%;
            overflow: hidden;
            padding: 1.5rem;
            position: relative;
        }

        .editorial-card.dark {
            background: linear-gradient(145deg, rgba(18, 49, 34, 0.62), rgba(33, 79, 54, 0.54));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 18px 44px rgba(7, 16, 11, 0.18);
        }

        .editorial-kicker {
            color: #687567;
            font-size: 0.74rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }

        .editorial-card.dark .editorial-kicker {
            color: #e6cc8d;
        }

        .editorial-title {
            color: #172218;
            font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif;
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 0.98;
            margin-top: 0.75rem;
        }

        .editorial-card.dark .editorial-title {
            color: #fff8ef;
        }

        .editorial-copy {
            color: #4f5d4e;
            font-size: 0.98rem;
            line-height: 1.72;
            margin-top: 0.85rem;
        }

        .editorial-card.dark .editorial-copy {
            color: rgba(255, 248, 239, 0.80);
        }

        .detail-list {
            display: grid;
            gap: 0.8rem;
            margin-top: 1rem;
        }

        .detail-item {
            border-top: 1px solid rgba(22, 34, 23, 0.08);
            padding-top: 0.8rem;
        }

        .editorial-card.dark .detail-item {
            border-top: 1px solid rgba(255, 255, 255, 0.08);
        }

        .item-label {
            color: #6d786b;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .editorial-card.dark .item-label {
            color: rgba(230, 204, 141, 0.78);
        }

        .item-value {
            color: #182319;
            font-size: 1rem;
            font-weight: 600;
            line-height: 1.55;
            margin-top: 0.24rem;
        }

        .editorial-card.dark .item-value {
            color: #fff8ef;
        }

        @media (max-width: 1100px) {
            .hero-grid,
            .cost-grid,
            .paired-section {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 760px) {
            .cost-card-head {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="hero-shell">
        <div class="hero-grid">
            <div>
                <div class="hero-kicker">Pagina 2  Custos</div>
                <h1 class="hero-title">Os custos que ja aparecem na planilha.</h1>
                <div class="hero-subline">O que ja esta mapeado  |  O que ainda falta preencher</div>
                <p class="hero-summary">
                    Aqui a gente separa os custos que a fazenda ja conhece dos que ainda faltam
                    ganhar valor. O foco por enquanto e organizar bem o que ja existe na base.
                </p>
            </div>
            <div class="hero-rail">
                <div class="hero-rail-label">Visao rapida</div>
                <div class="hero-rail-card">
                    <div class="hero-rail-kicker">Custos mapeados</div>
                    <div class="hero-rail-value">{metrics["known_count"]}</div>
                    <div class="hero-rail-copy">Itens que ja aparecem como custo conhecido na planilha.</div>
                </div>
                <div class="hero-rail-card">
                    <div class="hero-rail-kicker">Valor atual</div>
                    <div class="hero-rail-value">{summary["current_total_text"]}</div>
                    <div class="hero-rail-copy">Hoje a base ainda esta sem os valores reais preenchidos.</div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(4)
with metric_cols[0]:
    kpi_card("Custos ja mapeados", str(metrics["known_count"]), "Categorias conhecidas")
with metric_cols[1]:
    kpi_card("Com valor", str(metrics["filled_count"]), "Preenchidos de verdade")
with metric_cols[2]:
    kpi_card("Sem valor", str(metrics["pending_count"]), "Ainda faltando")
with metric_cols[3]:
    kpi_card("A descobrir", str(metrics["discover_count"]), "Custos para levantar")

section_header(
    "Custos que ja temos",
    "Esses sao os custos que ja aparecem com nome certo na planilha, mesmo sem o valor preenchido.",
)

two_up_cards(
    f"""
    <div class="editorial-card glow">
        <div class="editorial-kicker">O que ja esta certo</div>
        <div class="editorial-title">{metrics["known_count"]} custos ja aparecem separados.</div>
        <div class="editorial-copy">
            A fazenda ja tem uma boa parte da estrutura pronta. Falta agora so transformar essa lista em numero.
        </div>
        <div class="detail-list">
            <div class="detail-item">
                <div class="item-label">Custos conhecidos</div>
                <div class="item-value">{metrics["known_count"]} itens mapeados</div>
            </div>
            <div class="detail-item">
                <div class="item-label">Total anotado hoje</div>
                <div class="item-value">{summary["known_total_text"]}</div>
            </div>
        </div>
    </div>
    """,
    """
    <div class="editorial-card dark">
        <div class="editorial-kicker">Jeito de usar esta pagina</div>
        <div class="editorial-title">Primeiro olha o nome do custo. Depois preenche o valor.</div>
        <div class="editorial-copy">
            O mais importante aqui e deixar a equipe saber exatamente o que ja esta listado
            e como cada custo pode ser levantado.
        </div>
        <div class="detail-list">
            <div class="detail-item">
                <div class="item-label">Status atual</div>
                <div class="item-value">Todos ainda estao sem valor</div>
            </div>
            <div class="detail-item">
                <div class="item-label">Proximo passo</div>
                <div class="item-value">Pegar nota, conta, diaria ou contrato e jogar na planilha</div>
            </div>
        </div>
    </div>
    """,
)

known_html = "".join(cost_card(item, tone="light" if idx % 2 == 0 else "dark") for idx, item in enumerate(known))
st.markdown(f'<div class="cost-grid">{known_html}</div>', unsafe_allow_html=True)

section_header(
    "Leitura da pagina",
    "Hoje a parte mais importante nao e o total, e sim deixar bem claro o que ja esta organizado para preencher.",
)

two_up_cards(
    f"""
    <div class="editorial-card glow">
        <div class="editorial-kicker">Custos conhecidos</div>
        <div class="editorial-title">{summary["known_total_text"]}</div>
        <div class="editorial-copy">
            A planilha ja separa bem os custos que a fazenda conhece, mas os valores ainda nao entraram.
        </div>
        <div class="detail-list">
            <div class="detail-item">
                <div class="item-label">Itens conhecidos</div>
                <div class="item-value">{metrics["known_count"]} categorias ja listadas</div>
            </div>
            <div class="detail-item">
                <div class="item-label">Com valor hoje</div>
                <div class="item-value">{metrics["filled_count"]} preenchidos</div>
            </div>
        </div>
    </div>
    """,
    f"""
    <div class="editorial-card dark">
        <div class="editorial-kicker">O que esta faltando</div>
        <div class="editorial-title">Ainda falta colocar o valor de cada custo na conta.</div>
        <div class="editorial-copy">
            A estrutura ja esta boa. O proximo passo agora e colocar os numeros para essa pagina
            comecar a mostrar custo de verdade.
        </div>
        <div class="detail-list">
            <div class="detail-item">
                <div class="item-label">Sem valor</div>
                <div class="item-value">{metrics["pending_count"]} itens esperando preenchimento</div>
            </div>
            <div class="detail-item">
                <div class="item-label">Total atual</div>
                <div class="item-value">{summary["current_total_text"]}</div>
            </div>
        </div>
    </div>
    """,
)

section_header(
    "O que ainda falta levantar",
    "Esses custos tambem ja aparecem na planilha, mas ainda estao na lista do que precisa descobrir melhor.",
)

discover_html = "".join(cost_card(item, tone="dark" if idx % 2 == 0 else "light") for idx, item in enumerate(discover))
st.markdown(f'<div class="cost-grid">{discover_html}</div>', unsafe_allow_html=True)
