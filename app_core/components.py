from __future__ import annotations

import base64
from functools import lru_cache
from pathlib import Path

import streamlit as st


THEME_CSS = """
<style>
    :root {
        --bg: #f6f0e6;
        --surface: rgba(255, 250, 243, 0.80);
        --surface-strong: rgba(255, 250, 243, 0.92);
        --text: #192317;
        --muted: #5d695b;
        --green: #173e2d;
        --green-soft: #2f6c4d;
        --amber: #c79a46;
        --earth: #8f6338;
        --slate: #314844;
        --line: rgba(31, 42, 31, 0.10);
        --line-strong: rgba(255, 245, 228, 0.18);
        --shadow: 0 24px 60px rgba(10, 23, 15, 0.16);
        --shadow-soft: 0 18px 42px rgba(8, 18, 12, 0.12);
        --display-font: "Palatino Linotype", "Book Antiqua", Palatino, serif;
        --body-font: "Trebuchet MS", "Segoe UI", sans-serif;
    }

    .stApp {
        background:
            linear-gradient(180deg, rgba(6, 18, 11, 0.48) 0%, rgba(8, 20, 13, 0.40) 100%),
            radial-gradient(circle at top right, rgba(200, 141, 45, 0.20), transparent 24%),
            radial-gradient(circle at left 12%, rgba(31, 92, 63, 0.18), transparent 26%),
            var(--app-bg-image);
        background-attachment: fixed;
        background-position: center center;
        background-repeat: no-repeat;
        background-size: cover;
        color: var(--text);
        font-family: var(--body-font);
    }

    .block-container {
        padding-top: 2.4rem;
        padding-bottom: 3.6rem;
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
            linear-gradient(125deg, rgba(12, 34, 24, 0.68), rgba(23, 58, 40, 0.56) 48%, rgba(121, 89, 33, 0.12) 100%);
        backdrop-filter: blur(8px);
        border: 1px solid var(--line-strong);
        border-radius: 34px;
        box-shadow: 0 28px 80px rgba(7, 16, 11, 0.28);
        margin-bottom: 1.6rem;
        min-height: 320px;
        overflow: hidden;
        padding: 2.3rem 2.3rem 2.5rem 2.3rem;
        position: relative;
    }

    .hero-shell::before {
        background:
            radial-gradient(circle at 85% 20%, rgba(219, 183, 98, 0.34), transparent 24%),
            radial-gradient(circle at 12% 110%, rgba(255, 255, 255, 0.08), transparent 22%);
        content: "";
        inset: 0;
        pointer-events: none;
        position: absolute;
    }

    .hero-shell::after {
        background:
            linear-gradient(90deg, rgba(200, 141, 45, 0.14), transparent 32%),
            linear-gradient(180deg, rgba(255, 255, 255, 0.05), transparent 26%);
        content: "";
        inset: 0;
        pointer-events: none;
        position: absolute;
    }

    .hero-kicker {
        color: #f6d9a1;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.24em;
        margin-bottom: 0.95rem;
        position: relative;
        text-transform: uppercase;
        z-index: 1;
    }

    .hero-title {
        color: #fff8f0;
        font-family: var(--display-font);
        font-size: clamp(2.7rem, 5vw, 4.5rem);
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 0.95;
        margin: 0;
        max-width: 820px;
        position: relative;
        z-index: 1;
    }

    .hero-copy {
        color: rgba(255, 248, 240, 0.84);
        font-size: 1.04rem;
        line-height: 1.75;
        margin-top: 1rem;
        max-width: 720px;
        position: relative;
        z-index: 1;
    }

    .section-shell {
        margin: 1.5rem 0 0.95rem 0;
    }

    .section-title {
        color: var(--text);
        font-family: var(--display-font);
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.28rem;
    }

    .section-copy {
        color: var(--muted);
        font-size: 0.98rem;
        line-height: 1.68;
        max-width: 760px;
    }

    .kpi-shell {
        background: linear-gradient(180deg, rgba(255, 251, 246, 0.62), rgba(249, 242, 232, 0.42));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 24px;
        box-shadow: 0 14px 34px rgba(8, 18, 12, 0.10);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 164px;
        overflow: hidden;
        padding: 1.28rem 1.2rem 1.12rem 1.2rem;
        position: relative;
    }

    .kpi-shell::before {
        background: linear-gradient(90deg, rgba(47, 108, 77, 0.96), rgba(199, 154, 70, 0.72));
        content: "";
        height: 4px;
        left: 0;
        position: absolute;
        right: 0;
        top: 0;
    }

    .kpi-label {
        color: var(--muted);
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .kpi-value {
        color: var(--text);
        font-family: var(--display-font);
        font-size: clamp(2rem, 2.4vw, 2.5rem);
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 0.98;
        margin: 0.72rem 0 0.42rem 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .kpi-value-compact {
        font-size: clamp(1.7rem, 2vw, 2.05rem);
    }

    .kpi-value-tight {
        font-size: clamp(1.42rem, 1.7vw, 1.72rem);
        line-height: 1.04;
    }

    .kpi-delta {
        color: var(--green-soft);
        font-size: 0.88rem;
        font-weight: 700;
        line-height: 1.5;
    }

    .panel-shell {
        background: linear-gradient(180deg, rgba(255, 250, 243, 0.68), rgba(249, 243, 235, 0.48));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 24px;
        box-shadow: 0 14px 34px rgba(8, 18, 12, 0.10);
        margin-bottom: 1rem;
        padding: 1.3rem;
    }

    .panel-kicker {
        color: var(--muted);
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        margin-bottom: 0.65rem;
        text-transform: uppercase;
    }

    .panel-title {
        color: var(--text);
        font-family: var(--display-font);
        font-size: 1.32rem;
        font-weight: 800;
        line-height: 1.08;
        margin-bottom: 0.42rem;
    }

    .panel-copy {
        color: var(--muted);
        font-size: 0.97rem;
        line-height: 1.72;
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
        background: rgba(255, 250, 243, 0.62);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 18px;
        box-shadow: 0 14px 34px rgba(8, 18, 12, 0.10);
        color: var(--text);
        font-size: 0.95rem;
        font-weight: 600;
        padding: 0.95rem 1rem;
    }

    @media (max-width: 900px) {
        .hero-shell {
            min-height: auto;
            padding: 1.8rem 1.3rem 2rem 1.3rem;
        }

        .section-title {
            font-size: 1.55rem;
        }
    }
</style>
"""


ROOT_DIR = Path(__file__).resolve().parents[1]
BACKGROUND_IMAGE = ROOT_DIR / "assets" / "background.png"


@lru_cache(maxsize=1)
def _background_data_uri() -> str:
    if not BACKGROUND_IMAGE.exists():
        return "none"
    encoded = base64.b64encode(BACKGROUND_IMAGE.read_bytes()).decode("ascii")
    return f'url("data:image/png;base64,{encoded}")'


def apply_theme(page_title: str, page_icon: str) -> None:
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    themed_css = THEME_CSS.replace("var(--app-bg-image)", _background_data_uri())
    st.markdown(themed_css, unsafe_allow_html=True)


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
    value_length = len(value)
    value_class = "kpi-value"
    if value_length > 10:
        value_class += " kpi-value-compact"
    if value_length > 16:
        value_class += " kpi-value-tight"

    st.markdown(
        f"""
        <div class="kpi-shell">
            <div class="kpi-label">{label}</div>
            <div class="{value_class}">{value}</div>
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
