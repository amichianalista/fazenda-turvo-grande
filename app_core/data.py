from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import math
import re
import unicodedata
import xml.etree.ElementTree as ET
import zipfile


ROOT_DIR = Path(__file__).resolve().parents[1]
SOURCE_FILE = ROOT_DIR / "Referenciais Iniciais" / "planilha de gestao.ods"
BACKGROUND_IMAGE = ROOT_DIR / "assets" / "background.png"
PRODUCT_IMAGE = ROOT_DIR / "assets" / "queijopremiado.png"

NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}


def _strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def _clean_spaces(value: str | None) -> str:
    return " ".join((value or "").replace("\n", " ").split()).strip()


def _normalized_key(value: str | None) -> str:
    cleaned = _clean_spaces(_strip_accents(value or "")).lower()
    cleaned = re.sub(r"[^a-z0-9%/ ]+", "", cleaned)
    return " ".join(cleaned.split())


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
                text = _clean_spaces(_cell_text(cell))
                values.extend([text] * repeat_cols)

            while values and values[-1] == "":
                values.pop()

            if any(values):
                rows.append(values)

        workbook[name] = rows

    return workbook


def _resolve_sheet_name(expected_name: str) -> str:
    expected_key = _normalized_key(expected_name)
    for current_name in _sheet_rows():
        if _normalized_key(current_name) == expected_key:
            return current_name
    return expected_name


def _rows(sheet_name: str) -> list[list[str]]:
    return _sheet_rows().get(_resolve_sheet_name(sheet_name), [])


def _lookup(block: dict[str, str], label: str) -> str | None:
    return block.get(_normalized_key(label))


def _clean_cost_label(value: str) -> str:
    cleaned = _clean_spaces(value)
    return re.sub(r"^[^A-Za-z0-9]+", "", cleaned).strip()


@lru_cache(maxsize=1)
def identity_context() -> dict[str, str]:
    rows = _rows("1. O que a gente ja sabe")
    header = rows[0][0] if rows and rows[0] else ""
    parts = [part.strip() for part in header.split("·")] if header else []

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
    rows = _rows("1. O que a gente ja sabe")
    current_section = ""
    production: dict[str, str] = {}
    sales: dict[str, str] = {}
    results: dict[str, str] = {}

    for row in rows:
        label = row[0] if row else ""
        label_key = _normalized_key(label)

        if "producao" in label_key:
            current_section = "production"
            continue
        if label_key == "venda":
            current_section = "sales"
            continue
        if "resultado" in label_key:
            current_section = "results"
            continue

        if len(row) >= 3 and _normalized_key(row[1]) == "pergunta":
            continue

        if current_section in {"production", "sales"} and len(row) >= 3 and row[1]:
            target = production if current_section == "production" else sales
            target[_normalized_key(row[1])] = _clean_spaces(row[2])

        if current_section == "results" and len(row) >= 3 and row[1]:
            results[_normalized_key(row[1])] = _clean_spaces(row[2])

    return {
        "production": production,
        "sales": sales,
        "results": results,
    }


def production_metrics() -> dict[str, float | str | None]:
    blocks = sheet_one_blocks()
    production = blocks["production"]
    results = blocks["results"]

    dias_semana_text = _lookup(production, "Quantos dias por semana a senhora faz queijo?")
    queijos_dia_text = _lookup(production, "Quantos queijos saem prontos por dia de producao?")
    peso_medio_text = _lookup(production, "Quanto pesa cada queijo em media?")

    return {
        "dias_semana": _first_number(dias_semana_text),
        "queijos_dia": _first_number(queijos_dia_text),
        "peso_medio_kg": _first_number(peso_medio_text),
        "queijos_semana": _first_number(_lookup(results, "Queijos por semana")),
        "queijos_mes": _first_number(_lookup(results, "Queijos por mes")),
        "kg_mes": _first_number(_lookup(results, "Kg de queijo por mes")),
    }


def commercial_metrics() -> dict[str, float | str | None]:
    blocks = sheet_one_blocks()
    sales = blocks["sales"]
    results = blocks["results"]

    preco_text = _lookup(sales, "Quanto a cooperativa paga por kg do queijo?")
    pct_text = _lookup(sales, "Qual % do queijo vai para a cooperativa?")
    receita_text = _lookup(results, "Receita bruta do mes")

    return {
        "preco_kg": _first_number(preco_text),
        "pct_cooperativa": _first_number(pct_text),
        "receita_bruta": _first_number(receita_text),
        "canal": "Cooperativa",
    }


@lru_cache(maxsize=1)
def cost_entries() -> list[dict[str, str | bool | float | None]]:
    rows = _rows("2. O que a gente gasta")
    current_group = ""
    items: list[dict[str, str | bool | float | None]] = []

    for row in rows:
        label = row[0] if row else ""
        label_key = _normalized_key(label)

        if "custos que ja sabemos" in label_key:
            current_group = "known"
            continue
        if "custos a descobrir" in label_key:
            current_group = "discover"
            continue
        if "resumo dos custos" in label_key:
            current_group = ""
            continue

        if len(row) < 5 or not current_group:
            continue

        name = row[1] if len(row) > 1 else ""
        if not name or _normalized_key(name) == "custo":
            continue

        value_text = _clean_spaces(row[2]) if len(row) > 2 else ""
        method_text = _clean_spaces(row[3]) if len(row) > 3 else ""
        status_text = _clean_spaces(row[4]) if len(row) > 4 else ""
        numeric_value = _first_number(value_text)

        items.append(
            {
                "group": current_group,
                "category": _clean_cost_label(name),
                "value_text": value_text or "Nao preenchido",
                "method_text": method_text or "Sem orientacao",
                "status_text": status_text or "Sem status",
                "value_numeric": numeric_value,
                "has_value": numeric_value is not None,
            }
        )

    return items


def cost_metrics() -> dict[str, int]:
    known = sum(1 for item in cost_entries() if item["group"] == "known")
    discover = sum(1 for item in cost_entries() if item["group"] == "discover")
    filled = sum(1 for item in cost_entries() if item["has_value"])
    total = len(cost_entries())

    return {
        "known_count": known,
        "discover_count": discover,
        "filled_count": filled,
        "pending_count": max(total - filled, 0),
        "total_count": total,
    }


def missing_costs(limit: int = 5) -> list[dict[str, str]]:
    pending = [item for item in cost_entries() if not item["has_value"]]
    return [
        {
            "category": str(item["category"]),
            "method": str(item["method_text"]),
            "status": str(item["status_text"]),
        }
        for item in pending[:limit]
    ]


def management_readiness() -> dict[str, object]:
    metrics = cost_metrics()
    total = metrics["total_count"] or 1
    readiness_pct = round((metrics["filled_count"] / total) * 100)

    return {
        "readiness_pct": readiness_pct,
        "filled_count": metrics["filled_count"],
        "pending_count": metrics["pending_count"],
        "known_count": metrics["known_count"],
        "discover_count": metrics["discover_count"],
        "message": (
            "A producao e a receita ja estao na mao. O que ainda segura o lucro real "
            "e fechar os custos que faltam entrar no caderno."
        ),
    }


@lru_cache(maxsize=1)
def opportunities() -> list[dict[str, str]]:
    return [
        {
            "title": "Vender um pedaco em canal direto",
            "copy": (
                "Sem mexer em tudo de uma vez, a fazenda pode testar um canal pequeno "
                "de venda direta e aprender onde o produto ganha mais valor."
            ),
        },
        {
            "title": "Criar uma linha mais valorizada",
            "copy": (
                "O queijo tem origem forte e historia boa. Com maturacao bem cuidada, "
                "pode entrar numa faixa de preco mais nobre."
            ),
        },
        {
            "title": "Fechar o custo antes de acelerar",
            "copy": (
                "O melhor ganho agora talvez nem seja vender mais, e sim entender direito "
                "quanto sobra por mes para decidir com seguranca."
            ),
        },
    ]


def producer_messages() -> list[dict[str, str]]:
    return [
        {
            "title": "Produz todo dia, com cadencia boa",
            "copy": "A rotina de producao esta firme. Isso e base boa para crescer sem dar tranco.",
        },
        {
            "title": "Hoje o dinheiro entra por um canal so",
            "copy": "A cooperativa resolve a saida, mas deixa a fazenda dependente de um unico caminho.",
        },
        {
            "title": "O lucro real ainda nao esta fechado",
            "copy": "Enquanto varios custos seguem sem valor mensal, o numero final fica incompleto.",
        },
    ]


def source_registry() -> dict[str, str]:
    return {
        "operational": "Referenciais Iniciais/planilha de gestao.ods",
        "market": "Referenciais Iniciais/queijo_turvo_grande.pdf",
        "background": str(BACKGROUND_IMAGE),
        "product_image": str(PRODUCT_IMAGE),
    }


def formatting_helpers() -> dict[str, object]:
    return {
        "currency": _to_currency,
        "number": _to_number,
        "percent": _to_percent,
    }
