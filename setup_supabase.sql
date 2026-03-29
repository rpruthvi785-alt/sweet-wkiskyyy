-- 1. Create the `users` table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- 2. Create the `products` table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    description TEXT,
    price REAL,
    image_path TEXT,
    is_bestseller INTEGER DEFAULT 0
);

-- 3. Create the `orders` table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    order_type TEXT DEFAULT 'dine-in',
    status TEXT DEFAULT 'received',
    ordered_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
    custom_details TEXT
);

-- 4. Disable Row Level Security (RLS) temporarily so the Anonymous key can read/write
-- Alternatively, you can create policies for each table via the Supabase Dashboard
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE products DISABLE ROW LEVEL SECURITY;
ALTER TABLE orders DISABLE ROW LEVEL SECURITY;
