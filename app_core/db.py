from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import os

import psycopg
from psycopg import sql


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = "agro_turvo_grande"


@lru_cache(maxsize=1)
def _env_values() -> dict[str, str]:
    values: dict[str, str] = {}
    env_file = ROOT_DIR / ".env"

    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            cleaned = line.strip()
            if not cleaned or cleaned.startswith("#") or "=" not in cleaned:
                continue
            key, value = cleaned.split("=", 1)
            values[key.strip()] = value.strip()

    for key, value in os.environ.items():
        values[key] = value

    return values


def _database_url() -> str:
    database_url = _env_values().get("SUPABASE_DATABASE_URL")
    if not database_url:
        raise RuntimeError("SUPABASE_DATABASE_URL nao encontrada no ambiente.")
    return database_url


def _normalize_payload(payload: dict[str, str | None]) -> dict[str, str | None]:
    normalized: dict[str, str | None] = {}
    for key, value in payload.items():
        if value is None:
            normalized[key] = None
            continue
        cleaned = value.strip()
        normalized[key] = cleaned or None
    return normalized


def payload_has_values(payload: dict[str, str | None]) -> bool:
    return any(value not in {None, ""} for value in _normalize_payload(payload).values())


def insert_row(
    table: str,
    payload: dict[str, str | None],
    schema: str = DEFAULT_SCHEMA,
    conn: psycopg.Connection | None = None,
) -> str:
    normalized = _normalize_payload(payload)
    columns = [column for column, value in normalized.items() if value is not None]
    values = [normalized[column] for column in columns]

    manage_connection = conn is None
    active_conn = conn or psycopg.connect(_database_url())

    try:
        with active_conn.cursor() as cur:
            if columns:
                query = sql.SQL("insert into {}.{} ({}) values ({}) returning id").format(
                    sql.Identifier(schema),
                    sql.Identifier(table),
                    sql.SQL(", ").join(sql.Identifier(column) for column in columns),
                    sql.SQL(", ").join(sql.Placeholder() for _ in columns),
                )
                cur.execute(query, values)
            else:
                query = sql.SQL("insert into {}.{} default values returning id").format(
                    sql.Identifier(schema),
                    sql.Identifier(table),
                )
                cur.execute(query)

            record_id = str(cur.fetchone()[0])

        if manage_connection:
            active_conn.commit()

        return record_id
    except Exception:
        if manage_connection:
            active_conn.rollback()
        raise
    finally:
        if manage_connection:
            active_conn.close()


def insert_batch(
    rows: list[tuple[str, dict[str, str | None]]],
    schema: str = DEFAULT_SCHEMA,
) -> dict[str, str]:
    results: dict[str, str] = {}
    with psycopg.connect(_database_url()) as conn:
        with conn.transaction():
            for table, payload in rows:
                results[table] = insert_row(table=table, payload=payload, schema=schema, conn=conn)
    return results
