import time
from datetime import datetime
import json
import yfinance as yf
from tickers import TickerData
import threading

def calculate_regular_market_change_percent(previous_close, market_open):
    try:
        change_percent = ((market_open - previous_close) / previous_close) * 100
        return change_percent
    except ZeroDivisionError:
        return None  # Handle the case where previous_close is zero

class Finance(object):
    """Object dedicated to update the stocks_data.json file with fresh numbers from the API"""
    def __init__(self):
        self.tickerData = TickerData()
        self.start_yfinance_thread()

    def create_json_file_from_data(self, data):
        result = {}
        for ticker in data.columns.levels[0]:
            ticker_data = data[ticker].iloc[0]
            result[ticker] = {
                "currentPrice": ticker_data['Close'],
                "regularMarketVolume": ticker_data['Volume'],
                "regularMarketChangePercent": (ticker_data['Close'] - ticker_data['Open']) / ticker_data['Open'] * 100
            }
        with open('stock_data.json', 'w') as file:
            print("Saving data to file..")
            json.dump(result, file)

    def run_yfinance(self):
        stocks = self.tickerData.names_list()
        while True:
            try:
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
                self.create_json_file_from_data(data)
                print("Updated stock_data.json at", datetime.now())
            except Exception as e:
                print("ERROR run_yfinance.py, problem getting data from Yahoo Finance:", e)
            time.sleep(43200)  # sleep for 30 seconds

    def start_yfinance_thread(self):
        yfinance_thread = threading.Thread(target=self.run_yfinance)
        yfinance_thread.daemon = True  # This allows the thread to be killed when the main program exits
        yfinance_thread.start()

# Example usage
if __name__ == "__main__":
    finance = Finance()
