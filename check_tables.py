import requests

URL = "https://ojhenudsmcvuiobpcqsv.supabase.co"
KEY = "sb_publishable_jtGvrWNZ5moIkQj1HwoWQQ_W5nFMfjE"

headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
}

def test_connection():
    names = ["Products", "products", "Product", "product", "Inventory", "Items", "items", "bakery_products"]
    for n in names:
        resp = requests.get(f"{URL}/rest/v1/{n}?limit=1", headers=headers)
        print(n, resp.status_code, resp.text[:100])

if __name__ == "__main__":
    test_connection()
