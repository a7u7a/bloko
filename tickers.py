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
            },
            {
                "name":"AMZN",
                "image_path": "./images/amazon.ppm"
            },
            {
                "name":"BTC-USD",
                "image_path": "./images/bitcoin.ppm"
            },
            {
                "name":"BP",
                "image_path": "./images/bp.ppm"
            },
            {
                "name":"AAPL",
                "image_path": "./images/apple.ppm"
            },
            {
                "name":"ABT",
                "image_path": "./images/abbott.ppm"
            },
            {
                "name":"ACN",
                "image_path": "./images/accenture.ppm"
            },
            {
                "name":"ADBE",
                "image_path": "./images/adobe.ppm"
            },          
            {
                "name":"ASML",
                "image_path": "./images/asml.ppm"
            },
            {
                "name":"AVGO",
                "image_path": "./images/broadcom.ppm"
            },
            {
                "name":"CMCSA",
                "image_path": "./images/comcast.ppm"
            },     
            {
                "name":"COST",
                "image_path": "./images/cosco.ppm"
            }, 
            {
                "name":"CSCO",
                "image_path": "./images/cisco.ppm"
            },
            {
                "name":"CVX",
                "image_path": "./images/chevron.ppm"
            },
            {
                "name":"DIS",
                "image_path": "./images/disney.ppm"
            },                
            {
                "name":"FB",
                "image_path": "./images/meta.ppm"
            },
            {
                "name":"GOOGL",
                "image_path": "./images/google.ppm"
            },          
            {
                "name":"HD",
                "image_path": "./images/homedepot.ppm"
            },
            {
                "name":"JNJ",
                "image_path": "./images/jhonson.ppm"
            },
            {
                "name":"JPM",
                "image_path": "./images/chase.ppm"
            },
            {
                "name":"KO",
                "image_path": "./images/coca.ppm"
            },
            {
                "name":"MA",
                "image_path": "./images/mastercard.ppm"
            },
            {
                "name":"NKE",
                "image_path": "./images/nike.ppm"
            },
            {
                "name":"NVDA",
                "image_path": "./images/nvidia.ppm"
            },
            {
                "name":"PEP",
                "image_path": "./images/pepsi.ppm"
            },
            {
                "name":"PFE",
                "image_path": "./images/pfizer.ppm"
            },
            {
                "name":"PRDSY",
                "image_path": "./images/prada.ppm"
            },                
            {
                "name":"SHEL",
                "image_path": "./images/shell.ppm"
            },
            {
                "name":"SSNLF",
                "image_path": "./images/samsung.ppm"
            },

            {
                "name":"TM",
                "image_path": "./images/toyota.ppm"
            },
            {
                "name":"V",
                "image_path": "./images/visa.ppm"
            },
            {
                "name":"VZ",
                "image_path": "./images/verizon.ppm"
            },
            {
                "name":"WMT",
                "image_path": "./images/wallmart.ppm"
            },
            {
                "name":"XOM",
                "image_path": "./images/exxon.ppm"
            },
            {
                "name":"UNH",
                "image_path": "./images/uhg.ppm"
            },
            {
                "name":"BAC",
                "image_path": "./images/bankofamerica.ppm"
            }                             
        ]
        }"""
         )["tickers"]

    def names_list(self):
        list =[]
        for ticker in self.tickers:
            list.append(ticker['name'])
        return list

