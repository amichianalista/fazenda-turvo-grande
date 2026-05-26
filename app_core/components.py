from __future__ import annotations

import streamlit as st


THEME_CSS = """
<style>
    :root {
        --bg: #f6f0e6;
        --surface: rgba(255, 250, 243, 0.78);
        --surface-strong: #fffaf2;
        --text: #1f2a1f;
        --muted: #586357;
        --green: #1f5c3f;
        --green-soft: #2d7a54;
        --amber: #c88d2d;
        --earth: #8a5a34;
        --slate: #334e4a;
        --line: rgba(31, 42, 31, 0.08);
        --shadow: 0 24px 60px rgba(31, 42, 31, 0.10);
    }

    .stApp {
        background:
            radial-gradient(circle at top right, rgba(200, 141, 45, 0.22), transparent 20%),
            radial-gradient(circle at left 15%, rgba(31, 92, 63, 0.16), transparent 22%),
            linear-gradient(180deg, #f7f2e8 0%, #f2ecdf 100%);
        color: var(--text);
    }

    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1220px;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #214c38 0%, #183528 100%);
    }

    [data-testid="stSidebar"] * {
        color: #f8f2e9;
    }

    .hero-shell {
        background:
            linear-gradient(135deg, rgba(19, 58, 40, 0.95), rgba(35, 93, 63, 0.92)),
            linear-gradient(180deg, rgba(200, 141, 45, 0.20), transparent);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 28px;
        box-shadow: var(--shadow);
        margin-bottom: 1.4rem;
        overflow: hidden;
        padding: 2rem 2rem 2.2rem 2rem;
        position: relative;
    }

    .hero-shell::after {
        background: linear-gradient(90deg, rgba(200, 141, 45, 0.18), transparent);
        content: "";
        inset: 0;
        pointer-events: none;
        position: absolute;
    }

    .hero-kicker {
        color: #f6d9a1;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        margin-bottom: 0.8rem;
        position: relative;
        text-transform: uppercase;
        z-index: 1;
    }

    .hero-title {
        color: #fff8f0;
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1.03;
        margin: 0;
        max-width: 760px;
        position: relative;
        z-index: 1;
    }

    .hero-copy {
        color: rgba(255, 248, 240, 0.84);
        font-size: 1.02rem;
        line-height: 1.7;
        margin-top: 0.9rem;
        max-width: 720px;
        position: relative;
        z-index: 1;
    }

    .section-shell {
        margin: 1.35rem 0 0.85rem 0;
    }

    .section-title {
        color: var(--text);
        font-size: 1.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .section-copy {
        color: var(--muted);
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .kpi-shell {
        background: rgba(255, 250, 243, 0.88);
        backdrop-filter: blur(8px);
        border: 1px solid var(--line);
        border-radius: 22px;
        box-shadow: var(--shadow);
        min-height: 154px;
        padding: 1.2rem 1.15rem 1.05rem 1.15rem;
    }

    .kpi-label {
        color: var(--muted);
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .kpi-value {
        color: var(--text);
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.05;
        margin: 0.55rem 0 0.35rem 0;
    }

    .kpi-delta {
        color: var(--green-soft);
        font-size: 0.92rem;
        font-weight: 700;
    }

    .panel-shell {
        background: rgba(255, 250, 243, 0.86);
        border: 1px solid var(--line);
        border-radius: 24px;
        box-shadow: var(--shadow);
        margin-bottom: 1rem;
        padding: 1.25rem;
    }

    .panel-kicker {
        color: var(--muted);
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        margin-bottom: 0.65rem;
        text-transform: uppercase;
    }

    .panel-title {
        color: var(--text);
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .panel-copy {
        color: var(--muted);
        font-size: 0.94rem;
        line-height: 1.65;
        margin-bottom: 0;
    }

    .tone-green {
        border-left: 6px solid var(--green-soft);
    }

    .tone-amber {
        border-left: 6px solid var(--amber);
    }

    .tone-earth {
        border-left: 6px solid var(--earth);
    }

    .tone-slate {
        border-left: 6px solid var(--slate);
    }

    .bullet-panel {
        display: grid;
        gap: 0.8rem;
        margin-top: 0.25rem;
    }

    .bullet-item {
        background: rgba(255, 250, 243, 0.88);
        border: 1px solid var(--line);
        border-radius: 18px;
        box-shadow: var(--shadow);
        color: var(--text);
        font-size: 0.95rem;
        font-weight: 600;
        padding: 0.95rem 1rem;
    }
</style>
"""


def apply_theme(page_title: str, page_icon: str) -> None:
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def section_header(title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="section-shell">
            <div class="section-title">{title}</div>
            <div class="section-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, delta: str) -> None:
    st.markdown(
        f"""
        <div class="kpi-shell">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-delta">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_card(title: str, copy: str, tone: str = "green", kicker: str = "Estrutura") -> None:
    st.markdown(
        f"""
        <div class="panel-shell tone-{tone}">
            <div class="panel-kicker">{kicker}</div>
            <div class="panel-title">{title}</div>
            <div class="panel-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(title: str, copy: str, tone: str = "amber") -> None:
    insight_card(title=title, copy=copy, tone=tone, kicker="Base de dados")
