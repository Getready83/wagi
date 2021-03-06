import requests
import sys
import datetime
from os import path
import json
from os.path import getmtime


if len(sys.argv) <= 2:
    d = datetime.date.today() + datetime.timedelta(+1)
    date = str(d).replace("-", "")
else:
    date = sys.argv[2].replace("-", "")

today = datetime.date.today()
today = datetime.datetime.fromordinal(today.toordinal())

if path.exists("out1.txt") and getmtime("out1.txt") >= today.timestamp():
    print("odczyt z pliku")
    with open("out1.txt", "r", encoding="utf-8") as file:
        data = json.loads(file.read())

else:
    print("odczyt z api")
    url = "https://weather338.p.rapidapi.com/weather/forecast"

    querystring = {
        "date": date,
        "latitude": "51.114",
        "longitude": "17.021",
        "language": "en-US",
        "units": "m",
    }

    with open(sys.argv[1]) as file:
        apikey = file.read().strip()

    headers = {"x-rapidapi-host": "weather338.p.rapidapi.com", "x-rapidapi-key": apikey}

    response = requests.request("GET", url, headers=headers, params=querystring)

    with open("out1.txt", "w", encoding="utf-8") as file:
        file.write(response.text)
    data = response.json()
description = data["v3-wx-forecast-daily-15day"]["narrative"]
for days in description:
    opad = "rain" or "Rain" or "snow" or "Snow"
    if opad in days:
        print("będzie padać")
    else:
        print("nie będzie padać")
