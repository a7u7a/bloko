#!/usr/bin/env python
import json
class TickerData(object):
    def __init__(self):
        self.tickers = json.loads("""{
        "tickers": [
             {
                "name":"TSLA",
                "image_path": "./images/tesla.ppm"
            },
            {
                "name":"MSFT",
                "image_path": "./images/microsoft.ppm"
            },{
                "name":"AMZN",
                "image_path": "./images/amazon.ppm"
            },
            {
                "name":"BTC",
                "image_path": "./images/bitcoin.ppm"
            }
        ]
        }"""
         )["tickers"]

    def names_list(self):
        list =[]
        for ticker in self.tickers:
            list.append(ticker['name'])
        return list