import os
import requests
import json
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

SUPABASE_URL = "https://ojhenudsmcvuiobpcqsv.supabase.co"
SUPABASE_KEY = "sb_publishable_jtGvrWNZ5moIkQj1HwoWQQ_W5nFMfjE"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    res = requests.get(f"{SUPABASE_URL}/rest/v1/products", headers=HEADERS)
    if res.status_code == 200:
        return jsonify(res.json())
    return jsonify([]), res.status_code

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '').lower().strip()
    password = data.get('password')
    
    # Query Supabase for the user
    res = requests.get(
        f"{SUPABASE_URL}/rest/v1/users?username=eq.{username}&password=eq.{password}",
        headers=HEADERS
    )
    
    if res.status_code == 200:
        users = res.json()
        if len(users) > 0:
            return jsonify({"success": True, "user": users[0]['username']})
            
    return jsonify({"success": False, "message": "Invalid username or password"}), 401

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username', '').lower().strip()
    email = data.get('email', '').lower().strip()
    password = data.get('password')
    
    if not (username and email and password):
        return jsonify({"success": False, "message": "Missing fields"}), 400
        
    # Insert new user - pre-check is skipped to avoid RLS read-access issues
    # Supabase unique constraints (23505) will trigger an error if user exists
    insert_res = requests.post(f"{SUPABASE_URL}/rest/v1/users", headers={**HEADERS, "Prefer": "return=representation"}, json={
        "username": username,
        "email": email,
        "password": password
    })
    
    if insert_res.status_code in (200, 201):
        return jsonify({"success": True, "user": username})
    
    # Handle duplicate key error 23505
    err_data = insert_res.json()
    if err_data.get('code') == '23505':
        return jsonify({"success": False, "message": "Username or email already exists"}), 409
        
    return jsonify({"success": False, "message": err_data.get('message', "Failed to create user")}), insert_res.status_code

@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.json
    username = data.get('user')
    cart = data.get('cart')
    order_type = data.get('type', 'dine-in') # 'dine-in' or 'delivery'
    
    if not (username and cart):
        return jsonify({"success": False, "message": "Invalid data"}), 400
        
    orders_to_insert = []
    for item in cart:
        orders_to_insert.append({
            "username": username.lower().strip(),
            "product_name": item['name'],
            "price": float(item['price']),
            "quantity": int(item['quantity']),
            "order_type": order_type,
            "status": 'baking',
            "custom_details": item.get('details', '')
        })
        
    res = requests.post(f"{SUPABASE_URL}/rest/v1/orders", headers={**HEADERS, "Prefer": "return=minimal"}, json=orders_to_insert)
    
    if res.status_code in (200, 201):
        return jsonify({"success": True, "message": "Order history updated!"})
        
    return jsonify({"success": False, "message": "Failed to process checkout"}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    username = request.args.get('user')
    if not username:
        return jsonify([]), 400
        
    res = requests.get(
        f"{SUPABASE_URL}/rest/v1/orders?username=eq.{username}&order=ordered_at.desc",
        headers=HEADERS
    )
    
    if res.status_code == 200:
        return jsonify(res.json())
        
    return jsonify([]), 500

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    import csv
    import io
    
    res = requests.get(f"{SUPABASE_URL}/rest/v1/products", headers=HEADERS)
    products = res.json() if res.status_code == 200 else []
    
    si = io.StringIO()
    cw = csv.writer(si)
    
    if products:
        cw.writerow(products[0].keys())
        for p in products:
            cw.writerow(p.values())
    
    output = si.getvalue()
    return output, 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=bakery_products.csv'
    }

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5050)
