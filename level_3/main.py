#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from captcha_solver import CaptchaSolver

url_hodor = "http://158.69.76.135/level3.php"


def captcha_solver(session):
    captcha = session.get('http://158.69.76.135/captcha.php')
    with open('captcha.png', 'wb') as f:
        f.write(captcha.content)
    solver = CaptchaSolver('browser')
    raw_data = open('captcha.png', 'rb').read()
    return solver.solve_captcha(raw_data)


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


with requests.session() as session:
    for i in range(2):
        data = current_session(session)
        res = session.post(
            url=url_hodor,
            data=data["session"],
            headers=data["headers"],
        )
        print(res.text)
        if res.status_code == 200:
            print(f"Vote count:{i + 1}")

captcha_link = "http://158.69.76.135/captcha.php"
