
# 
# Copyright (c) Carlos Tojal
# covid19
# 

import sys
import matplotlib.pyplot as plt
import datetime

from data import Data

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

dataManager = Data()

data = dataManager.get_data(country)

if data != "error":
    success = True

if success:

    success = False

    print(dataManager.get_confirmed(data))

    if study == "confirmed":
        data = dataManager.get_confirmed(data)
        plt.title("Confirmed")
        success = True

    elif study == "deaths":
        data = dataManager.get_deaths(data)
        plt.title("Deaths")
        success = True

    elif study == "recovered":
        data = dataManager.get_recovered(data)
        plt.title("Recovered")
        success = True

    else:
        print("Invalid study.")

    if success:
        plt.plot(data['dates'], data['values'])
        plt.plot(data['variations'])
        plt.xticks(data['dates'], data['dates'], rotation='vertical')
        plt.suptitle("COVID19 " + country.upper())
        plt.show()

        days_to_max = dataManager.estimate_days_to_max(data, 5, 3)

        if days_to_max == "error":
            print("Couldn't determine based on the given data.")
        else:
            print("Estimated days to maximum: " + str(days_to_max))

            date = datetime.datetime.strptime(data['dates'][len(data) - 1], "%d %B") + datetime.timedelta(days=days_to_max)
            date = date.strftime("%d %B")
            
            print("(" + date + ")")
