import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from datetime import datetime
import json
from urllib.request import urlopen
from tickers import TickerData


class Finance(object):
    def __init__(self):
        self.tickerData = TickerData()
        self.thread = Thread(target=self.run_yfinance)
        self.thread.daemon = True
        self.thread.start()
        # self.thread.join()

    def get_stocks_data(self, symbol: str) -> dict:
        try:
            url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules=price'.format(symbol=symbol)
            data = {}
            with urlopen(url, timeout=3) as connection:
                res = json.loads(connection.read())['quoteSummary']['result'][0]['price']
                data["regularMarketPrice"] = res['regularMarketPrice']
                data['regularMarketVolume'] = res['regularMarketVolume']
                data['regularMarketChangePercent'] = res['regularMarketChangePercent']
                return [symbol, data]
        except:
            # bad url, socket timeout, http forbidden, etc.
            return None

    def save_file(self,dict_data):
        with open('stock_data.json', 'w') as file:
            json.dump(dict_data, file)    

    def run_yfinance(self):
        stocks = self.tickerData.names_list()

        while True:
            with ThreadPoolExecutor(max_workers=4) as pool:
                results = pool.map(self.get_stocks_data, stocks)
            data = {}
            for r in results:
                data[r[0]] = r[1]
            self.save_file(data)
            now = datetime.now()
            print("Updated stock_data.json at", now)
            time.sleep(1800) # sleep for 30 minutes