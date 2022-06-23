import csv
import json
import time
from datetime import datetime
from datetime import date
import math



def datetime_dict(data):
    dt_data = {}
    for key in data.keys():
        print(key)
        dt = datetime.fromtimestamp(int(key)/1000)
        dt_data[dt] = data[key]
    return dt_data

def interpolate_vals(x):
    out = min_date_val + (x-min_date)*((max_date_val - min_date_val)/(max_date - min_date))
    return out

def epoch_to_datetime(epoch):
    return datetime.fromtimestamp(int(epoch)/1000)


# read json
with open('debt_predictions.json') as json_file:
    data = json.load(json_file)

    # replace dict keys with datetimes
    #dt_data = datetime_dict(data)

    # get current time

    now = math.floor(time.time()*1000) # epoch
    #now = datetime.now()
    #now = datetime(2019, 5, 17)
    dates_in_data = data.keys()

    country_name = "Argentina"

    # get data ranges
    before = []
    after = []
    for d in dates_in_data:
        current_date = int(d)
        if current_date > now:
            after.append(current_date)
        if current_date < now:
            before.append(current_date)
    
    if after:
        max_date = min(after)
    else:
        max_date = None
    
    if before:
        min_date = max(before)
    else: 
        min_date = None
    
    # make it so that if now is after max available date it will only displat latest value in dataset

    print(min_date, max_date)
    if min_date and max_date:
        min_date_val = data[str(min_date)][country_name]
        max_date_val = data[str(max_date)][country_name]
        print("country",country_name)
        print("now",epoch_to_datetime(now))
        print("min_date",epoch_to_datetime(min_date))
        print("max_date",epoch_to_datetime(max_date))
        print("min_date_val",min_date_val)
        print("max_date_val",max_date_val)

        # now we interpolate
        
    else:
        print("No data available in debt_predictions.json that matches the current time.")


