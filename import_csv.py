import sqlite3
import csv
import os

def import_csv_to_db():
    db_path = r'd:\B WEB\freelance\bakery.db'
    csv_path = r'd:\B WEB\freelance\bakery_products_export.csv'
    
    if not os.path.exists(csv_path):
        print("CSV not found!")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table if not exists (redundant since app.py does it but good for safety)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image_path TEXT,
                is_bestseller INTEGER DEFAULT 0
            )
        ''')

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute('''
                    INSERT INTO products (id, name, category, description, price, image_path, is_bestseller)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (row['id'], row['name'], row['category'], row['description'], row['price'], row['image_path'], row['is_bestseller']))
            
        conn.commit()
        print(f"Successfully imported products from {csv_path}")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import_csv_to_db()
