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
        self.thread = Thread(target=self.run_yfinance)
        self.thread.daemon = True
        self.thread.start()

    def get_stocks_data(self, symbol: str) -> dict:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.info
            print("yfinance data",data)
            regular_market_previous_close = data.get('regularMarketPreviousClose')
            regular_market_open = data.get('regularMarketOpen')
            
            regular_market_change_percent = calculate_regular_market_change_percent(regular_market_previous_close, regular_market_open)
            stock_data = {
                "currentPrice": data.get('currentPrice'),
                "regularMarketVolume": data.get('regularMarketVolume'),
                "regularMarketChangePercent": regular_market_change_percent
            }
            return [symbol, stock_data]
        except Exception as e:
            print("Error on get_stocks_data(). Processing:",symbol ,"Error:", e)
            return None

    def save_file(self, dict_data):
        try:
            with open('stock_data.json', 'w') as file:
                json.dump(dict_data, file)
        except Exception as e:
            print("Error while saving stock data to file:", e)

    def run_yfinance(self):
        stocks = self.tickerData.names_list()
        while True:
            data = {}
            try:
                for symbol in stocks:
                    result = self.get_stocks_data(symbol)
                    if result:
                        data[result[0]] = result[1]
                self.save_file(data)
                print("Updated stock_data.json at", datetime.now())
            except Exception as e:
                print("ERROR run_yfinance.py, problem getting data from Yahoo Finance:", e)
            time.sleep(30)  # sleep for 30 seconds

# Example usage
if __name__ == "__main__":
    finance = Finance()
    finance.thread.join()  # This will keep the main thread running
