import sqlite3
import json
import os

# Check if the file exists first
db_path = r'd:\B WEB\luxury web\preorders.db'

if not os.path.exists(db_path):
    print(f"File not found: {db_path}")
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        data = {}
        for table_name in tables:
            t_name = table_name[0]
            cursor.execute(f"SELECT * FROM {t_name}")
            rows = cursor.fetchall()
            colnames = [description[0] for description in cursor.description]
            data[t_name] = [dict(zip(colnames, row)) for row in rows]
            
        print(json.dumps(data, indent=2))
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
