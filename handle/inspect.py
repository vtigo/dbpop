from database.api import Database

# TODO: extract configuration
DATABASE_URL = "postgresql+psycopg2://appuser:changeme@localhost:5432/dbpop-probe"

inspector = Database(DATABASE_URL).inspector()

for table_name in inspector.get_table_names(schema="public"):
    print(table_name)
    for column in inspector.get_columns(table_name, schema="public"):
        print(" ", column["name"], column["type"])
    print(" PKs:", inspector.get_pk_constraint(table_name))
    print(" FKs:", inspector.get_foreign_keys(table_name))
    print(" Indexes:", inspector.get_indexes(table_name))
