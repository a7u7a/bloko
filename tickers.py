#!/usr/bin/env python
import json
class TickerData(object):
    def __init__(self):
        self.tickers = json.loads("""{
        "tickers": [
            {
                "name":"TSLA",
                "image_path": "./images/tickers/tesla.ppm"
            },
            {
                "name":"MSFT",
                "image_path": "./images/tickers/microsoft.ppm"
            },
            {
                "name":"AMZN",
                "image_path": "./images/tickers/amazon.ppm"
            },
            {
                "name":"BP",
                "image_path": "./images/tickers/bp.ppm"
            },
            {
                "name":"AAPL",
                "image_path": "./images/tickers/apple.ppm"
            },
            {
                "name":"ABT",
                "image_path": "./images/tickers/abbott.ppm"
            },
            {
                "name":"ACN",
                "image_path": "./images/tickers/accenture.ppm"
            },
            {
                "name":"ADBE",
                "image_path": "./images/tickers/adobe.ppm"
            },          
            {
                "name":"ASML",
                "image_path": "./images/tickers/asml.ppm"
            },
            {
                "name":"AVGO",
                "image_path": "./images/tickers/broadcom.ppm"
            },
            {
                "name":"CMCSA",
                "image_path": "./images/tickers/comcast.ppm"
            },     
            {
                "name":"COST",
                "image_path": "./images/tickers/cosco.ppm"
            }, 
            {
                "name":"CSCO",
                "image_path": "./images/tickers/cisco.ppm"
            },
            {
                "name":"CVX",
                "image_path": "./images/tickers/chevron.ppm"
            },
            {
                "name":"DIS",
                "image_path": "./images/tickers/disney.ppm"
            },                
            {
                "name":"META",
                "image_path": "./images/tickers/meta.ppm"
            },
            {
                "name":"GOOGL",
                "image_path": "./images/tickers/google.ppm"
            },          
            {
                "name":"HD",
                "image_path": "./images/tickers/homedepot.ppm"
            },
            {
                "name":"JNJ",
                "image_path": "./images/tickers/jhonson.ppm"
            },
            {
                "name":"JPM",
                "image_path": "./images/tickers/chase.ppm"
            },
            {
                "name":"KO",
                "image_path": "./images/tickers/coca.ppm"
            },
            {
                "name":"MA",
                "image_path": "./images/tickers/mastercard.ppm"
            },
            {
                "name":"NKE",
                "image_path": "./images/tickers/nike.ppm"
            },
            {
                "name":"NVDA",
                "image_path": "./images/tickers/nvidia.ppm"
            },
            {
                "name":"PEP",
                "image_path": "./images/tickers/pepsi.ppm"
            },
            {
                "name":"PFE",
                "image_path": "./images/tickers/pfizer.ppm"
            },
            {
                "name":"PRDSY",
                "image_path": "./images/tickers/prada.ppm"
            },                
            {
                "name":"SHEL",
                "image_path": "./images/tickers/shell.ppm"
            },
            {
                "name":"SSNLF",
                "image_path": "./images/tickers/samsung.ppm"
            },
            {
                "name":"TM",
                "image_path": "./images/tickers/toyota.ppm"
            },
            {
                "name":"V",
                "image_path": "./images/tickers/visa.ppm"
            },
            {
                "name":"VZ",
                "image_path": "./images/tickers/verizon.ppm"
            },
            {
                "name":"WMT",
                "image_path": "./images/tickers/wallmart.ppm"
            },
            {
                "name":"XOM",
                "image_path": "./images/tickers/exxon.ppm"
            },
            {
                "name":"UNH",
                "image_path": "./images/tickers/uhg.ppm"
            },
            {
                "name":"BAC",
                "image_path": "./images/tickers/bankofamerica.ppm"
            }                             
        ]
        }"""
         )["tickers"]

    def names_list(self):
        list =[]
        for ticker in self.tickers:
            list.append(ticker['name'])
        return list

