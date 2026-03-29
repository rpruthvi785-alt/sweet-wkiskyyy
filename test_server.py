import urllib.request
from urllib.error import URLError, HTTPError
import time

def test_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        return response.getcode()
    except HTTPError as e:
        return e.code
    except URLError as e:
        return str(e.reason)

if __name__ == "__main__":
    urls = [
        "http://127.0.0.1:5050/assets/images/hero.png",
        "http://127.0.0.1:5050/assets/images/about.png",
        "http://127.0.0.1:5050/assets/images/icon_preservatives.png",
        "http://127.0.0.1:5050/assets/images/icon_eggs.png",
        "http://127.0.0.1:5050/assets/images/icon_custom.png",
        "http://127.0.0.1:5050/assets/images/wild_berry_scone.png",
        "http://127.0.0.1:5050/assets/images/assorted_macaron_set.png"
    ]
    for url in urls:
        print(f"{url} -> {test_url(url)}")
