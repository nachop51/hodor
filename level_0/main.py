#!/usr/bin/python3
import requests

parameters = {
    "id": "4386",
    "holdthedoor": "Submit",
}

for i in range(1024):
    res = requests.post(
        url="http://158.69.76.135/level0.php", data=parameters)
