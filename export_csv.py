import sqlite3
import csv
import os

def export_db_to_csv():
    db_path = r'd:\B WEB\freelance\bakery.db'
    csv_path = r'd:\B WEB\freelance\bakery_products_export.csv'
    
    if not os.path.exists(db_path):
        print("Database not found!")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get products
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        
        # Get column names
        colnames = [description[0] for description in cursor.description]
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(colnames) # write headers
            writer.writerows(rows)
            
        print(f"Successfully exported products to {csv_path}")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    export_db_to_csv()
