
import json
import requests
from datetime import datetime
import numpy as np

class Data:

    def format_date(self, date):
        date1 = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        return date1.strftime("%d %B")

    def get_data(self, country):
        try:
            """
            # request server
            r = requests.get('https://api.covid19api.com/country/' + country)
            # write to file
            f = open("data/" + country + ".json", "w")
            f.write(r)
            f.close()
            data = r.json()
            """
            f = open("data/" + country + ".json", "r")
            data = json.loads(f.read())
            return data
        except:
            print("Error getting data.")
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

    def estimate_days_to_max(self, data, period_length, n_periods):
        print("Estimating from the last " + str(int(period_length * n_periods)) + " days...")
        periods = np.array_split(data['variations'], int(len(data['variations']) / period_length))
        periods1 = []
        periods_variation = []
        average_variation = 0
        for p in periods:
            periods1.append(np.mean(p))
        i = len(periods1) - n_periods - 1
        while i < len(periods1) - 1:
            periods_variation.append(periods1[i] - periods1[i+1])
            i += 1
        average_variation = np.mean(periods_variation)
        print(average_variation)
        if average_variation > 0:
            days = (data['values'][len(data['values']) - 1] / average_variation) * period_length
            print("Accuracy on existent data: " + str(self.calculate_accuracy(data['variations'], average_variation, (period_length * n_periods))) + "%")
            return days
        return "error"
    
    def calculate_accuracy(self, data, average_variation, n_days):
        accuracies = []
        i = len(data) - n_days - 1
        # i = 0
        estimated_value = data[i]
        while i < len(data):
            if data[i] > 0:
                accuracies.append(estimated_value / data[i])
                estimated_value -= average_variation
            i += 1
        return abs(np.mean(accuracies) * 100)