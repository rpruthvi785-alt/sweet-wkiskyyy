import os
import re
import sqlite3

print("--- index.html missing ---")
html_path = 'index.html'
if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    imgs = re.findall(r'src="([^"]+)"', content)
    for img in imgs:
        if not img.startswith('http') and not img.startswith('//'):
            path = os.path.join(os.getcwd(), img.replace('/', os.sep))
            if not os.path.exists(path):
                print(f"MISSING IN HTML: {img}")

print("--- DB missing ---")
db_path = 'bakery.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, image_path FROM products')
    for pid, name, img in cursor.fetchall():
        if img and not img.startswith('http'):
            path = os.path.join(os.getcwd(), img.replace('/', os.sep))
            if not os.path.exists(path):
                print(f"MISSING IN DB [ID {pid}]: {img}")
    conn.close()
