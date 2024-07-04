import time
from threading import Thread
from datetime import datetime
import json
import yfinance as yf
from tickers import TickerData
    
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
        self.run_yfinance()

    def create_json_file_from_data(self, data):
        result = {}
        for ticker in data.columns.levels[0]:
            ticker_data = data[ticker].iloc[0]  # Get the first row of the ticker data
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
            data = {}
            try:
                data = yf.download(
                tickers=stocks,
                period='1d',
                interval='1d',
                group_by='ticker',
                auto_adjust=False,
                prepost=False,
                threads=True,
                proxy=None)
                self.create_json_file_from_data(data)
                print("Updated stock_data.json at", datetime.now())
            except Exception as e:
                print("ERROR run_yfinance.py, problem getting data from Yahoo Finance:", e)
            time.sleep(30)  # sleep for 30 seconds

# Example usage
if __name__ == "__main__":
    finance = Finance()
    # finance.thread.join()  # This will keep the main thread running
