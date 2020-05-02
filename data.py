
import json
import requests
from datetime import datetime
import numpy as np

class Data:

    def format_date(self, date):
        date1 = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        return date1.strftime("%d %B %Y")

    def get_config(self):
        f = open("config.json", "r")
        config = json.loads(f.read())
        f.close()
        return config

    def get_data(self, country):
        existent_data = False
        try:
            f = open("data/" + country + ".json", "r")
            data = json.loads(f.read())
            f.close()
            existent_data = True
        except:
            print("No existent data. Getting from server.")
            existent_data = False
        
        try:
            # request server
            r = requests.get('https://api.covid19api.com/country/' + country)
            # write to file
            f = open("data/" + country + ".json", "w")
            f.write(r.text)
            f.close()
            data = r.json()
            return data
        except:
            print("Error getting data.")
            if existent_data:
                print("Will use existent data")
                return data
            return "error"

    def get_confirmed(self, data):
        confirmed = {}
        confirmed['values'] = []
        confirmed['variations'] = []
        confirmed['dates'] = []

        for i in range(len(data)):
            confirmed1 = int(data[i]['Confirmed'])
            if confirmed1 > 0:
                confirmed['values'].append(confirmed1)
                if i == 0:
                    confirmed['variations'].append(0)
                else:
                    confirmed['variations'].append(confirmed1 - int(data[i-1]['Confirmed']))
                confirmed['dates'].append(self.format_date(data[i]['Date']))

        return confirmed
    
    def get_deaths(self, data):
        deaths = {}
        deaths['values'] = []
        deaths['variations'] = []
        deaths['dates'] = []

        for i in range(len(data)):
            deaths1 = int(data[i]['Deaths'])
            if deaths1 > 0:
                deaths['values'].append(deaths1)
                if i == 0:
                    deaths['variations'].append(0)
                else:
                    deaths['variations'].append(deaths1 - int(data[i-1]['Deaths']))
                deaths['dates'].append(self.format_date(data[i]['Date']))
        
        return deaths
    
    def get_recovered(self, data):
        recovered = {}
        recovered['values'] = []
        recovered['variations'] = []
        recovered['dates'] = []

        for i in range(len(data)):
            recovered1 = int(data[i]['Recovered'])
            if recovered1 > 0:
                recovered['values'].append(recovered1)
                if i == 0:
                    recovered['variations'].append(0)
                else:
                    recovered['variations'].append(recovered1 - int(data[i-1]['Recovered']))
                recovered['dates'].append(self.format_date(data[i]['Date']))
        
        return recovered

    def estimate_days_to_max(self, data, n_days):
        n_days = int(n_days)
        print("Estimating from the last " + str(n_days) + " days...")
        average_variation = 0
        days_variation = []
        calculated_values = []
        i = len(data['variations']) - n_days - 1
        # fill array with existent data until estimated values
        for x in range(i):
            calculated_values.append(data['values'][x])
        # save daily variation to array
        while i < len(data['variations']) - 1:
            days_variation.append(data['variations'][i] - data['variations'][i+1])
            i += 1
        # calculate average variation
        average_variation = np.mean(days_variation)
        # if the variation is positive (each day there are less occurences)
        if average_variation > 0:
            days = 0
            current_value = data['values'][len(data['values']) - n_days - 1] # current number of occurences
            current_variation = data['variations'][len(data['variations'])  - n_days - 1] # current variation
            target = self.get_config()['estimate_until']
            if target != "zero":
                target = "max"
            if target == "zero":
                while current_value > 0:
                    calculated_values.append(current_value)
                    current_value += current_variation
                    current_variation -= average_variation
                    days += 1 # one more day is needed to the occurences reach 0
            else:
                while current_variation > 0:
                    calculated_values.append(current_value)
                    current_value += current_variation
                    current_variation -= average_variation
                    days += 1 # one more day is needed to the occurences reach 0
            return [days, calculated_values]
        return "error"