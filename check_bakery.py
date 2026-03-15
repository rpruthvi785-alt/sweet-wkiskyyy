import sqlite3
import json

db_path = r'd:\B WEB\freelance\bakery.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT * FROM products")
rows = cursor.fetchall()
colnames = [description[0] for description in cursor.description]
data = [dict(zip(colnames, row)) for row in rows]
print(json.dumps(data, indent=2))
conn.close()
