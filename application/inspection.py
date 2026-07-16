from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TableInfo:
    """A table's introspected schema, as plain data (no formatting)."""

    name: str
    columns: list[tuple[str, str]]  # (column name, column type)
    pks: dict
    fks: list
    indexes: list


def introspect_tables(inspector, schema: str = "public") -> list[TableInfo]:
    """Introspect every table in ``schema`` and return it as plain data."""

    tables: list[TableInfo] = []
    for name in inspector.get_table_names(schema=schema):
        columns = [
            (c["name"], str(c["type"]))
            for c in inspector.get_columns(name, schema=schema)
        ]
        tables.append(
            TableInfo(
                name=name,
                columns=columns,
                pks=inspector.get_pk_constraint(name, schema=schema),
                fks=inspector.get_foreign_keys(name, schema=schema),
                indexes=inspector.get_indexes(name, schema=schema),
            )
        )
    return tables
