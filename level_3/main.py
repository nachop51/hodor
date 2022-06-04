#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import pytesseract
import cv2

url_hodor = "http://158.69.76.135/level3.php"


def captcha_solver(session):
    captcha = session.get('http://158.69.76.135/captcha.php')
    with open('captcha.png', 'wb') as f:
        f.write(captcha.content)
    img = cv2.imread('captcha.png')
    # print(pytesseract.image_to_string(img).split('\n')[0], end=".")
    return pytesseract.image_to_string(img).split('\n')[0]


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
    while solved < 1024:
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
