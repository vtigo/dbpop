from application.inspection import TableInfo, introspect_tables
from config import DATABASE_URL
from database.api import get_database


def format_table(table: TableInfo) -> str:
    lines = [table.name, "-" * len(table.name)]
    lines += [f"{col_name} {col_type}" for col_name, col_type in table.columns]
    lines += ["", f"PKs: {table.pks}"]
    lines += ["", f"FKs: {table.fks}"]
    lines += ["", f"Indexes: {table.indexes}"]
    return "\n".join(lines)


if __name__ == "__main__":
    inspector = get_database(DATABASE_URL).inspector()
    tables = introspect_tables(inspector)
    print("\n\n\n".join(format_table(t) for t in tables))
