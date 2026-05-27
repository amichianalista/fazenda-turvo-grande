from __future__ import annotations

import base64
from functools import lru_cache
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from app_core.data import BACKGROUND_IMAGE, PRODUCT_IMAGE


@lru_cache(maxsize=8)
def _image_data_uri(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        return ""
    encoded = base64.b64encode(file_path.read_bytes()).decode("ascii")
    suffix = file_path.suffix.lower().replace(".", "") or "png"
    return f"data:image/{suffix};base64,{encoded}"


def _theme_css() -> str:
    background_uri = _image_data_uri(str(BACKGROUND_IMAGE))
    background_rule = (
        f'background-image: linear-gradient(rgba(8, 20, 12, 0.78), rgba(8, 20, 12, 0.82)), url("{background_uri}");'
        if background_uri
        else "background: linear-gradient(180deg, #102515 0%, #1b3d24 100%);"
    )

    return f"""
    <style>
        :root {{
            --paper: rgba(10, 24, 14, 0.18);
            --paper-strong: rgba(255, 251, 243, 0.10);
            --paper-soft: rgba(255, 251, 243, 0.08);
            --ink: #fff7ea;
            --muted: rgba(255, 247, 234, 0.74);
            --line: rgba(255, 255, 255, 0.12);
            --gold: #c79a47;
            --gold-soft: #e0bc79;
            --green: #214a2d;
            --green-soft: #3f7851;
            --danger: #8c5536;
            --shadow: 0 18px 34px rgba(7, 17, 10, 0.14);
            --display-font: "Georgia", "Palatino Linotype", serif;
            --body-font: "Trebuchet MS", "Segoe UI", sans-serif;
        }}

        .stApp {{
            {background_rule}
            background-attachment: fixed;
            background-position: center center;
            background-repeat: no-repeat;
            background-size: cover;
            color: var(--ink);
            font-family: var(--body-font);
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            background:
                radial-gradient(circle at 18% 18%, rgba(221, 184, 110, 0.12), transparent 28%),
                radial-gradient(circle at 82% 20%, rgba(98, 151, 95, 0.10), transparent 20%);
            pointer-events: none;
            z-index: 0;
        }}

        .block-container {{
            max-width: 1280px;
            padding-top: 1.6rem;
            padding-bottom: 3rem;
            position: relative;
            z-index: 1;
        }}

        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, rgba(15, 34, 20, 0.98), rgba(10, 23, 14, 0.98));
            border-right: 1px solid rgba(255, 255, 255, 0.06);
        }}

        [data-testid="stSidebar"] * {{
            color: #f7f2e5;
        }}

        [data-testid="stSidebarNavLink"] {{
            border-radius: 16px;
            margin-bottom: 0.3rem;
        }}

        [data-testid="stSidebarNavLink"][aria-current="page"] {{
            background: rgba(255, 255, 255, 0.10);
        }}

        .sidebar-box {{
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 22px;
            padding: 1rem 1rem 1.1rem 1rem;
            margin-bottom: 1rem;
        }}

        .sidebar-kicker {{
            color: #d9b46c;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }}

        .sidebar-title {{
            color: #fff7ea;
            font-family: var(--display-font);
            font-size: 1.3rem;
            font-weight: 700;
            line-height: 1.02;
            margin-top: 0.5rem;
        }}

        .sidebar-copy {{
            color: rgba(255, 247, 234, 0.78);
            font-size: 0.93rem;
            line-height: 1.58;
            margin-top: 0.7rem;
        }}

        .topline {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
            align-items: center;
            color: #eadcc0;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            margin-bottom: 0.95rem;
            text-transform: uppercase;
        }}

        .topline-dot {{
            color: rgba(234, 220, 192, 0.55);
        }}

        .hero-shell {{
            background: linear-gradient(145deg, rgba(9, 23, 13, 0.28), rgba(22, 48, 29, 0.18));
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 34px;
            box-shadow: 0 24px 48px rgba(7, 17, 10, 0.16);
            padding: 2rem;
            overflow: hidden;
            position: relative;
            margin-bottom: 1.2rem;
            backdrop-filter: blur(8px);
        }}

        .hero-shell::after {{
            content: "";
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at right top, rgba(214, 175, 98, 0.18), transparent 28%),
                linear-gradient(90deg, rgba(214, 175, 98, 0.08), transparent 42%);
            pointer-events: none;
        }}

        .hero-grid {{
            display: grid;
            gap: 1.2rem;
            justify-items: center;
            position: relative;
            z-index: 1;
            text-align: center;
        }}

        .hero-kicker {{
            color: #e0bc79;
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.18em;
            text-transform: uppercase;
        }}

        .hero-title {{
            color: #fff7ea;
            font-family: var(--display-font);
            font-size: clamp(2.4rem, 4.8vw, 4.2rem);
            font-weight: 800;
            line-height: 0.95;
            letter-spacing: -0.03em;
            margin-top: 0;
            max-width: 920px;
        }}

        .hero-title-card {{
            background: linear-gradient(180deg, rgba(8, 21, 12, 0.42), rgba(8, 21, 12, 0.24));
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 28px;
            box-shadow: 0 20px 40px rgba(7, 17, 10, 0.16);
            padding: 1.25rem 1.4rem 1.35rem 1.4rem;
            width: min(100%, 980px);
            backdrop-filter: blur(10px);
        }}

        .hero-copy {{
            color: rgba(255, 247, 234, 0.82);
            font-size: 1rem;
            line-height: 1.72;
            margin-top: 0.9rem;
            max-width: 860px;
        }}

        .badge-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 1rem;
            justify-content: center;
        }}

        .badge-pill {{
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.10);
            color: #fff7ea;
            font-size: 0.8rem;
            font-weight: 700;
            padding: 0.45rem 0.72rem;
        }}

        .hero-stats {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
            margin-top: 1.2rem;
            width: min(100%, 980px);
        }}

        .hero-stat {{
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 20px;
            padding: 0.9rem;
            backdrop-filter: blur(10px);
        }}

        .hero-stat-label {{
            color: rgba(224, 188, 121, 0.95);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }}

        .hero-stat-value {{
            color: #fff7ea;
            font-family: var(--display-font);
            font-size: 1.65rem;
            font-weight: 800;
            line-height: 1;
            margin-top: 0.5rem;
        }}

        .hero-stat-note {{
            color: rgba(255, 247, 234, 0.72);
            font-size: 0.9rem;
            line-height: 1.45;
            margin-top: 0.35rem;
        }}

        .hero-aside {{
            display: grid;
            gap: 0.9rem;
            align-content: start;
            width: min(100%, 780px);
        }}

        .hero-note-card {{
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 24px;
            backdrop-filter: blur(10px);
        }}

        .hero-note-card {{
            padding: 1rem;
        }}

        .hero-note-title {{
            color: #fff7ea;
            font-family: var(--display-font);
            font-size: 1.2rem;
            font-weight: 700;
            line-height: 1.08;
            margin-top: 0.4rem;
        }}

        .hero-note-copy {{
            color: rgba(255, 247, 234, 0.75);
            font-size: 0.94rem;
            line-height: 1.62;
            margin-top: 0.55rem;
        }}

        .section-block {{
            margin: 1.55rem 0 0.85rem 0;
        }}

        .section-kicker {{
            color: #e0bc79;
            font-size: 0.73rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }}

        .section-title {{
            color: #fbf7ed;
            font-family: var(--display-font);
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.02;
            letter-spacing: -0.03em;
            margin-top: 0.45rem;
        }}

        .section-copy {{
            color: rgba(251, 247, 237, 0.82);
            font-size: 0.98rem;
            line-height: 1.7;
            margin-top: 0.55rem;
            max-width: 820px;
        }}

        .metric-card,
        .insight-card,
        .note-card {{
            background: var(--paper);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 24px;
            box-shadow: var(--shadow);
            padding: 1.15rem;
            height: 100%;
            backdrop-filter: blur(10px);
        }}

        .metric-card {{
            position: relative;
            overflow: hidden;
        }}

        .metric-card::before {{
            content: "";
            position: absolute;
            left: 0;
            right: 0;
            top: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--green-soft), var(--gold));
        }}

        .metric-label {{
            color: var(--muted);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }}

        .metric-value {{
            color: var(--ink);
            font-family: var(--display-font);
            font-size: clamp(1.7rem, 2.3vw, 2.35rem);
            font-weight: 800;
            line-height: 1;
            margin-top: 0.6rem;
            overflow-wrap: anywhere;
        }}

        .metric-note {{
            color: rgba(255, 247, 234, 0.78);
            font-size: 0.92rem;
            font-weight: 700;
            line-height: 1.5;
            margin-top: 0.5rem;
        }}

        .insight-title {{
            color: var(--ink);
            font-family: var(--display-font);
            font-size: 1.3rem;
            font-weight: 800;
            line-height: 1.08;
        }}

        .insight-copy {{
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.64;
            margin-top: 0.55rem;
        }}

        .note-title {{
            color: var(--ink);
            font-family: var(--display-font);
            font-size: 1.35rem;
            font-weight: 800;
            line-height: 1.08;
        }}

        .note-copy {{
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.62;
            margin-top: 0.5rem;
        }}

        .bullet-list {{
            display: grid;
            gap: 0.75rem;
            margin-top: 0.9rem;
        }}

        .bullet-item {{
            border-top: 1px solid var(--line);
            padding-top: 0.8rem;
        }}

        .bullet-label {{
            color: var(--muted);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }}

        .bullet-value {{
            color: var(--ink);
            font-size: 0.98rem;
            font-weight: 700;
            line-height: 1.52;
            margin-top: 0.25rem;
        }}

        .source-note {{
            color: rgba(251, 247, 237, 0.78);
            font-size: 0.86rem;
            line-height: 1.55;
            margin-top: 1rem;
        }}

        div[data-testid="stPlotlyChart"] {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 24px;
            box-shadow: var(--shadow);
            padding: 0.35rem;
            backdrop-filter: blur(8px);
        }}

        @media (max-width: 1100px) {{
            .hero-stats {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
    """


def apply_theme(page_title: str, page_icon: str) -> None:
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(_theme_css(), unsafe_allow_html=True)


def sidebar_context(page_title: str, page_copy: str) -> None:
    st.sidebar.markdown(
        f"""
        <div class="sidebar-box">
            <div class="sidebar-kicker">Turvo Grande</div>
            <div class="sidebar-title">{page_title}</div>
            <div class="sidebar-copy">{page_copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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

    st.markdown(
        f"""
        <div class="hero-shell">
            <div class="hero-grid">
                <div>
                    <div class="hero-kicker">{kicker}</div>
                    <div class="hero-title-card">
                        <div class="hero-title">{title}</div>
                    </div>
                    <div class="hero-copy">{copy}</div>
                    <div class="badge-row">{badge_html}</div>
                    <div class="hero-stats">{stats_html}</div>
                </div>
                <div class="hero-aside">
                    <div class="hero-note-card">
                        <div class="hero-kicker">Leitura do produtor</div>
                        <div class="hero-note-title">{note_title}</div>
                        <div class="hero-note-copy">{note_copy}</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(kicker: str, title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="section-block">
            <div class="section-kicker">{kicker}</div>
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


def insight_card(title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">{title}</div>
            <div class="insight-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def note_card(title: str, copy: str, rows: list[dict[str, str]] | None = None) -> None:
    rows_html = ""
    if rows:
        items = "".join(
            f"""
            <div class="bullet-item">
                <div class="bullet-label">{row['label']}</div>
                <div class="bullet-value">{row['value']}</div>
            </div>
            """
            for row in rows
        )
        rows_html = f'<div class="bullet-list">{items}</div>'

    st.markdown(
        f"""
        <div class="note-card">
            <div class="note-title">{title}</div>
            <div class="note-copy">{copy}</div>
            {rows_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def source_note(copy: str) -> None:
    st.markdown(f'<div class="source-note">{copy}</div>', unsafe_allow_html=True)


def chart_style(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        font={"family": "Trebuchet MS, Segoe UI, sans-serif", "color": "#fff7ea"},
        title_font={"color": "#fff7ea"},
        paper_bgcolor="rgba(255,251,243,0)",
        plot_bgcolor="rgba(255,251,243,0)",
        margin={"l": 26, "r": 26, "t": 54, "b": 24},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "x": 0},
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="rgba(255,255,255,0.10)",
        tickfont={"color": "#fff7ea"},
        title_font={"color": "#fff7ea"},
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.10)",
        zeroline=False,
        tickfont={"color": "#fff7ea"},
        title_font={"color": "#fff7ea"},
    )
    return fig
