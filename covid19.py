
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

success = False

if data != "error":
    success = True

if success:

    success = False

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

        days_to_target = dataManager.estimate_days_to_max(data, dataManager.get_config()['estimate_from'])
        int_days_to_target = days_to_target[0]
        estimated_values = days_to_target[1]

        if days_to_target == "error":
            print("Couldn't determine based on the given data.")
        else:
            print("Estimated days to " + dataManager.get_config()['estimate_until'] + ": " + str(int_days_to_target))

            date = datetime.datetime.strptime(data['dates'][len(data['dates']) - 1], "%d %B %Y") + datetime.timedelta(days=int_days_to_target)
            date = date.strftime("%d %B %Y")
            
            print("(" + date + ")")

            plt.plot(estimated_values)
            plt.plot(data['dates'], data['values'])
            plt.xticks(data['dates'], data['dates'], rotation='vertical')
            plt.suptitle("Estimated " + dataManager.get_config()['estimate_until'] + " in " + country.upper())
            plt.show()
