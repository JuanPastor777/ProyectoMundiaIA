from app.database import execute_query

tablas = execute_query("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'mundial'
    ORDER BY table_name
""")

print("TABLAS DEL SCHEMA MUNDIAL:")
print()

for tabla in tablas:
    print("-", tabla["table_name"])