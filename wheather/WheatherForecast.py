import requests
import sys
import datetime
from os import path
import json
from os.path import getmtime


class WheatherForecast:
    def __init__(self, apikey):
        self.apikey = apikey
        self.dates = []
        self.datas = []
        self.description = []

    def __iter__(self):
        result = [date for date, value in self.items()]
        return iter(result)

    def __str__(self):
        return self.dates

    def __getitem__(self, item):
        self.date = item
        wf.read()
        data = wf.will_be_rain()
        return data

    def items(self):
        with open("out2.txt", "r", encoding="utf-8") as file:
            datas = json.loads(file.read())["v3-wx-forecast-daily-15day"]
            for number, date in enumerate(datas["validTimeUtc"]):
                date1 = datetime.datetime.utcfromtimestamp(date).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                )
                date = date1[0:10]
                description = datas["narrative"][number]
                opady = ["rain", "Rain", "snow", "Snow"]
                for opad in opady:
                    if opad in description:
                        yield date, "Będzie padać"
                        break
                else:
                    yield date, "Nie będzie padać"
                    self.dates.append(date)

    def will_be_rain(self):
        print("weszło")
        with open("out2.txt", "r", encoding="utf-8") as file:
            datas = json.loads(file.read())
            date = datas["v3-wx-forecast-daily-15day"]["validTimeUtc"][0]
            date1 = datetime.datetime.utcfromtimestamp(date).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
            date = date1[0:10]
            description = datas["v3-wx-forecast-daily-15day"]["narrative"][0]
            opady = ["rain", "Rain", "snow", "Snow"]
        for opad in opady:
            if opad in description:
                return "Będzie padać"
            else:
                return "Nie będzie padać"

    def read(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        today = datetime.datetime.fromordinal(yesterday.toordinal())

        if path.exists("out2.txt") and getmtime("out2.txt") >= today.timestamp():
            with open("out2.txt", "r", encoding="utf-8") as file:
                datas = json.loads(file.read())
        else:
            datas = self.api_read()
        return datas

    def file_read(self):
        print("weszło")
        with open("out2.txt", "r", encoding="utf-8") as file:
            datas = json.loads(file.read())
            date = datas["v3-wx-forecast-daily-15day"]["validTimeUtc"][0]
            description = datas["v3-wx-forecast-daily-15day"]["narrative"][0]
            return date, description

    def api_read(self):
        print("odczyt z api")
        url = "https://weather338.p.rapidapi.com/weather/forecast"
        querystring = {
            "date": user_date,
            "latitude": "51.114",
            "longitude": "17.021",
            "language": "en-US",
            "units": "m",
        }
        with open(sys.argv[1]) as file:
            apikey = file.read().strip()

        headers = {
            "x-rapidapi-host": "weather338.p.rapidapi.com",
            "x-rapidapi-key": apikey,
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring
        )

        with open("out2.txt", "w", encoding="utf-8") as file:
            file.write(response.text)
        return response.json()


wf = WheatherForecast(sys.argv[1])

if len(sys.argv) <= 2:
    d = datetime.date.today() + datetime.timedelta(+1)
    user_date = str(d).replace("-", "")
else:
    user_date = sys.argv[2].replace("-", "")

wf.read()
wf.items()
print(wf[user_date])
for date in wf:
    print(date)
for date, value in wf.items():
    print(date, value)

