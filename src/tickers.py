#!/usr/bin/env python
import json
class TickerData(object):
    def __init__(self):
        self.tickers = json.loads("""{
        "tickers": [
            {
                "name":"TSLA",
                "image_path": "tesla.ppm"
            },
            {
                "name":"MSFT",
                "image_path": "microsoft.ppm"
            },
            {
                "name":"AMZN",
                "image_path": "amazon.ppm"
            },
            {
                "name":"BP",
                "image_path": "bp.ppm"
            },
            {
                "name":"AAPL",
                "image_path": "apple.ppm"
            },
            {
                "name":"ABT",
                "image_path": "abbott.ppm"
            },
            {
                "name":"ACN",
                "image_path": "accenture.ppm"
            },
            {
                "name":"ADBE",
                "image_path": "adobe.ppm"
            },          
            {
                "name":"ASML",
                "image_path": "asml.ppm"
            },
            {
                "name":"AVGO",
                "image_path": "broadcom.ppm"
            },
            {
                "name":"CMCSA",
                "image_path": "comcast.ppm"
            },     
            {
                "name":"COST",
                "image_path": "cosco.ppm"
            }, 
            {
                "name":"CSCO",
                "image_path": "cisco.ppm"
            },
            {
                "name":"CVX",
                "image_path": "chevron.ppm"
            },
            {
                "name":"DIS",
                "image_path": "disney.ppm"
            },                
            {
                "name":"META",
                "image_path": "meta.ppm"
            },
            {
                "name":"GOOGL",
                "image_path": "google.ppm"
            },          
            {
                "name":"HD",
                "image_path": "homedepot.ppm"
            },
            {
                "name":"JNJ",
                "image_path": "jhonson.ppm"
            },
            {
                "name":"JPM",
                "image_path": "chase.ppm"
            },
            {
                "name":"KO",
                "image_path": "coca.ppm"
            },
            {
                "name":"MA",
                "image_path": "mastercard.ppm"
            },
            {
                "name":"NKE",
                "image_path": "nike.ppm"
            },
            {
                "name":"NVDA",
                "image_path": "nvidia.ppm"
            },
            {
                "name":"PEP",
                "image_path": "pepsi.ppm"
            },
            {
                "name":"PFE",
                "image_path": "pfizer.ppm"
            },
            {
                "name":"PRDSY",
                "image_path": "prada.ppm"
            },                
            {
                "name":"SHEL",
                "image_path": "shell.ppm"
            },
            {
                "name":"TM",
                "image_path": "toyota.ppm"
            },
            {
                "name":"V",
                "image_path": "visa.ppm"
            },
            {
                "name":"VZ",
                "image_path": "verizon.ppm"
            },
            {
                "name":"WMT",
                "image_path": "wallmart.ppm"
            },
            {
                "name":"XOM",
                "image_path": "exxon.ppm"
            },
            {
                "name":"UNH",
                "image_path": "uhg.ppm"
            },
            {
                "name":"BAC",
                "image_path": "bankofamerica.ppm"
            }                             
        ]
        }"""
         )["tickers"]

    def names_list(self):
        list =[]
        for ticker in self.tickers:
            list.append(ticker['name'])
        return list