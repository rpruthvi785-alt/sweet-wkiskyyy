import sqlite3
import os

def list_products_and_images():
    db_path = 'bakery.db'
    if not os.path.exists(db_path):
        print(f"Error: Database {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, name, category, image_path FROM products")
        products = cursor.fetchall()
        
        print(f"{'ID':<4} | {'Name':<25} | {'Category':<10} | {'Image Status'}")
        print("-" * 70)
        
        for pid, name, cat, img in products:
            status = "✓ Local"
            if img.startswith('http'):
                status = "✗ External"
            else:
                path = os.path.join(os.getcwd(), img.replace('/', os.sep))
                if not os.path.exists(path):
                    status = "✗ MISSING Local"
            
            print(f"{pid:<4} | {name:<25} | {cat:<10} | {status} ({img})")
            
    except sqlite3.OperationalError as e:
        print(f"Error accessing products table: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    list_products_and_images()
