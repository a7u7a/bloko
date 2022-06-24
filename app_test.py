import json
import time
from datetime import datetime
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

def get_country_list(debt_preds_data):
    # assumes items have been sorted beforehand
    latest_item = list(debt_preds_data.keys())[0]
    return list(debt_preds_data[latest_item].keys())

def get_date_range(now, dates_in_data):
    """Returns the date range within the provided date ranges('dates_in_data') with respect to 'now '
    For instance: if now: 2022-6-2 then ranges should be min_date: 2022-1-1, max_date: 2023-1-1. As long as these dates can be found in the data."""
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

    return (min_date, max_date)

def get_gdp(country_name, gtp_data):
    time_key = list(gdp_data.keys())[0]
    return gdp_data[time_key][country_name]

# get data
debt_preds_data = read_forecast_file()
gdp_data = read_gdp_file()
dates_in_data = debt_preds_data.keys()

countries = get_country_list(debt_preds_data)

for country_name in countries:

    # get current time
    now = math.floor(time.time()*1000) # epoch

    min_date, max_date = get_date_range(now, dates_in_data)

    # handle case where now is outside range of available dates

    if min_date and max_date:
        min_date_debt = debt_preds_data[str(min_date)][country_name]
        max_date_debt = debt_preds_data[str(max_date)][country_name]
        
        # print("country",country_name)
        # print("now",epoch_to_datetime(now))
        # print("min_date",epoch_to_datetime(min_date))
        # print("max_date",epoch_to_datetime(max_date))
        # print("min_date_debt",min_date_debt)
        # print("max_date_debt",max_date_debt)

        # now we interpolate
        debt_now = interpolate_vals(now, min_date, min_date_debt, max_date, max_date_debt)
        # print("interpolated", debt_now)
        
        gdp = get_gdp(country_name, gdp_data)
        # how many times larger is the debt with respect to the gdp
        gdp_perc = (debt_now/gdp)*100
        # print("gdp", gdp)
        
        print(country_name, "debt now: $"+ str(debt_now),"GDP%:",gdp_perc )
    else:
        print("No data available in debt_predictions.json that matches the current time.")


