import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
import json
import time
import logging
import requests
from datetime import datetime, timedelta

# Configuration
FETCH_URL = 'https://oqbhgishqhkteqpzyavt.supabase.co/functions/v1/get-ticker-data-v1'
SLEEP_INTERVAL = 60 # in minutes
STALE_THRESHOLD = 60 # in minutes

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE_PATH=os.path.join(PROJECT_ROOT, 'data', 'stocks-data.json')
LOG_FILE_PATH =  os.path.join(PROJECT_ROOT, 'logs', 'bloko-data.log')

# Setup logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def is_data_valid(data):
    if not isinstance(data, list) or not len(data) > 1:
        return False
    required_keys = {"symbol", "current_price", "regular_market_volume", "regular_market_change_percent"}
    return required_keys.issubset(data[0].keys())

def is_data_stale(file_path, threshold_minutes):
    if not os.path.exists(file_path):
        return True
    file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    return datetime.now() - file_mod_time > timedelta(minutes=threshold_minutes)

def fetch_and_save_data():
    try:
        response = requests.get(FETCH_URL, verify=False)
        response.raise_for_status()
        data = response.json()

        if not data:
            logging.warning("Fetched data is empty. Stocks file not updated.")
            return
        
        with open(DATA_FILE_PATH, 'w') as f:
            json.dump(response.json(), f)
        logging.info("Data fetched and saved successfully.")
    except requests.RequestException as e:
        logging.error(f"Failed to fetch data: {e}")

def main():
    while True:
        logging.info("Running data updater...")
        logging.info("Checking validity of pre-existing data...")
        if os.path.exists(DATA_FILE_PATH):
            with open(DATA_FILE_PATH, 'r') as f:
                try:
                    data = json.load(f)
                    if is_data_valid(data) and not is_data_stale(DATA_FILE_PATH, STALE_THRESHOLD):
                        logging.info("Valid and fresh data found in stocks file. Sleeping...")
                        time.sleep(SLEEP_INTERVAL * 60)
                        continue
                except json.JSONDecodeError:
                    logging.error("Failed to decode JSON data.")
        
        logging.info("Data is either not found, invalid or stale. Fetching new data...")
        fetch_and_save_data()
        logging.info(f"Sleeping for {SLEEP_INTERVAL} minutes...")
        time.sleep(SLEEP_INTERVAL * 60)

if __name__ == "__main__":
    main()