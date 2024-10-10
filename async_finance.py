import os, os.path
import time
from datetime import datetime
import json
import yfinance as yf
from tickers import TickerData
import threading
import logging
import pandas as pd

# Ensure the log directory exists
log_directory = '/home/pi/bloko/logs/'
data_directory = '/home/pi/bloko/data/'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up logging configuration
logging.basicConfig(
    filename=os.path.join(log_directory, 'async_yfinance.log'), 
    level=logging.INFO,  # Set to DEBUG to capture all types of logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def calculate_regular_market_change_percent(previous_close, market_open):
    try:
        change_percent = ((market_open - previous_close) / previous_close) * 100
        return change_percent
    except ZeroDivisionError:
        logging.error("ZeroDivisionError: previous_close was zero.")
        return None  # Handle the case where previous_close is zero

class Finance(object):
    """Object dedicated to update the stocks_data.json file with fresh numbers from the API"""
    def __init__(self):
        logging.info("init Finance class")
        self.tickerData = TickerData()
        self.start_yfinance_thread()

    def create_json_file_from_data(self, data):
        result = {}
        for ticker in data.columns.levels[0]:
            ticker_data = data[ticker]
            if not ticker_data.empty and 'Close' in ticker_data.columns and 'Open' in ticker_data.columns:
                close = ticker_data['Close'].iloc[-1]
                open_price = ticker_data['Open'].iloc[-1]
                volume = ticker_data['Volume'].iloc[-1] if 'Volume' in ticker_data.columns else None

                if not pd.isna(close) and not pd.isna(open_price) and open_price != 0:
                    rmcp = (close - open_price) / open_price * 100
                    result[ticker] = {
                        "currentPrice": float(close),
                        "regularMarketVolume": int(volume) if volume is not None else None,
                        "regularMarketChangePercent": float(rmcp)
                    }
                else:
                    logging.warning(f"Invalid Close or Open price for ticker {ticker}")
            else:
                logging.warning(f"No valid data returned for ticker {ticker}")

        # Write the result to a JSON file
        with open(os.path.join(self.data_directory, 'stock_data.json'), 'w') as f:
            json.dump(result, f, indent=2)

    def run_yfinance(self):
        stocks = self.tickerData.names_list()
        
        while True:
            try:
                logging.info("Attempting to download data from Yahoo Finance")
                data = yf.download(
                    tickers=stocks,
                    period='1d',
                    interval='1d',
                    group_by='ticker',
                    auto_adjust=False,
                    prepost=False,
                    threads=False,
                    proxy=None
                )
                logging.info("Data downloaded successfully")
                
                # Log the structure of the data
                logging.info(f"Downloaded data shape: {data.shape}")
                logging.info(f"Downloaded data columns: {data.columns}")
                logging.info(f"First few rows of data:\n{data.head()}")

                self.create_json_file_from_data(data)
                logging.info(f"Updated stock_data.json")
            except Exception as e:
                logging.exception(f"ERROR run_yfinance(), problem getting data from Yahoo Finance: {e}")
            time.sleep(86400) # Sleep for 24 hrs

    def start_yfinance_thread(self):
        logging.info("Starting thread")
        yfinance_thread = threading.Thread(target=self.run_yfinance)
        yfinance_thread.daemon = True  # This allows the thread to be killed when the main program exits
        yfinance_thread.start()
        logging.info("Thread started ok!")
        yfinance_thread.join()

if __name__ == "__main__":
    logging.info("Starting Finance daemon")
    finance = Finance()
