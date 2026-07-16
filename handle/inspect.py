from database.api import Database

def inspection_print_tables(inspector):
    for table_name in inspector.get_table_names(schema="public"):
        print(table_name, "-" * len(table_name), sep="\n")
        columns = inspector.get_columns(table_name, schema="public")
        print(*(f"{c['name']} {c['type']}" for c in columns), sep="\n", end="\n\n")
        print("PKs:", inspector.get_pk_constraint(table_name), end="\n\n")
        print("FKs:", inspector.get_foreign_keys(table_name), end="\n\n")
        print("Indexes:", inspector.get_indexes(table_name), end="\n\n\n")

if __name__ == "__main__":
    db_url = "postgresql+psycopg2://appuser:changeme@localhost:5432/dbpop-probe"
    inspector = Database(db_url).inspector()
    inspection_print_tables(inspector)
