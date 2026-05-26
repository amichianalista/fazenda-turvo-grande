from __future__ import annotations

import streamlit as st

from app_core.components import apply_theme, kpi_card, section_header
from app_core.data import commercial_metrics, formatting_helpers, identity_context, production_metrics


apply_theme(
    page_title="Turvo Grande: Queijo Minas Artesanal",
    page_icon="🌾",
)

fmt = formatting_helpers()
identity = identity_context()
production = production_metrics()
commercial = commercial_metrics()

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
            background: linear-gradient(180deg, rgba(255, 248, 239, 0.10), rgba(255, 248, 239, 0.05));
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
            background: linear-gradient(180deg, rgba(255, 248, 239, 0.10), rgba(255, 248, 239, 0.04));
            border: 1px solid rgba(255, 255, 255, 0.08);
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

        .section-ribbon {
            align-items: center;
            display: flex;
            gap: 0.8rem;
            margin-bottom: 0.95rem;
        }

        .section-index {
            background: rgba(217, 192, 125, 0.16);
            border: 1px solid rgba(217, 192, 125, 0.22);
            border-radius: 999px;
            color: #f0dca9;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            padding: 0.42rem 0.78rem;
            text-transform: uppercase;
        }

        .editorial-card {
            background: linear-gradient(180deg, rgba(255, 250, 243, 0.90), rgba(248, 241, 232, 0.80));
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 30px;
            box-shadow: 0 22px 56px rgba(8, 20, 13, 0.14);
            min-height: 100%;
            overflow: hidden;
            padding: 1.5rem;
            position: relative;
        }

        .editorial-card.dark {
            background: linear-gradient(145deg, rgba(18, 49, 34, 0.96), rgba(33, 79, 54, 0.92));
            border: 1px solid rgba(255, 255, 255, 0.10);
            box-shadow: 0 24px 64px rgba(7, 16, 11, 0.24);
        }

        .editorial-card.glow::after {
            background: radial-gradient(circle at top right, rgba(217, 192, 125, 0.24), transparent 34%);
            content: "";
            inset: 0;
            pointer-events: none;
            position: absolute;
        }

        .editorial-kicker {
            color: #687567;
            font-size: 0.74rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            position: relative;
            text-transform: uppercase;
            z-index: 1;
        }

        .editorial-card.dark .editorial-kicker {
            color: #e6cc8d;
        }

        .editorial-title {
            color: #172218;
            font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif;
            font-size: 2.05rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 0.98;
            margin-top: 0.65rem;
            position: relative;
            z-index: 1;
        }

        .editorial-card.dark .editorial-title {
            color: #fff8ef;
        }

        .editorial-copy {
            color: #4f5d4e;
            font-size: 0.98rem;
            line-height: 1.75;
            margin-top: 0.9rem;
            position: relative;
            z-index: 1;
        }

        .editorial-card.dark .editorial-copy {
            color: rgba(255, 248, 239, 0.80);
        }

        .identity-stack,
        .detail-list,
        .signal-grid {
            display: grid;
            gap: 0.8rem;
            margin-top: 1.1rem;
            position: relative;
            z-index: 1;
        }

        .identity-item,
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
            font-size: 1.05rem;
            font-weight: 700;
            line-height: 1.45;
            margin-top: 0.18rem;
        }

        .editorial-card.dark .item-value {
            color: #fff8ef;
        }

        .signal-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .signal-tile {
            background: rgba(255, 248, 239, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 22px;
            padding: 0.95rem;
        }

        .signal-tile-label {
            color: rgba(230, 204, 141, 0.76);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .signal-tile-value {
            color: #fff8ef;
            font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif;
            font-size: 1.45rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1;
            margin-top: 0.45rem;
        }

        .signal-strip {
            align-items: stretch;
            display: grid;
            gap: 0.95rem;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            margin-top: 1rem;
        }

        .signal-panel {
            background: linear-gradient(180deg, rgba(255, 250, 243, 0.88), rgba(248, 241, 232, 0.76));
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 24px;
            box-shadow: 0 16px 42px rgba(8, 20, 13, 0.12);
            padding: 1.15rem;
        }

        .signal-panel-label {
            color: #6d786b;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .signal-panel-value {
            color: #172218;
            font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif;
            font-size: 1.72rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 0.98;
            margin-top: 0.55rem;
        }

        .signal-panel-copy {
            color: #4f5d4e;
            font-size: 0.92rem;
            line-height: 1.6;
            margin-top: 0.38rem;
        }

        @media (max-width: 1100px) {
            .hero-grid,
            .signal-strip {
                grid-template-columns: 1fr;
            }

            .signal-grid {
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
                <div class="hero-kicker">Pagina 1  Visao Geral</div>
                <h1 class="hero-title">Turvo Grande: Queijo Minas Artesanal</h1>
                <div class="hero-subline">{identity["product_name"]}  |  {identity["location"]}</div>
                <p class="hero-summary">
                    Aqui a gente mostra o que ja tem preenchido na planilha da fazenda:
                    de onde vem a producao, quanto esta saindo por dia e quanto entra na venda.
                    Tudo de um jeito direto, sem complicacao.
                </p>
            </div>
            <div class="hero-rail">
                <div class="hero-rail-label">Numero da vez</div>
                <div class="hero-rail-card">
                    <div class="hero-rail-kicker">Producao do mes</div>
                    <div class="hero-rail-value">{fmt["number"](production["queijos_mes"], suffix=" un.")}</div>
                    <div class="hero-rail-copy">Quantidade que a planilha ja mostra para o mes.</div>
                </div>
                <div class="hero-rail-card">
                    <div class="hero-rail-kicker">Venda bruta</div>
                    <div class="hero-rail-value">{fmt["currency"](commercial["receita_bruta"])}</div>
                    <div class="hero-rail-copy">Valor bruto do mes pelo preco pago no queijo.</div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(4)
with metric_cols[0]:
    kpi_card("Operacao", identity["operation_name"], "Fonte oficial da planilha")
with metric_cols[1]:
    kpi_card("Queijos por dia", fmt["number"](production["queijos_dia"], suffix=" un."), "Cadencia atual")
with metric_cols[2]:
    kpi_card("Kg por mes", fmt["number"](production["kg_mes"], decimals=1, suffix=" kg"), "Escala mensal")
with metric_cols[3]:
    kpi_card("Receita bruta", fmt["currency"](commercial["receita_bruta"]), "Leitura comercial")

section_header(
    "Identidade e contexto",
    "Primeiro, vamos situar bem a fazenda e o tipo de producao que ela toca hoje.",
)

st.markdown('<div class="section-ribbon"><div class="section-index">Bloco 1</div></div>', unsafe_allow_html=True)

identity_cols = st.columns([1.12, 0.88])
with identity_cols[0]:
    st.markdown(
        f"""
        <div class="editorial-card glow">
            <div class="editorial-kicker">Quem e a fazenda</div>
            <div class="editorial-title">{identity["operation_name"]}</div>
            <div class="editorial-copy">
                Pelo que esta na planilha, a fazenda trabalha com queijo minas artesanal
                e hoje vende tudo pela cooperativa.
            </div>
            <div class="identity-stack">
                <div class="identity-item">
                    <div class="item-label">Produto</div>
                    <div class="item-value">{identity["product_name"]}</div>
                </div>
                <div class="identity-item">
                    <div class="item-label">Local</div>
                    <div class="item-value">{identity["location"]}</div>
                </div>
                <div class="identity-item">
                    <div class="item-label">Base usada</div>
                    <div class="item-value">Planilha de gestao preenchida pela propria fazenda</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with identity_cols[1]:
    st.markdown(
        f"""
        <div class="editorial-card dark glow">
            <div class="editorial-kicker">Jeito da operacao</div>
            <div class="editorial-title">Producao artesanal, tocada com rotina e venda bem definida.</div>
            <div class="editorial-copy">
                Antes de falar de conta e grafico, faz mais sentido mostrar com clareza
                o que a fazenda produz e para onde esse queijo vai.
            </div>
            <div class="signal-grid">
                <div class="signal-tile">
                    <div class="signal-tile-label">Produto</div>
                    <div class="signal-tile-value">Artesanal</div>
                </div>
                <div class="signal-tile">
                    <div class="signal-tile-label">Destino</div>
                    <div class="signal-tile-value">Cooperativa</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

section_header(
    "Producao",
    "Aqui ficam os numeros da lida do dia a dia: quantos dias produz, quanto sai e quanto isso vira no mes.",
)

st.markdown('<div class="section-ribbon"><div class="section-index">Bloco 2</div></div>', unsafe_allow_html=True)

production_cols = st.columns(4)
with production_cols[0]:
    kpi_card("Dias por semana", fmt["number"](production["dias_semana"], suffix=" dias"), "Ritmo de operacao")
with production_cols[1]:
    kpi_card("Queijos por dia", fmt["number"](production["queijos_dia"], suffix=" un."), "Saida diaria")
with production_cols[2]:
    kpi_card("Queijos por semana", fmt["number"](production["queijos_semana"], suffix=" un."), "Escala semanal")
with production_cols[3]:
    kpi_card("Kg por mes", fmt["number"](production["kg_mes"], decimals=1, suffix=" kg"), "Volume atual")

st.markdown(
    f"""
    <div class="signal-strip">
        <div class="signal-panel">
            <div class="signal-panel-label">Peso medio</div>
            <div class="signal-panel-value">{fmt["number"](production["peso_medio_kg"], decimals=1, suffix=" kg")}</div>
            <div class="signal-panel-copy">Peso medio de cada queijo, do jeito que esta anotado hoje.</div>
        </div>
        <div class="signal-panel">
            <div class="signal-panel-label">Total no mes</div>
            <div class="signal-panel-value">{fmt["number"](production["queijos_mes"], suffix=" un.")}</div>
            <div class="signal-panel-copy">Quanto a producao fecha no mes pela conta da planilha.</div>
        </div>
        <div class="signal-panel">
            <div class="signal-panel-label">Como foi escrito</div>
            <div class="signal-panel-value">{production["queijos_dia_text"] or "Nao mapeado"}</div>
            <div class="signal-panel-copy">A resposta aparece do mesmo jeito que foi colocada na base.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

production_detail_cols = st.columns([0.92, 1.08])
with production_detail_cols[0]:
    st.markdown(
        f"""
        <div class="editorial-card dark">
            <div class="editorial-kicker">Ritmo da producao</div>
            <div class="editorial-title">A fazenda ja mostra uma rotina bem clara de producao.</div>
            <div class="editorial-copy">
                So com esses dados ja da para entender bem a lida:
                quantos dias trabalha, quanto sai por dia e o tamanho dessa producao no mes.
            </div>
            <div class="detail-list">
                <div class="detail-item">
                    <div class="item-label">Dias de producao</div>
                    <div class="item-value">{production["dias_semana_text"] or "Nao mapeado"}</div>
                </div>
                <div class="detail-item">
                    <div class="item-label">Peso por unidade</div>
                    <div class="item-value">{production["peso_medio_kg_text"] or "Nao mapeado"}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with production_detail_cols[1]:
    st.markdown(
        f"""
        <div class="editorial-card glow">
            <div class="editorial-kicker">Fechamento do mes</div>
            <div class="editorial-title">{fmt["number"](production["queijos_mes"], suffix=" queijos por mes")}</div>
            <div class="editorial-copy">
                Esse numero junta a conta toda e mostra de forma simples
                quanto a fazenda produz no mes.
            </div>
            <div class="identity-stack">
                <div class="identity-item">
                    <div class="item-label">Queijos por semana</div>
                    <div class="item-value">{production["queijos_semana_text"] or "Nao mapeado"}</div>
                </div>
                <div class="identity-item">
                    <div class="item-label">Volume mensal</div>
                    <div class="item-value">{production["kg_mes_text"] or "Nao mapeado"}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

section_header(
    "Comercial",
    "Por fim, aqui fica a parte da venda: quanto estao pagando e quanto isso rende no mes.",
)

st.markdown('<div class="section-ribbon"><div class="section-index">Bloco 3</div></div>', unsafe_allow_html=True)

commercial_cols = st.columns(4)
with commercial_cols[0]:
    kpi_card("Preco por kg", fmt["currency"](commercial["preco_kg"]), "Valor praticado")
with commercial_cols[1]:
    kpi_card("Receita bruta", fmt["currency"](commercial["receita_bruta"]), "Mes atual")
with commercial_cols[2]:
    kpi_card("Canal principal", commercial["canal"], "Escoamento atual")
with commercial_cols[3]:
    kpi_card("Venda para cooperativa", fmt["percent"](commercial["pct_cooperativa"]), "Participacao")

commercial_detail_cols = st.columns([1.05, 0.95])
with commercial_detail_cols[0]:
    st.markdown(
        f"""
        <div class="editorial-card glow">
            <div class="editorial-kicker">Dinheiro da venda</div>
            <div class="editorial-title">{fmt["currency"](commercial["receita_bruta"])}</div>
            <div class="editorial-copy">
                Aqui fica mais facil enxergar o valor bruto que entra no mes,
                junto com o preco pago no quilo do queijo.
            </div>
            <div class="identity-stack">
                <div class="identity-item">
                    <div class="item-label">Preco pago</div>
                    <div class="item-value">{commercial["preco_kg_text"] or "Nao mapeado"}</div>
                </div>
                <div class="identity-item">
                    <div class="item-label">Para onde vai</div>
                    <div class="item-value">{commercial["pct_cooperativa_text"] or "Nao mapeado"}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with commercial_detail_cols[1]:
    st.markdown(
        f"""
        <div class="editorial-card dark glow">
            <div class="editorial-kicker">Jeito de vender</div>
            <div class="editorial-title">Hoje a venda toda vai para a cooperativa.</div>
            <div class="editorial-copy">
                Isso ajuda a entender rapido como a fazenda vende a producao
                e de onde sai esse valor mostrado acima.
            </div>
            <div class="detail-list">
                <div class="detail-item">
                    <div class="item-label">Canal principal</div>
                    <div class="item-value">{commercial["canal"]}</div>
                </div>
                <div class="detail-item">
                    <div class="item-label">Valor anotado</div>
                    <div class="item-value">{commercial["receita_bruta_text"] or "Nao mapeado"}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
