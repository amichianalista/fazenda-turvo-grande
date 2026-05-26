from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import math
import re

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT_DIR / "data" / "planilha_gestao.csv"


def _first_number(text: str | None) -> float | None:
    if not text:
        return None
    matches = re.findall(r"\d{1,3}(?:\.\d{3})*(?:,\d+)?|\d+(?:,\d+)?", str(text))
    if not matches:
        return None
    raw = matches[0].replace(".", "").replace(",", ".")
    try:
        return float(raw)
    except ValueError:
        return None


def _to_currency(value: float | None) -> str:
    if value is None or math.isnan(value):
        return "Nao mapeado"
    integer = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {integer}"


def _to_number(value: float | None, decimals: int = 0, suffix: str = "") -> str:
    if value is None or math.isnan(value):
        return "Nao mapeado"
    if decimals == 0:
        base = f"{int(round(value)):,}".replace(",", ".")
    else:
        base = f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{base}{suffix}"


def _to_percent(value: float | None) -> str:
    if value is None or math.isnan(value):
        return "Nao mapeado"
    return f"{value:.1f}%".replace(".", ",")


@lru_cache(maxsize=1)
def load_reference_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=["aba", "secao", "campo", "valor", "observacao", "status"])
    return pd.read_csv(DATA_FILE, encoding="utf-8-sig")


@lru_cache(maxsize=1)
def _field_lookup() -> dict[str, dict[str, str]]:
    df = load_reference_data()
    return {
        str(row["campo"]): row.to_dict()
        for _, row in df.iterrows()
        if pd.notna(row.get("campo"))
    }


def _field_text(field: str) -> str | None:
    record = _field_lookup().get(field)
    if not record:
        return None
    value = record.get("valor")
    if pd.isna(value) or value == "":
        return None
    return str(value)


def _field_number(field: str) -> float | None:
    return _first_number(_field_text(field))


def production_metrics() -> dict[str, float | str | None]:
    dias_semana = _field_number("Dias por semana de produção")
    queijos_dia = _field_number("Queijos por dia")
    peso_medio_kg = _field_number("Peso médio por queijo")
    queijos_semana = _field_number("Queijos por semana")
    queijos_mes = _field_number("Queijos por mês")
    kg_mes = _field_number("Kg de queijo por mês")
    receita_bruta = _field_number("Receita bruta mensal estimada")
    preco_kg = _field_number("Preço por kg pago pela cooperativa")
    pct_cooperativa = _field_number("Percentual vendido para cooperativa")

    capacidade_produtiva = None
    evolucao_pct = None

    return {
        "dias_semana": dias_semana,
        "queijos_dia": queijos_dia,
        "peso_medio_kg": peso_medio_kg,
        "queijos_semana": queijos_semana,
        "queijos_mes": queijos_mes,
        "kg_mes": kg_mes,
        "receita_bruta": receita_bruta,
        "preco_kg": preco_kg,
        "pct_cooperativa": pct_cooperativa,
        "capacidade_produtiva": capacidade_produtiva,
        "evolucao_pct": evolucao_pct,
    }


def production_snapshot_chart() -> pd.DataFrame:
    metrics = production_metrics()
    rows = []
    mapping = [
        ("Queijos por dia", metrics["queijos_dia"]),
        ("Queijos por semana", metrics["queijos_semana"]),
        ("Queijos por mes", metrics["queijos_mes"]),
    ]
    for label, value in mapping:
        if value is not None:
            rows.append({"indicador": label, "valor": value})
    return pd.DataFrame(rows)


def production_page_status() -> pd.DataFrame:
    metrics = production_metrics()
    rows = [
        ("Queijos/dia", metrics["queijos_dia"], "ok" if metrics["queijos_dia"] is not None else "faltando"),
        ("Kg/mes", metrics["kg_mes"], "ok" if metrics["kg_mes"] is not None else "faltando"),
        ("Evolucao da producao", metrics["evolucao_pct"], "faltando"),
        ("Capacidade produtiva", metrics["capacidade_produtiva"], "faltando"),
    ]
    return pd.DataFrame(rows, columns=["campo", "valor", "status"])


def cost_items() -> pd.DataFrame:
    df = load_reference_data()
    costs = df[df["aba"] == "2. O que a gente gasta"].copy()
    costs = costs[costs["secao"].isin(["CUSTOS QUE JÁ SABEMOS", "CUSTOS A DESCOBRIR"])].copy()
    costs["valor_num"] = costs["valor"].apply(_first_number)
    costs["tem_valor"] = costs["valor_num"].notna() & (costs["valor_num"] > 0)
    costs["categoria"] = costs["campo"].fillna("").astype(str)
    costs["grupo"] = costs["secao"].map(
        {
            "CUSTOS QUE JÁ SABEMOS": "Conhecidos",
            "CUSTOS A DESCOBRIR": "A descobrir",
        }
    )
    return costs[
        ["categoria", "grupo", "valor", "valor_num", "observacao", "status", "tem_valor"]
    ].reset_index(drop=True)


def cost_coverage_metrics() -> dict[str, float | int | None]:
    costs = cost_items()
    total = len(costs)
    filled = int(costs["tem_valor"].sum())
    pending = total - filled
    known = int((costs["grupo"] == "Conhecidos").sum())
    unknown = int((costs["grupo"] == "A descobrir").sum())
    filled_pct = (filled / total * 100) if total else 0.0
    return {
        "total_categorias": total,
        "categorias_com_valor": filled,
        "categorias_sem_valor": pending,
        "categorias_conhecidas": known,
        "categorias_a_descobrir": unknown,
        "percentual_preenchido": filled_pct,
    }


def cost_visibility() -> pd.DataFrame:
    coverage = cost_coverage_metrics()
    return pd.DataFrame(
        {
            "status": ["Com valor", "Sem valor"],
            "valor": [
                coverage["categorias_com_valor"],
                coverage["categorias_sem_valor"],
            ],
        }
    )


def cost_group_chart() -> pd.DataFrame:
    costs = cost_items()
    return (
        costs.groupby("grupo", as_index=False)
        .agg(quantidade=("categoria", "count"))
        .sort_values("quantidade", ascending=False)
    )


def cost_breakdown() -> pd.DataFrame:
    costs = cost_items()
    return costs[costs["tem_valor"]][["categoria", "valor_num"]].rename(
        columns={"valor_num": "valor"}
    )


def financial_metrics() -> dict[str, float | None]:
    production = production_metrics()
    costs = cost_breakdown()
    receita_bruta = production["receita_bruta"]
    custos = float(costs["valor"].sum()) if not costs.empty else None
    lucro_liquido = None
    margem = None
    if receita_bruta is not None and custos is not None:
        lucro_liquido = receita_bruta - custos
        margem = (lucro_liquido / receita_bruta * 100) if receita_bruta else None
    return {
        "receita_bruta": receita_bruta,
        "custos": custos,
        "lucro_liquido": lucro_liquido,
        "margem": margem,
    }


def financial_page_status() -> pd.DataFrame:
    metrics = financial_metrics()
    rows = [
        ("Receita bruta", metrics["receita_bruta"], "ok" if metrics["receita_bruta"] is not None else "faltando"),
        ("Custos", metrics["custos"], "ok" if metrics["custos"] is not None else "faltando"),
        ("Lucro liquido", metrics["lucro_liquido"], "ok" if metrics["lucro_liquido"] is not None else "faltando"),
        ("Margem", metrics["margem"], "ok" if metrics["margem"] is not None else "faltando"),
    ]
    return pd.DataFrame(rows, columns=["campo", "valor", "status"])


def financial_availability_chart() -> pd.DataFrame:
    status = financial_page_status()
    return (
        status.groupby("status", as_index=False)
        .agg(quantidade=("campo", "count"))
        .sort_values("quantidade", ascending=False)
    )


def diagnosis_cards() -> list[dict[str, str]]:
    production = production_metrics()
    finance = financial_metrics()
    costs = cost_items()

    cards: list[dict[str, str]] = []

    if production["queijos_dia"] is not None and production["kg_mes"] is not None:
        cards.append(
            {
                "title": "Producao atual ja mapeada",
                "copy": (
                    f"A base ja sustenta uma leitura inicial de {int(production['queijos_dia'])} "
                    f"queijos por dia e {production['kg_mes']:.0f} kg por mes."
                ),
                "tone": "green",
            }
        )

    if finance["margem"] is None:
        cards.append(
            {
                "title": "Margem ainda indisponivel",
                "copy": "A margem nao pode ser calculada enquanto os custos mensais continuarem sem valor preenchido.",
                "tone": "amber",
            }
        )

    if not costs[costs["categoria"].str.contains("Frete", case=False, na=False)]["tem_valor"].any():
        cards.append(
            {
                "title": "Frete segue sem valor",
                "copy": "A categoria de frete existe na estrutura, mas ainda nao tem numero para entrar no diagnostico real.",
                "tone": "earth",
            }
        )

    if not costs[costs["categoria"].str.contains("Energia", case=False, na=False)]["tem_valor"].any():
        cards.append(
            {
                "title": "Energia ainda nao mapeada",
                "copy": "O custo energetico aparece como lacuna explicita e hoje e um dos melhores candidatos para proxima coleta.",
                "tone": "slate",
            }
        )

    return cards


def action_priorities() -> pd.DataFrame:
    costs = cost_items()
    rows = []

    for _, row in costs.iterrows():
        if row["tem_valor"]:
            continue
        base_score = 92 if row["grupo"] == "Conhecidos" else 76
        if "Frete" in row["categoria"]:
            base_score = 95
        if "Energia" in row["categoria"]:
            base_score = 88
        rows.append({"frente": row["categoria"], "prioridade": base_score})

    rows.extend(
        [
            {"frente": "Historico de producao", "prioridade": 83},
            {"frente": "Capacidade produtiva", "prioridade": 79},
        ]
    )

    return pd.DataFrame(rows).sort_values("prioridade", ascending=False).reset_index(drop=True)


def overview_metrics() -> dict[str, str]:
    production = production_metrics()
    finance = financial_metrics()
    coverage = cost_coverage_metrics()

    margin_label = _to_percent(finance["margem"])
    if finance["margem"] is None:
        margin_delta = "Custos ainda nao preenchidos"
    else:
        margin_delta = "Margem calculada pela base atual"

    return {
        "queijos_dia": _to_number(production["queijos_dia"], suffix=" un."),
        "queijos_dia_delta": "Snapshot real da planilha",
        "receita_bruta": _to_currency(finance["receita_bruta"]),
        "receita_bruta_delta": "Estimativa mensal atual",
        "margem": margin_label,
        "margem_delta": margin_delta,
        "custos_cobertura": f"{coverage['categorias_com_valor']}/{coverage['total_categorias']}",
        "custos_cobertura_delta": "Categorias com valor monetizado",
    }


def formatting_helpers() -> dict[str, callable]:
    return {
        "currency": _to_currency,
        "number": _to_number,
        "percent": _to_percent,
    }
