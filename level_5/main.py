#!/usr/bin/python3
import cv2
import pytesseract
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageFilter

url_hodor = "http://158.69.76.135/level5.php"


def prepare_image(img):
    """Transform image to greyscale and blur it"""
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    if 'L' != img.mode:
        img = img.convert('L')
    return img


def remove_noise(img, pass_factor):
    for column in range(img.size[0]):
        for line in range(img.size[1]):
            value = remove_noise_by_pixel(img, column, line, pass_factor)
            img.putpixel((column, line), value)
    return img


def remove_noise_by_pixel(img, column, line, pass_factor):
    if img.getpixel((column, line)) < pass_factor:
        return (0)
    return (255)


def process_image():
    img = Image.open('captcha.png')
    img = prepare_image(img)
    img = remove_noise(img, 90)
    img.save('captcha.png')


def captcha_solver(session):
    captcha = session.get('http://158.69.76.135/tim.php')
    with open('captcha.png', 'wb') as f:
        f.write(captcha.content)
    process_image()
    img = cv2.imread('captcha.png')
    print(pytesseract.image_to_string(img), end=".")
    return pytesseract.image_to_string(img)


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
        print(res.text)
        if 'See you later' in res.text:
            print("Captcha failed")
        else:
            solved += 1
            print(f"Vote count: {solved}")
        total += 1
        print(f"Summary: {solved}/{total}")
