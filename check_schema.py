import requests

URL = "https://ojhenudsmcvuiobpcqsv.supabase.co"
KEY = "sb_publishable_jtGvrWNZ5moIkQj1HwoWQQ_W5nFMfjE"

headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
}

def test_connection():
    resp = requests.get(f"{URL}/rest/v1/", headers=headers)
    print("OpenAPI spec:", resp.status_code)
    print("Response text:", resp.text)

if __name__ == "__main__":
    test_connection()
