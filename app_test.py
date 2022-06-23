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

def epoch_to_datetime(epoch):
    return datetime.fromtimestamp(int(epoch)/1000)

def interpolate_vals(x, x1, y1, x2, y2):
    out = y1 + (x - x1) * ((y2 - y1) / (x2 - x1))
    return math.floor(out)

def read_forecast_file():
    f = open('debt_predictions.json')
    debt_preds_data = json.load(f)
    f.close()
    return debt_preds_data

def read_gdp_file():
    f = open('gdp.json')
    #print(f.read())
    gdp_data = json.load(f)
    gdp_data = json.loads(gdp_data)
    f.close()
    return gdp_data


debt_preds_data = read_forecast_file()
gdp_data = read_gdp_file()

# get current time
now = math.floor(time.time()*1000) # epoch
dates_in_data = debt_preds_data.keys()

country_name = "St. Vincent and the Grenadines"

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

if min_date and max_date:
    min_date_val = debt_preds_data[str(min_date)][country_name]
    max_date_val = debt_preds_data[str(max_date)][country_name]
    print("country",country_name)
    print("now",epoch_to_datetime(now))
    print("min_date",epoch_to_datetime(min_date))
    print("max_date",epoch_to_datetime(max_date))
    print("min_date_val",min_date_val)
    print("max_date_val",max_date_val)

    # now we interpolate
    interpolated_debt = interpolate_vals(now, min_date, min_date_val,max_date, max_date_val)
    print("interpolated", interpolated_debt)
    time_key = list(gdp_data.keys())[0]
    gdp = gdp_data[time_key][country_name]
    print("gdp", gdp)
    # how many times larger is the debt with respect to the gdp
    print("GDP %", (interpolated_debt/gdp)*100)
else:
    print("No data available in debt_predictions.json that matches the current time.")


