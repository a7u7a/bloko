import yfinance as yf
import json
from tickers import TickerData

tickerData = TickerData()

data = yf.download(
        tickers = tickerData.names_list(),
        period = '1d',
        interval = '1d',
        group_by = 'ticker',
        auto_adjust = False,
        prepost = False,
        threads = True,
        proxy = None
    )
print("Result:", data)