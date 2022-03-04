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
            },
            {
                "name":"AAPL",
                "image_path": "./images/apple.ppm"
            },
            {
                "name":"ABBV",
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
                "name":"BABA",
                "image_path": "./images/alibaba.ppm"
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
                "name":"CRM",
                "image_path": "./images/cosco.ppm"
            }, 
            {
                "name":"CSCO",
                "image_path": "./images/cisco.ppm"
            },
            {
                "name":"CVX",
                "image_path": "./images/cisco.ppm"
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
                "name":"GOOG",
                "image_path": "./images/google.ppm"
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
                "image_path": "./images/jpmorgan.ppm"
            },
            {
                "name":"KO",
                "image_path": "./images/cocacola.ppm"
            },
            {
                "name":"LLY",
                "image_path": "./images/cocacola.ppm"
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
                "name":"NTES",
                "image_path": "./images/nike.ppm"
            },          
            {
                "name":"NVDA",
                "image_path": "./images/nvidia.ppm"
            },
            {
                "name":"NVO",
                "image_path": "./images/nvidia.ppm"
            },
            {
                "name":"ORCL",
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
                "name":"PG",
                "image_path": "./images/pfizer.ppm"
            },                
            {
                "name":"SHEL",
                "image_path": "./images/pfizer.ppm"
            },
            {
                "name":"TM",
                "image_path": "./images/pfizer.ppm"
            },
            {
                "name":"TMO",
                "image_path": "./images/pfizer.ppm"
            },
            {
                "name":"TSM",
                "image_path": "./images/pfizer.ppm"
            },
            {
                "name":"V",
                "image_path": "./images/pfizer.ppm"
            },
            {
                "name":"VZ",
                "image_path": "./images/pfizer.ppm"
            },
            {
                "name":"WMT",
                "image_path": "./images/pfizer.ppm"
            },
            {
                "name":"XOM",
                "image_path": "./images/pfizer.ppm"
            },
            {
                "name":"UNH",
                "image_path": "./images/pfizer.ppm"
            },
            {
                "name":"BAC",
                "image_path": "./images/pfizer.ppm"
            }                             
        ]
        }"""
         )["tickers"]

    def names_list(self):
        list =[]
        for ticker in self.tickers:
            list.append(ticker['name'])
        return list