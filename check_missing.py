import sqlite3
import os

db_path = 'bakery.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('SELECT id, name, image_path FROM products')
rows = cursor.fetchall()

missing = []
for pid, name, img in rows:
    path = os.path.join(os.getcwd(), img.replace('/', os.sep))
    if not os.path.exists(path):
        missing.append((pid, name, img))

with open('missing_db_images.txt', 'w') as f:
    for m in missing:
        f.write(f"ID {m[0]}: {m[1]} -> {m[2]}\n")

conn.close()
