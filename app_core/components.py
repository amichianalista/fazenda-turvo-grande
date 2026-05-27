from __future__ import annotations

import base64
from functools import lru_cache
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from app_core.data import PRODUCT_IMAGE


THEME_CSS = """
<style>
    :root {
        --bg: #f4f0e8;
        --surface: #fffdf8;
        --surface-muted: #f7f1e8;
        --surface-dark: #123326;
        --surface-dark-soft: #1a4735;
        --text: #17231c;
        --muted: #627063;
        --line: rgba(23, 35, 28, 0.08);
        --line-strong: rgba(255, 255, 255, 0.12);
        --green: #173e2d;
        --green-soft: #2c6b4b;
        --amber: #b98433;
        --sand: #d8c2a4;
        --danger: #8d4b2f;
        --shadow: 0 16px 40px rgba(18, 40, 28, 0.08);
        --display-font: "Palatino Linotype", "Book Antiqua", Palatino, serif;
        --body-font: "Segoe UI", "Trebuchet MS", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(214, 191, 151, 0.14), transparent 28%),
            radial-gradient(circle at top right, rgba(32, 94, 66, 0.06), transparent 24%),
            linear-gradient(180deg, #f7f3eb 0%, #f3eee5 100%);
        color: var(--text);
        font-family: var(--body-font);
    }

    .block-container {
        max-width: 1240px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #183b2c 0%, #10271e 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    [data-testid="stSidebar"] * {
        color: #f6f1e7;
    }

    [data-testid="stSidebarNavLink"] {
        border-radius: 14px;
        margin-bottom: 0.3rem;
    }

    [data-testid="stSidebarNavLink"][aria-current="page"] {
        background: rgba(255, 255, 255, 0.10);
    }

    .sidebar-shell {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        margin-bottom: 1rem;
        padding: 1rem 1rem 1.1rem 1rem;
    }

    .sidebar-kicker {
        color: #e4c78f;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .sidebar-title {
        color: #fff8ec;
        font-family: var(--display-font);
        font-size: 1.3rem;
        font-weight: 700;
        line-height: 1.02;
        margin-top: 0.55rem;
    }

    .sidebar-copy {
        color: rgba(255, 248, 236, 0.78);
        font-size: 0.92rem;
        line-height: 1.58;
        margin-top: 0.7rem;
    }

    .source-note {
        color: var(--muted);
        font-size: 0.86rem;
        line-height: 1.55;
        margin-top: 0.75rem;
    }

    .topline {
        align-items: center;
        color: var(--muted);
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        font-size: 0.84rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }

    .topline-dot {
        color: #9a8f7c;
    }

    .hero-panel {
        background:
            linear-gradient(140deg, rgba(15, 39, 29, 0.98), rgba(23, 62, 45, 0.96)),
            linear-gradient(90deg, rgba(185, 132, 51, 0.12), transparent 35%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 30px;
        box-shadow: 0 24px 60px rgba(13, 33, 23, 0.18);
        margin-bottom: 1.3rem;
        overflow: hidden;
        padding: 1.9rem 1.9rem 2rem 1.9rem;
        position: relative;
    }

    .hero-panel::after {
        background: radial-gradient(circle at top right, rgba(230, 193, 125, 0.18), transparent 24%);
        content: "";
        inset: 0;
        pointer-events: none;
        position: absolute;
    }

    .hero-grid {
        display: grid;
        gap: 1.25rem;
        grid-template-columns: minmax(0, 1.55fr) minmax(280px, 0.95fr);
        position: relative;
        z-index: 1;
    }

    .hero-kicker {
        color: #e7cb92;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.18em;
        text-transform: uppercase;
    }

    .hero-title {
        color: #fff9ef;
        font-family: var(--display-font);
        font-size: clamp(2.4rem, 4.5vw, 4rem);
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 0.94;
        margin-top: 0.8rem;
        max-width: 740px;
    }

    .hero-copy {
        color: rgba(255, 249, 239, 0.82);
        font-size: 1rem;
        line-height: 1.72;
        margin-top: 0.9rem;
        max-width: 720px;
    }

    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-top: 1rem;
    }

    .badge-pill {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 999px;
        color: #fff6e8;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 0.46rem 0.72rem;
    }

    .hero-stats {
        display: grid;
        gap: 0.85rem;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        margin-top: 1.3rem;
    }

    .hero-stat {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 0.85rem 0.9rem 0.9rem 0.9rem;
    }

    .hero-stat-label {
        color: rgba(231, 203, 146, 0.88);
        font-size: 0.74rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .hero-stat-value {
        color: #fff9ef;
        font-family: var(--display-font);
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1;
        margin-top: 0.45rem;
    }

    .hero-stat-note {
        color: rgba(255, 249, 239, 0.72);
        font-size: 0.9rem;
        line-height: 1.45;
        margin-top: 0.35rem;
    }

    .hero-aside {
        display: grid;
        gap: 0.9rem;
        grid-template-rows: auto 1fr;
    }

    .hero-image-card,
    .hero-note-card {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        overflow: hidden;
    }

    .hero-image-card img {
        display: block;
        height: 100%;
        max-height: 330px;
        object-fit: cover;
        width: 100%;
    }

    .hero-note-card {
        padding: 1rem 1rem 1.05rem 1rem;
    }

    .hero-note-label {
        color: rgba(231, 203, 146, 0.88);
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    .hero-note-title {
        color: #fff9ef;
        font-family: var(--display-font);
        font-size: 1.22rem;
        font-weight: 700;
        line-height: 1.08;
        margin-top: 0.55rem;
    }

    .hero-note-copy {
        color: rgba(255, 249, 239, 0.76);
        font-size: 0.94rem;
        line-height: 1.62;
        margin-top: 0.55rem;
    }

    .section-shell {
        margin: 1.6rem 0 0.85rem 0;
    }

    .section-eyebrow {
        color: var(--amber);
        font-size: 0.74rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .section-title {
        color: var(--text);
        font-family: var(--display-font);
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.02;
        margin-top: 0.45rem;
    }

    .section-copy {
        color: var(--muted);
        font-size: 0.98rem;
        line-height: 1.72;
        margin-top: 0.55rem;
        max-width: 780px;
    }

    .metric-card,
    .info-card,
    .list-card {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 24px;
        box-shadow: var(--shadow);
        height: 100%;
        overflow: hidden;
        padding: 1.2rem 1.2rem 1.15rem 1.2rem;
    }

    .metric-card {
        position: relative;
    }

    .metric-card::before {
        background: linear-gradient(90deg, var(--green-soft), var(--amber));
        content: "";
        height: 4px;
        left: 0;
        position: absolute;
        right: 0;
        top: 0;
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.74rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .metric-value {
        color: var(--text);
        font-family: var(--display-font);
        font-size: clamp(1.7rem, 2.2vw, 2.3rem);
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1;
        margin-top: 0.65rem;
        overflow-wrap: anywhere;
    }

    .metric-note {
        color: var(--green-soft);
        font-size: 0.9rem;
        font-weight: 700;
        line-height: 1.5;
        margin-top: 0.55rem;
    }

    .info-card.dark {
        background: linear-gradient(160deg, #153728 0%, #1d4a37 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 16px 40px rgba(13, 33, 23, 0.14);
    }

    .info-kicker {
        color: var(--muted);
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .info-card.dark .info-kicker {
        color: #e4c78f;
    }

    .info-title {
        color: var(--text);
        font-family: var(--display-font);
        font-size: 1.45rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.06;
        margin-top: 0.6rem;
    }

    .info-card.dark .info-title {
        color: #fff8eb;
    }

    .info-copy {
        color: var(--muted);
        font-size: 0.95rem;
        line-height: 1.68;
        margin-top: 0.6rem;
    }

    .info-card.dark .info-copy {
        color: rgba(255, 248, 235, 0.78);
    }

    .list-card-title {
        color: var(--text);
        font-family: var(--display-font);
        font-size: 1.32rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        line-height: 1.08;
    }

    .list-card-copy {
        color: var(--muted);
        font-size: 0.95rem;
        line-height: 1.62;
        margin-top: 0.45rem;
    }

    .list-rows {
        display: grid;
        gap: 0.8rem;
        margin-top: 0.95rem;
    }

    .list-row {
        border-top: 1px solid var(--line);
        padding-top: 0.8rem;
    }

    .list-row-label {
        color: var(--muted);
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .list-row-value {
        color: var(--text);
        font-size: 1rem;
        font-weight: 700;
        line-height: 1.55;
        margin-top: 0.22rem;
    }

    .mini-callout {
        background: var(--surface-muted);
        border: 1px solid var(--line);
        border-radius: 18px;
        color: var(--text);
        font-size: 0.92rem;
        line-height: 1.58;
        margin-top: 0.9rem;
        padding: 0.85rem 0.9rem;
    }

    @media (max-width: 1100px) {
        .hero-grid {
            grid-template-columns: 1fr;
        }

        .hero-stats {
            grid-template-columns: 1fr;
        }
    }
</style>
"""


@lru_cache(maxsize=8)
def _image_data_uri(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        return ""
    encoded = base64.b64encode(file_path.read_bytes()).decode("ascii")
    suffix = file_path.suffix.lower().replace(".", "") or "png"
    return f"data:image/{suffix};base64,{encoded}"


def apply_theme(page_title: str, page_icon: str) -> None:
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def sidebar_context(page_title: str, page_copy: str) -> None:
    st.sidebar.markdown(
        f"""
        <div class="sidebar-shell">
            <div class="sidebar-kicker">Turvo Grande</div>
            <div class="sidebar-title">{page_title}</div>
            <div class="sidebar-copy">{page_copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.caption("Base operacional: planilha de gestao da fazenda.")
    st.sidebar.caption("Contexto de mercado: estudo estrategico em PDF, maio de 2026.")


def topline(items: list[str]) -> None:
    parts = []
    for index, item in enumerate(items):
        parts.append(f"<span>{item}</span>")
        if index < len(items) - 1:
            parts.append('<span class="topline-dot">•</span>')
    st.markdown(f'<div class="topline">{"".join(parts)}</div>', unsafe_allow_html=True)


def hero_panel(
    kicker: str,
    title: str,
    copy: str,
    badges: list[str],
    stats: list[dict[str, str]],
    note_title: str,
    note_copy: str,
    image_path: Path | None = PRODUCT_IMAGE,
) -> None:
    badge_html = "".join(f'<span class="badge-pill">{badge}</span>' for badge in badges)
    stats_html = "".join(
        f"""
        <div class="hero-stat">
            <div class="hero-stat-label">{item['label']}</div>
            <div class="hero-stat-value">{item['value']}</div>
            <div class="hero-stat-note">{item['note']}</div>
        </div>
        """
        for item in stats
    )

    image_html = ""
    if image_path is not None:
        image_uri = _image_data_uri(str(image_path))
        if image_uri:
            image_html = f'<div class="hero-image-card"><img src="{image_uri}" alt="Queijo Turvo Grande"></div>'

    st.markdown(
        f"""
        <div class="hero-panel">
            <div class="hero-grid">
                <div>
                    <div class="hero-kicker">{kicker}</div>
                    <div class="hero-title">{title}</div>
                    <div class="hero-copy">{copy}</div>
                    <div class="badge-row">{badge_html}</div>
                    <div class="hero-stats">{stats_html}</div>
                </div>
                <div class="hero-aside">
                    {image_html}
                    <div class="hero-note-card">
                        <div class="hero-note-label">Leitura da vez</div>
                        <div class="hero-note-title">{note_title}</div>
                        <div class="hero-note-copy">{note_copy}</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(eyebrow: str, title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="section-shell">
            <div class="section-eyebrow">{eyebrow}</div>
            <div class="section-title">{title}</div>
            <div class="section-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, note: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(kicker: str, title: str, copy: str, tone: str = "light") -> None:
    class_name = "info-card dark" if tone == "dark" else "info-card"
    st.markdown(
        f"""
        <div class="{class_name}">
            <div class="info-kicker">{kicker}</div>
            <div class="info-title">{title}</div>
            <div class="info-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def list_card(title: str, copy: str, rows: list[dict[str, str]], callout: str | None = None) -> None:
    rows_html = "".join(
        f"""
        <div class="list-row">
            <div class="list-row-label">{row['label']}</div>
            <div class="list-row-value">{row['value']}</div>
        </div>
        """
        for row in rows
    )
    callout_html = f'<div class="mini-callout">{callout}</div>' if callout else ""
    st.markdown(
        f"""
        <div class="list-card">
            <div class="list-card-title">{title}</div>
            <div class="list-card-copy">{copy}</div>
            <div class="list-rows">{rows_html}</div>
            {callout_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def source_note(copy: str) -> None:
    st.markdown(f'<div class="source-note">{copy}</div>', unsafe_allow_html=True)


def chart_style(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        font={"family": "Segoe UI, Trebuchet MS, sans-serif", "color": "#17231c"},
        paper_bgcolor="#fffdf8",
        plot_bgcolor="#fffdf8",
        margin={"l": 24, "r": 24, "t": 28, "b": 24},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "x": 0},
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="rgba(23, 35, 28, 0.08)")
    fig.update_yaxes(gridcolor="rgba(23, 35, 28, 0.08)", zeroline=False)
    return fig
