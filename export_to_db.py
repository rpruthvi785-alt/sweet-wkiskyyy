import sqlite3
import re
import os

def extract_products(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex for menu items
    # Sample: <article class="menu-item reveal delay-1" data-category="cakes">
    item_pattern = re.compile(r'<article class="menu-item[^"]*" data-category="([^"]+)">\s*(.*?)\s*</article>', re.DOTALL)
    
    products = []
    items = item_pattern.findall(content)
    
    for category, inner_html in items:
        # Extract title: <h3 class="menu-title">Classic Vanilla Sponge</h3>
        title_match = re.search(r'<h3 class="menu-title">([^<]+)</h3>', inner_html)
        title = title_match.group(1) if title_match else "Unknown"
        
        # Extract description: <p class="menu-desc">...</p>
        desc_match = re.search(r'<p class="menu-desc">([^<]+)</p>', inner_html)
        desc = desc_match.group(1) if desc_match else ""
        
        # Extract image: <img src="([^"]+)"
        img_match = re.search(r'<img src="([^"]+)"', inner_html)
        image_path = img_match.group(1) if img_match else ""
        
        # Extract price and name from button: data-name="([^"]+)" data-price="([^"]+)"
        btn_match = re.search(r'data-name="([^"]+)" data-price="([^"]+)"', inner_html)
        if btn_match:
            # name = btn_match.group(1) # We use the title instead
            price_str = btn_match.group(2)
            try:
                price = float(price_str)
            except ValueError:
                price = 0.0
        else:
            price = 0.0
            
        # Check for bestseller badge
        is_bestseller = 1 if 'menu-badge' in inner_html else 0
        
        products.append((title, category, desc, price, image_path, is_bestseller))
    
    return products

def main():
    html_path = r'd:\B WEB\freelance\index.html'
    db_path = r'd:\B WEB\freelance\bakery.db'
    
    if not os.path.exists(html_path):
        print(f"File not found: {html_path}")
        return

    print(f"Reading products from {html_path}...")
    products = extract_products(html_path)
    print(f"Found {len(products)} products.")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            description TEXT,
            price REAL,
            image_path TEXT,
            is_bestseller INTEGER DEFAULT 0
        )
    ''')
    
    # Insert data
    cursor.executemany('''
        INSERT INTO products (name, category, description, price, image_path, is_bestseller)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', products)
    
    conn.commit()
    conn.close()
    
    print(f"Successfully exported {len(products)} products to {db_path}")

if __name__ == "__main__":
    main()
