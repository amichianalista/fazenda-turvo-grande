from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import math
import re
import xml.etree.ElementTree as ET
import zipfile


ROOT_DIR = Path(__file__).resolve().parents[1]
SOURCE_FILE = ROOT_DIR / "Referenciais Iniciais" / "planilha de gestao.ods"

NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}


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


def _normalize_label(value: str) -> str:
    return " ".join(value.replace("\n", " ").split()).strip()


def _cell_text(cell: ET.Element) -> str:
    parts = []
    for paragraph in cell.findall(".//text:p", NS):
        parts.append("".join(paragraph.itertext()))
    return "\n".join(part for part in parts if part).strip()


@lru_cache(maxsize=1)
def _sheet_rows() -> dict[str, list[list[str]]]:
    if not SOURCE_FILE.exists():
        return {}

    with zipfile.ZipFile(SOURCE_FILE) as archive:
        root = ET.fromstring(archive.read("content.xml"))

    spreadsheet = root.find("office:body/office:spreadsheet", NS)
    if spreadsheet is None:
        return {}

    workbook: dict[str, list[list[str]]] = {}
    table_name_attr = f"{{{NS['table']}}}name"
    repeat_cols_attr = f"{{{NS['table']}}}number-columns-repeated"

    for table in spreadsheet.findall("table:table", NS):
        name = table.get(table_name_attr, "Sem nome")
        rows: list[list[str]] = []

        for row in table.findall("table:table-row", NS):
            values: list[str] = []
            for cell in row.findall("table:table-cell", NS):
                repeat_cols = int(cell.get(repeat_cols_attr, "1"))
                text = _cell_text(cell)
                values.extend([text] * repeat_cols)

            while values and values[-1] == "":
                values.pop()

            if any(values):
                rows.append(values)

        workbook[name] = rows

    return workbook


def _rows(sheet_name: str) -> list[list[str]]:
    return _sheet_rows().get(sheet_name, [])


@lru_cache(maxsize=1)
def identity_context() -> dict[str, str]:
    rows = _rows("1. O que a gente já sabe")
    header = rows[0][0] if rows and rows[0] else ""
    parts = [part.strip() for part in header.split("·")]

    operation_name = parts[0].title() if parts else "Operacao nao mapeada"
    product_name = parts[1] if len(parts) > 1 else "Produto nao mapeado"
    location = parts[2] if len(parts) > 2 else "Localidade nao mapeada"

    return {
        "headline": header,
        "operation_name": operation_name,
        "product_name": product_name,
        "location": location,
    }


@lru_cache(maxsize=1)
def sheet_one_blocks() -> dict[str, dict[str, str]]:
    rows = _rows("1. O que a gente já sabe")
    sections = {"PRODUÇÃO", "VENDA", "RESULTADO"}
    current_section = ""
    questions: dict[str, str] = {}
    sales: dict[str, str] = {}
    results: dict[str, str] = {}

    for row in rows:
        label = _normalize_label(row[0]) if row else ""
        if any(section in label for section in sections):
            if "PRODUÇÃO" in label:
                current_section = "production"
            elif "VENDA" in label:
                current_section = "sales"
            elif "RESULTADO" in label:
                current_section = "results"
            continue

        if len(row) >= 3 and _normalize_label(row[1]) == "Pergunta":
            continue

        if current_section in {"production", "sales"} and len(row) >= 3 and row[1]:
            target = questions if current_section == "production" else sales
            target[_normalize_label(row[1])] = _normalize_label(row[2])

        if current_section == "results" and len(row) >= 3 and row[1]:
            results[_normalize_label(row[1])] = _normalize_label(row[2])

    return {
        "production": questions,
        "sales": sales,
        "results": results,
    }


def production_metrics() -> dict[str, float | str | None]:
    blocks = sheet_one_blocks()
    production = blocks["production"]
    results = blocks["results"]

    dias_semana_text = production.get("Quantos dias por semana a senhora faz queijo?")
    queijos_dia_text = production.get("Quantos queijos saem prontos por dia de produção?")
    peso_medio_text = production.get("Quanto pesa cada queijo em média?")

    return {
        "dias_semana": _first_number(dias_semana_text),
        "dias_semana_text": dias_semana_text,
        "queijos_dia": _first_number(queijos_dia_text),
        "queijos_dia_text": queijos_dia_text,
        "peso_medio_kg": _first_number(peso_medio_text),
        "peso_medio_kg_text": peso_medio_text,
        "queijos_semana": _first_number(results.get("Queijos por semana")),
        "queijos_semana_text": results.get("Queijos por semana"),
        "queijos_mes": _first_number(results.get("Queijos por mês")),
        "queijos_mes_text": results.get("Queijos por mês"),
        "kg_mes": _first_number(results.get("Kg de queijo por mês")),
        "kg_mes_text": results.get("Kg de queijo por mês"),
    }


def commercial_metrics() -> dict[str, float | str | None]:
    blocks = sheet_one_blocks()
    sales = blocks["sales"]
    results = blocks["results"]

    preco_text = sales.get("Quanto a cooperativa paga por kg do queijo?")
    pct_text = sales.get("Qual % do queijo vai para a cooperativa?")
    receita_text = results.get("💰 RECEITA BRUTA DO MÊS")

    return {
        "preco_kg": _first_number(preco_text),
        "preco_kg_text": preco_text,
        "pct_cooperativa": _first_number(pct_text),
        "pct_cooperativa_text": pct_text,
        "receita_bruta": _first_number(receita_text),
        "receita_bruta_text": receita_text,
        "canal": "Cooperativa",
    }


def overview_metrics() -> dict[str, str]:
    production = production_metrics()
    commercial = commercial_metrics()

    return {
        "operation_name": identity_context()["operation_name"],
        "product_name": identity_context()["product_name"],
        "location": identity_context()["location"],
        "queijos_dia": _to_number(production["queijos_dia"], suffix=" un."),
        "queijos_mes": _to_number(production["queijos_mes"], suffix=" un."),
        "kg_mes": _to_number(production["kg_mes"], decimals=1, suffix=" kg"),
        "receita_bruta": _to_currency(commercial["receita_bruta"]),
        "preco_kg": _to_currency(commercial["preco_kg"]),
        "pct_cooperativa": _to_percent(commercial["pct_cooperativa"]),
    }


def formatting_helpers() -> dict[str, callable]:
    return {
        "currency": _to_currency,
        "number": _to_number,
        "percent": _to_percent,
    }
