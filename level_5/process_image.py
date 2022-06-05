#!/usr/bin/python3
from io import BytesIO
from PIL import Image
import requests
import pytesseract


def process_image(session):
    captcha = session.get('http://158.69.76.135/tim.php')
    with open('captcha.png', 'wb') as f:
        f.write(captcha.content)
    img = Image.open(BytesIO(captcha.content))
    noise = []
    for y in range(img.height):
        for x in range(img.width):
            pixel_color = img.getpixel((x, y))
            if pixel_color == (0, 0, 0):
                noise.append((x, y))
            elif pixel_color == (128, 128, 128):
                img.putpixel((x, y), (255, 255, 255))
    for pixel in noise:
        img.putpixel(pixel, (255, 255, 255))
    colours = []
    for y in range(img.height):
        for x in range(img.width):
            pixel_color = img.getpixel((x, y))
            if pixel_color != (255, 255, 255):
                colours.append(pixel_color)
    img.save('captcha.png')
    print(pytesseract.image_to_string(img).split('\n')[0], end=".\n")
    return pytesseract.image_to_string(img).split('\n')[0]
