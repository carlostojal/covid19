
# 
# Copyright (c) Carlos Tojal
# covid19
# 

import sys
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import json

try:
    country = sys.argv[1].lower()
except:
    print("No country defined. PT set.")
    country = "pt"

try:
    study = sys.argv[2].lower()
except:
    print("No study defined. Confirmed set.")
    study = "confirmed"

print("Starting...")

f = open("data/" + country + ".json", "r")
data = json.loads(f.read())
f.close()
print("Got data.")
success = True

"""
try:
    print("Getting data...")
    r = requests.get('https://api.covid19api.com/country/' + country)
    f = open("data/" + country + ".json", "w")
    f.write(r)
    f.close()
    data = r.json()
    print("Got data.")
    success = True
except:
    print("Error getting data.")
    success = False
"""

if success:
    confirmed = []
    deaths = []
    recovered = []
    date = []

    confirmed_variations = []

    for i in range(len(data)):
        confirmed1 = int(data[i]['Confirmed'])
        deaths1 = int(data[i]['Deaths'])
        recovered1 = int(data[i]['Recovered'])
        date1 = data[i]['Date']
        if confirmed1 > 0 or deaths1 > 0 or recovered1 > 0:
            confirmed.append(confirmed1)
            # calculate variation
            if i == 0:
                confirmed_variations.append(0)
            else:
                confirmed_variations.append(int(int(data[i]['Confirmed']) - int(data[i-1]['Confirmed'])))
            deaths.append(deaths1)
            recovered.append(recovered1)
            # format date
            date1 = date1.replace('T', ' ')
            date1 = date1.replace('Z', '')
            date1 = datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
            date.append(date1.strftime("%d %B"))

    print(confirmed_variations)

    success = False

    if study == "confirmed":
        plt.plot(date, confirmed)
        plt.plot(confirmed_variations)
        plt.title("Confirmed")
        plt.xticks(date, date, rotation='vertical')
        success = True

    elif study == "deaths":
        plt.plot(date, deaths)
        plt.title("Deaths")
        plt.xticks(date, date, rotation='vertical')
        success = True

    elif study == "recovered":
        plt.plot(date, recovered)
        plt.title("Recovered")
        plt.xticks(date, date, rotation='vertical')
        success = True

    else:
        print("Invalid study.")

    if success:
        plt.suptitle("COVID19 " + country.upper())
        plt.show()
