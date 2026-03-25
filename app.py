import sqlite3
import os
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

DB_FILE = 'bakery.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Create users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Create orders table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            order_type TEXT DEFAULT 'dine-in',
            status TEXT DEFAULT 'received',
            ordered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            custom_details TEXT
        )
    ''')
    # Create products table
    try:
        conn.execute("ALTER TABLE orders ADD COLUMN custom_details TEXT")
    except sqlite3.OperationalError:
        pass

    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            description TEXT,
            price REAL,
            image_path TEXT,
            is_bestseller INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in products])

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                        (username, password)).fetchone()
    conn.close()
    
    if user:
        return jsonify({"success": True, "user": user['username']})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not (username and email and password):
        return jsonify({"success": False, "message": "Missing fields"}), 400
        
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                    (username, email, password))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "user": username})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Username or email already exists"}), 400

@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.json
    username = data.get('user')
    cart = data.get('cart')
    order_type = data.get('type', 'dine-in') # 'dine-in' or 'delivery'
    
    if not (username and cart):
        return jsonify({"success": False, "message": "Invalid data"}), 400
        
    try:
        conn = get_db_connection()
        for item in cart:
            conn.execute('''
                INSERT INTO orders (username, product_name, price, quantity, order_type, status, custom_details)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, item['name'], item['price'], item['quantity'], order_type, 'baking', item.get('details', '')))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Order history updated!"})
    except Exception as e:
        print(f"Checkout error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    username = request.args.get('user')
    if not username:
        return jsonify([]), 400
        
    conn = get_db_connection()
    history = conn.execute('''
        SELECT product_name, price, quantity, ordered_at, status, order_type
        FROM orders WHERE username = ? 
        ORDER BY ordered_at DESC
    ''', (username,)).fetchall()
    conn.close()
    
    return jsonify([dict(ix) for ix in history])

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    # Trigger the export script logic or just serve the file
    # For simplicity, we'll just serve the already generated file or generate it on the fly
    import csv
    import io
    
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    
    si = io.StringIO()
    cw = csv.writer(si)
    
    if products:
        cw.writerow(products[0].keys())
        cw.writerows(products)
    
    output = si.getvalue()
    return output, 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=bakery_products.csv'
    }

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5050)
