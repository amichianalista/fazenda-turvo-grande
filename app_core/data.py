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
        "region": "Serro (MG)",
        "territory_label": "Microrregiao do Serro",
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
        "dias_semana_text": dias_semana_text,
        "queijos_dia": _first_number(queijos_dia_text),
        "queijos_dia_text": queijos_dia_text,
        "peso_medio_kg": _first_number(peso_medio_text),
        "peso_medio_kg_text": peso_medio_text,
        "queijos_semana": _first_number(_lookup(results, "Queijos por semana")),
        "queijos_semana_text": _lookup(results, "Queijos por semana"),
        "queijos_mes": _first_number(_lookup(results, "Queijos por mes")),
        "queijos_mes_text": _lookup(results, "Queijos por mes"),
        "kg_mes": _first_number(_lookup(results, "Kg de queijo por mes")),
        "kg_mes_text": _lookup(results, "Kg de queijo por mes"),
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
        "preco_kg_text": preco_text,
        "pct_cooperativa": _first_number(pct_text),
        "pct_cooperativa_text": pct_text,
        "receita_bruta": _first_number(receita_text),
        "receita_bruta_text": receita_text,
        "canal": "Cooperativa",
    }


def operations_story() -> dict[str, object]:
    production = production_metrics()
    commercial = commercial_metrics()
    identity = identity_context()

    cadence = [
        {"label": "Dia", "value": production["queijos_dia"] or 0},
        {"label": "Semana", "value": production["queijos_semana"] or 0},
        {"label": "Mes", "value": production["queijos_mes"] or 0},
    ]

    formula_steps = [
        {
            "label": "Dias de producao",
            "value": _to_number(production["dias_semana"], suffix=" dias/semana"),
        },
        {
            "label": "Saida por dia",
            "value": _to_number(production["queijos_dia"], suffix=" queijos"),
        },
        {
            "label": "Peso medio",
            "value": _to_number(production["peso_medio_kg"], decimals=1, suffix=" kg/peca"),
        },
        {
            "label": "Receita atual",
            "value": _to_currency(commercial["receita_bruta"]),
        },
    ]

    return {
        "headline": "Operacao atual e potencial de captura de valor do Turvo Grande",
        "summary": (
            "A fazenda opera com cadencia recorrente, venda concentrada em cooperativa "
            "e um ativo de marca forte para evoluir em canal e posicionamento."
        ),
        "cadence": cadence,
        "formula_steps": formula_steps,
        "location_line": f"{identity['product_name']} | {identity['location']}",
    }


@lru_cache(maxsize=1)
def market_context() -> dict[str, object]:
    return {
        "hero_title": "Mercado, reputacao e espaco de expansao",
        "hero_copy": (
            "O estudo estrategico mostra que o principal valor do Turvo Grande esta na "
            "origem, na premiacao e na aderencia ao canal premium, e nao em competir por preco."
        ),
        "highlights": [
            {
                "label": "Premiacao",
                "value": "Mondial du Fromage 2019",
                "note": "Ativo raro de reputacao para um queijo artesanal regional.",
            },
            {
                "label": "Indicacao geografica",
                "value": "IG Serro desde 2011",
                "note": "Origem protegida, rastreavel e valorizada no varejo especializado.",
            },
            {
                "label": "Referencia de varejo",
                "value": "R$ 96 a R$ 140 por peca",
                "note": "Faixa observada no estudo para pecas premium de 700g a 1kg.",
            },
            {
                "label": "Base regional",
                "value": "~800 produtores",
                "note": "Escala territorial relevante e disputa por atencao qualificada.",
            },
        ],
        "market_stats": [
            {
                "label": "Consumo artesanal",
                "value": "20%",
                "note": "Participacao estimada do artesanal no consumo nacional citado no estudo.",
            },
            {
                "label": "Formalizacao",
                "value": "+300%",
                "note": "Crescimento observado em queijarias formalizadas em SP.",
            },
            {
                "label": "Ticket premium",
                "value": "R$ 96-R$ 140",
                "note": "Benchmark de varejo premium identificado em maio de 2026.",
            },
        ],
        "seasonality": [
            {"quarter": "Q1", "period": "Jan-Mar", "index": 72},
            {"quarter": "Q2", "period": "Abr-Jun", "index": 88},
            {"quarter": "Q3", "period": "Jul-Set", "index": 65},
            {"quarter": "Q4", "period": "Out-Dez", "index": 100},
        ],
        "competitors": [
            {
                "name": "Produtores do Serro",
                "score": 60,
                "threat": "Media",
                "detail": "Mesmo terroir, mesma IG e mesmo mercado base.",
            },
            {
                "name": "Canastra premium",
                "score": 92,
                "threat": "Alta",
                "detail": "Marca mais nacionalizada e e-commerce consolidado.",
            },
            {
                "name": "Emporios e distribuidores",
                "score": 48,
                "threat": "Indireta",
                "detail": "Agregam alcance, mas capturam margem de canal.",
            },
            {
                "name": "Industriais",
                "score": 20,
                "threat": "Baixa",
                "detail": "Competem em volume e preco, nao em atributo premium.",
            },
        ],
        "opportunities": [
            {
                "title": "Venda direta em plataformas",
                "ticket": "R$ 90 a R$ 140 por peca",
                "potential_score": 90,
                "complexity_score": 45,
                "next_step": "Validar cadastro em uma plataforma especializada.",
                "detail": "Canal com captura imediata de margem e prova de demanda.",
            },
            {
                "title": "Linha maturada premium",
                "ticket": "R$ 96 a R$ 160 por peca",
                "potential_score": 86,
                "complexity_score": 82,
                "next_step": "Dimensionar câmara, maturacao e padrao tecnico.",
                "detail": "Maior valor unitario, com barreira tecnica defensavel.",
            },
            {
                "title": "Restaurantes e chefs",
                "ticket": "R$ 60 a R$ 90 por kg",
                "potential_score": 74,
                "complexity_score": 55,
                "next_step": "Montar amostra comercial e roteiro BH/SP.",
                "detail": "Canal recorrente, reputacional e com volume mais previsivel.",
            },
            {
                "title": "Turismo e venda na fazenda",
                "ticket": "R$ 40 a R$ 80 por visitante",
                "potential_score": 62,
                "complexity_score": 58,
                "next_step": "Mapear adequacoes minimas e aderencia familiar.",
                "detail": "Receita complementar com alta forca de marca.",
            },
        ],
        "risks": [
            {
                "title": "Governanca e sucessao",
                "copy": "Sem clareza sobre quem assume a producao, a expansao fica fragil.",
            },
            {
                "title": "Capacidade produtiva",
                "copy": "Antes de vender mais caro, e preciso confirmar rebanho, estrutura e consistencia.",
            },
            {
                "title": "Regularizacao",
                "copy": "Selo Arte, SIF e requisitos sanitarios definem o teto real de canal.",
            },
            {
                "title": "Maturacao",
                "copy": "Linha premium exige câmara, controle e padrao tecnico, nao improviso.",
            },
        ],
        "action_plan": [
            {
                "window": "Dias 1-3",
                "title": "Conversa franca com a familia",
                "copy": "Confirmar abertura real para continuidade, papeis e limites da operacao.",
            },
            {
                "window": "Dias 4-6",
                "title": "Diagnostico tecnico da fazenda",
                "copy": "Levantar volume atual, estrutura, sanidade e capacidade de escala.",
            },
            {
                "window": "Dias 7-9",
                "title": "Pesquisa de canal e preco",
                "copy": "Mapear 3 a 5 canais especializados e suas exigencias de entrada.",
            },
            {
                "window": "Dias 10-12",
                "title": "Contato com SENAR / Emater",
                "copy": "Entender apoio tecnico e caminho de regularizacao para expansao.",
            },
            {
                "window": "Dias 13-15",
                "title": "Decisao de proximo passo",
                "copy": "Escolher um canal piloto com volume minimo e meta de validacao.",
            },
        ],
        "sources": [
            "Planilha operacional da fazenda",
            "Analise estrategica de mercado Turvo Grande, maio de 2026",
        ],
        "opportunity_note": (
            "Scores de potencial e complexidade sao uma sintese analitica derivada do estudo em PDF."
        ),
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
        note_text = _clean_spaces(row[6]) if len(row) > 6 else ""
        numeric_value = _first_number(value_text)
        has_value = numeric_value is not None

        items.append(
            {
                "group": current_group,
                "category": _clean_cost_label(name),
                "value_text": value_text or "Nao preenchido",
                "method_text": method_text or "Sem orientacao",
                "status_text": status_text or "Sem status",
                "note_text": note_text or "",
                "value_numeric": numeric_value,
                "has_value": has_value,
            }
        )

    return items


def known_costs() -> list[dict[str, str | bool | float | None]]:
    return [item for item in cost_entries() if item["group"] == "known"]


def discover_costs() -> list[dict[str, str | bool | float | None]]:
    return [item for item in cost_entries() if item["group"] == "discover"]


def cost_metrics() -> dict[str, int]:
    known = known_costs()
    discover = discover_costs()
    filled = sum(1 for item in cost_entries() if item["has_value"])

    return {
        "known_count": len(known),
        "discover_count": len(discover),
        "filled_count": filled,
        "pending_count": len(cost_entries()) - filled,
        "total_count": len(cost_entries()),
    }


def cost_summary() -> dict[str, str]:
    total_known = sum(float(item["value_numeric"]) for item in known_costs() if item["value_numeric"] is not None)
    total_discover = sum(
        float(item["value_numeric"]) for item in discover_costs() if item["value_numeric"] is not None
    )
    current_total = total_known + total_discover

    return {
        "known_total_text": _to_currency(total_known),
        "discover_total_text": _to_currency(total_discover),
        "current_total_text": _to_currency(current_total),
    }


def cost_readiness() -> dict[str, object]:
    metrics = cost_metrics()
    return {
        "status_split": [
            {"label": "Com valor", "value": metrics["filled_count"]},
            {"label": "Sem valor", "value": metrics["pending_count"]},
        ],
        "group_split": [
            {"label": "Custos conhecidos", "value": metrics["known_count"]},
            {"label": "Custos a descobrir", "value": metrics["discover_count"]},
        ],
        "next_steps": [
            "Transformar os custos conhecidos em valores mensais.",
            "Levantar energia, alimentacao do gado, manutencao e veterinario.",
            "Fechar taxa da cooperativa com contrato ou extrato real.",
            "So depois consolidar custo total, lucro e margem com seguranca.",
        ],
    }


def source_registry() -> dict[str, str]:
    return {
        "operational": "Referenciais Iniciais/planilha de gestao.ods",
        "market": "Referenciais Iniciais/queijo_turvo_grande.pdf",
        "product_image": str(PRODUCT_IMAGE),
    }


def overview_metrics() -> dict[str, str]:
    production = production_metrics()
    commercial = commercial_metrics()
    identity = identity_context()

    return {
        "operation_name": identity["operation_name"],
        "product_name": identity["product_name"],
        "location": identity["location"],
        "queijos_dia": _to_number(production["queijos_dia"], suffix=" un."),
        "queijos_mes": _to_number(production["queijos_mes"], suffix=" un."),
        "kg_mes": _to_number(production["kg_mes"], decimals=1, suffix=" kg"),
        "receita_bruta": _to_currency(commercial["receita_bruta"]),
        "preco_kg": _to_currency(commercial["preco_kg"]),
        "pct_cooperativa": _to_percent(commercial["pct_cooperativa"]),
    }


def formatting_helpers() -> dict[str, object]:
    return {
        "currency": _to_currency,
        "number": _to_number,
        "percent": _to_percent,
    }
