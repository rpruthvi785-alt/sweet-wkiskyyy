import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

srcs = re.findall(r'src="([^"]+)"', text)
for src in srcs:
    if not (src.startswith('http') or src.startswith('//')):
        path = src.replace('/', os.sep)
        if not os.path.exists(path):
            print(f"MISSING SRC: {src}")
        else:
            print(f"FOUND: {src}")
