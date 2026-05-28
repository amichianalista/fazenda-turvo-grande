from __future__ import annotations

import base64
from functools import lru_cache
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from app_core.data import BACKGROUND_IMAGE

PAGE_NAV_ITEMS = [
    {"path": "pages/1_Visao_Executiva.py", "label": "Pagina 1", "title": "Visão Executiva"},
    {"path": "pages/2_Producao.py", "label": "Pagina 2", "title": "Produção"},
    {"path": "pages/3_Custos.py", "label": "Pagina 3", "title": "Custos"},
    {"path": "pages/4_Mao_de_Obra.py", "label": "Pagina 4", "title": "Mão de Obra"},
    {"path": "pages/5_Resultado_Financeiro.py", "label": "Pagina 5", "title": "Financeiro"},
    {"path": "pages/6_Comercial.py", "label": "Pagina 6", "title": "Comercial"},
]


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
        f'background-image: linear-gradient(rgba(8, 20, 12, 0.34), rgba(8, 20, 12, 0.42)), url("{background_uri}");'
        if background_uri
        else "background: linear-gradient(180deg, #102515 0%, #1b3d24 100%);"
    )

    return f"""
    <style>
        :root {{
            --paper: rgba(10, 24, 14, 0.10);
            --paper-strong: rgba(255, 251, 243, 0.08);
            --paper-soft: rgba(255, 251, 243, 0.06);
            --ink: #fff7ea;
            --muted: rgba(255, 247, 234, 0.78);
            --line: rgba(255, 255, 255, 0.12);
            --gold: #c79a47;
            --green-soft: #3f7851;
            --shadow: 0 12px 22px rgba(7, 17, 10, 0.08);
            --glass-highlight: inset 0 1px 0 rgba(255, 255, 255, 0.10);
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
                radial-gradient(circle at 18% 18%, rgba(221, 184, 110, 0.08), transparent 34%),
                radial-gradient(circle at 82% 20%, rgba(98, 151, 95, 0.06), transparent 24%),
                linear-gradient(180deg, rgba(8, 20, 12, 0.02), rgba(8, 20, 12, 0.08));
            pointer-events: none;
            z-index: 0;
        }}

        .block-container {{
            max-width: 1280px;
            padding-top: 10rem;
            padding-bottom: 3rem;
            position: relative;
            z-index: 1;
        }}

        [data-testid="stSidebar"] {{
            display: none;
        }}

        [data-testid="stSidebarCollapsedControl"] {{
            display: none;
        }}

        .st-key-page_nav_shell {{
            position: fixed;
            top: 3.85rem;
            left: 0;
            right: 0;
            z-index: 1000;
            width: min(100%, 760px);
            margin: 0 auto;
            padding: 0 0.75rem;
        }}

        .st-key-page_nav_shell > div {{
            background: rgba(9, 23, 13, 0.66);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 22px;
            padding: 0.8rem 0.95rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 16px 28px rgba(7, 17, 10, 0.14), var(--glass-highlight);
        }}

        .page-nav-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.8rem;
        }}

        .page-nav-kicker {{
            color: #d9b46c;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            padding: 0 0.2rem;
            white-space: nowrap;
        }}

        .st-key-page_nav_shell [data-testid="stSelectbox"] {{
            min-width: 0;
            margin-top: 0.08rem;
        }}

        .st-key-page_nav_shell [data-baseweb="select"] > div {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            min-height: 3.15rem;
            transition: background 0.18s ease, border-color 0.18s ease, transform 0.18s ease;
        }}

        .st-key-page_nav_shell [data-baseweb="select"] > div:hover {{
            transform: translateY(-1px);
            border-color: rgba(255, 255, 255, 0.16);
        }}

        .st-key-page_nav_shell [data-baseweb="select"] span {{
            color: #fff7ea;
        }}

        .st-key-page_nav_shell [data-baseweb="select"] [data-testid="stMarkdownContainer"] p,
        .st-key-page_nav_shell [data-baseweb="select"] div[role="combobox"] > div,
        .st-key-page_nav_shell [data-baseweb="select"] div[role="combobox"] {{
            color: #fff7ea !important;
        }}

        .st-key-page_nav_shell [data-baseweb="select"] input {{
            color: #fff7ea !important;
            font-family: var(--display-font);
            font-size: clamp(0.98rem, 1.5vw, 1.08rem);
            font-weight: 800;
        }}

        .st-key-page_nav_shell [data-baseweb="popover"] {{
            border-radius: 18px;
            overflow: hidden;
        }}

        .st-key-page_nav_shell [data-baseweb="popover"] > div {{
            background: rgba(9, 23, 13, 0.96) !important;
        }}

        .st-key-page_nav_shell [role="listbox"] {{
            background: rgba(9, 23, 13, 0.96) !important;
            border: 1px solid rgba(255, 255, 255, 0.10);
            color: #fff7ea !important;
        }}

        .st-key-page_nav_shell [role="option"] {{
            background: transparent !important;
            color: #fff7ea !important;
            font-family: var(--body-font);
            font-weight: 800 !important;
        }}

        .st-key-page_nav_shell [role="option"] * {{
            color: #fff7ea !important;
            font-weight: 800 !important;
        }}

        .st-key-page_nav_shell [role="option"]:hover {{
            background: rgba(255, 255, 255, 0.06) !important;
        }}

        .st-key-page_nav_shell [role="option"][aria-selected="true"] {{
            background: linear-gradient(90deg, rgba(48, 100, 64, 0.95), rgba(199, 154, 71, 0.58));
            color: #fff7ea !important;
        }}

        .form-intro {{
            background: linear-gradient(145deg, rgba(9, 23, 13, 0.12), rgba(22, 48, 29, 0.06));
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 30px;
            box-shadow: 0 14px 26px rgba(7, 17, 10, 0.09), var(--glass-highlight);
            padding: 1.6rem 1.65rem;
            margin-bottom: 1.25rem;
            backdrop-filter: blur(5px);
            position: relative;
            overflow: hidden;
        }}

        .form-intro::after {{
            content: "";
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at right top, rgba(214, 175, 98, 0.12), transparent 30%),
                linear-gradient(90deg, rgba(214, 175, 98, 0.05), transparent 46%);
            pointer-events: none;
        }}

        .form-intro > * {{
            position: relative;
            z-index: 1;
        }}

        .form-intro-kicker {{
            color: #e0bc79;
            font-size: 0.74rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }}

        .form-intro-title {{
            color: #fff7ea;
            font-family: var(--display-font);
            font-size: clamp(2rem, 4vw, 3.1rem);
            font-weight: 800;
            line-height: 0.98;
            margin-top: 0.55rem;
            max-width: 860px;
        }}

        .form-intro-copy {{
            color: rgba(255, 247, 234, 0.82);
            font-size: 0.97rem;
            line-height: 1.7;
            margin-top: 0.8rem;
            max-width: 860px;
        }}

        .form-intro-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 1rem;
        }}

        .form-intro-tag {{
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.10);
            color: #fff7ea;
            font-size: 0.8rem;
            font-weight: 700;
            padding: 0.42rem 0.7rem;
        }}

        div[data-testid="stForm"] {{
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 28px;
            padding: 1.35rem 1.35rem 0.9rem 1.35rem;
            margin-bottom: 1.1rem;
            box-shadow: var(--shadow), var(--glass-highlight);
            backdrop-filter: blur(5px);
        }}

        div[data-testid="stForm"] [data-testid="stHorizontalBlock"] {{
            gap: 1.35rem;
            align-items: flex-start;
        }}

        div[data-testid="stForm"] [data-testid="column"] {{
            gap: 0.25rem;
        }}

        div[data-testid="stForm"] h3 {{
            margin-top: 1.45rem;
            margin-bottom: 1rem;
        }}

        div[data-testid="stForm"] h3:first-of-type {{
            margin-top: 0.2rem;
        }}

        div[data-testid="stForm"] [data-testid="stMarkdownContainer"] p,
        div[data-testid="stForm"] label p {{
            color: #fff7ea;
        }}

        div[data-testid="stForm"] div[data-testid="stTextInput"],
        div[data-testid="stForm"] div[data-testid="stTextArea"] {{
            margin-bottom: 0.95rem;
        }}

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea {{
            background: rgba(255, 251, 243, 0.07) !important;
            color: #fff7ea !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 16px !important;
        }}

        div[data-testid="stTextInput"] input::placeholder,
        div[data-testid="stTextArea"] textarea::placeholder {{
            color: rgba(255, 247, 234, 0.48) !important;
        }}

        div[data-testid="stFormSubmitButton"] button {{
            background: linear-gradient(90deg, #2f6944, #c79a47);
            color: #fff7ea;
            border: 0;
            border-radius: 999px;
            font-weight: 800;
            padding: 0.62rem 1.1rem;
            width: 100%;
        }}

        div[data-testid="stFormSubmitButton"] button:hover {{
            background: linear-gradient(90deg, #3a7a51, #d0a455);
            color: #fff7ea;
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
            background: linear-gradient(145deg, rgba(9, 23, 13, 0.12), rgba(22, 48, 29, 0.06));
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 34px;
            box-shadow: 0 14px 26px rgba(7, 17, 10, 0.09), var(--glass-highlight);
            padding: 2rem;
            overflow: hidden;
            position: relative;
            margin-bottom: 1.35rem;
            backdrop-filter: blur(4px);
        }}

        .hero-shell::after {{
            content: "";
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at right top, rgba(214, 175, 98, 0.12), transparent 32%),
                linear-gradient(90deg, rgba(214, 175, 98, 0.04), transparent 46%);
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

        .hero-title-card {{
            background: linear-gradient(180deg, rgba(8, 21, 12, 0.20), rgba(8, 21, 12, 0.10));
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 28px;
            box-shadow: 0 14px 24px rgba(7, 17, 10, 0.08), var(--glass-highlight);
            padding: 1.25rem 1.4rem 1.35rem 1.4rem;
            width: min(100%, 980px);
            backdrop-filter: blur(6px);
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

        .hero-copy {{
            color: rgba(255, 247, 234, 0.84);
            font-size: 1rem;
            line-height: 1.72;
            margin-top: 1rem;
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
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.10);
            color: #fff7ea;
            font-size: 0.8rem;
            font-weight: 700;
            padding: 0.45rem 0.72rem;
            backdrop-filter: blur(5px);
            box-shadow: var(--glass-highlight);
        }}

        .hero-stats {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
            margin-top: 1.35rem;
            width: min(100%, 980px);
        }}

        .hero-stat {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 20px;
            padding: 0.9rem;
            backdrop-filter: blur(6px);
            box-shadow: var(--glass-highlight);
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
            color: rgba(255, 247, 234, 0.74);
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
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 24px;
            padding: 1rem;
            backdrop-filter: blur(6px);
            box-shadow: var(--glass-highlight);
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
            color: rgba(255, 247, 234, 0.76);
            font-size: 0.94rem;
            line-height: 1.62;
            margin-top: 0.55rem;
        }}

        .section-block {{
            margin: 1.65rem 0 0.95rem 0;
            padding: 0.8rem 1rem;
            border-radius: 22px;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.01));
            border: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(4px);
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
            color: rgba(251, 247, 237, 0.84);
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
            backdrop-filter: blur(6px);
            box-shadow: var(--shadow), var(--glass-highlight);
        }}

        .metric-card {{
            position: relative;
            overflow: hidden;
            background: rgba(255, 255, 255, 0.028);
            border: 1px solid rgba(255, 255, 255, 0.10);
            backdrop-filter: blur(5px);
        }}

        .metric-card::before {{
            content: "";
            position: absolute;
            left: 0;
            right: 0;
            top: 0;
            height: 3px;
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

        .insight-copy,
        .note-copy {{
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
            background: rgba(255, 255, 255, 0.015);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 24px;
            box-shadow: var(--shadow), var(--glass-highlight);
            padding: 0.35rem;
            backdrop-filter: blur(4px);
        }}

        @media (max-width: 1100px) {{
            .hero-stats {{
                grid-template-columns: 1fr;
            }}
        }}

        @media (min-width: 1200px) {{
            .block-container {{
                padding-top: 10.4rem;
            }}

            .hero-shell {{
                margin-top: 0.7rem;
            }}
        }}

        @media (max-width: 640px) {{
            .block-container {{
                padding-top: 11.2rem;
            }}

            .st-key-page_nav_shell {{
                top: 3.5rem;
                padding: 0 0.55rem;
            }}

            .st-key-page_nav_shell > div {{
                border-radius: 18px;
                padding: 0.6rem;
            }}

            .page-nav-row {{
                flex-direction: column;
                align-items: stretch;
            }}
        }}
    </style>
    """


def apply_theme(page_title: str, page_icon: str) -> None:
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(_theme_css(), unsafe_allow_html=True)


def render_page_nav(active_page: str) -> None:
    option_map = {item["title"]: item["path"] for item in PAGE_NAV_ITEMS}
    labels = list(option_map)
    active_label = next(
        (label for label, path in option_map.items() if path == active_page),
        labels[0],
    )

    with st.container(key="page_nav_shell"):
        left_col, right_col = st.columns([1, 2.6], vertical_alignment="center")
        with left_col:
            st.markdown('<div class="page-nav-kicker">Paginas</div>', unsafe_allow_html=True)
        with right_col:
            selected = st.selectbox(
                "Paginas",
                labels,
                index=labels.index(active_label),
                key=f"page_nav_{active_page}",
                label_visibility="collapsed",
            )

    if selected != active_label:
        st.switch_page(option_map[selected])


def sidebar_context(page_title: str, page_copy: str) -> None:
    render_page_nav("pages/1_Visao_Executiva.py")


def form_intro(kicker: str, title: str, copy: str, tags: list[str] | None = None) -> None:
    tags_html = ""
    if tags:
        tags_html = '<div class="form-intro-tags">' + "".join(
            f'<span class="form-intro-tag">{tag}</span>' for tag in tags
        ) + "</div>"

    st.markdown(
        f"""
        <div class="form-intro">
            <div class="form-intro-kicker">{kicker}</div>
            <div class="form-intro-title">{title}</div>
            <div class="form-intro-copy">{copy}</div>
            {tags_html}
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
