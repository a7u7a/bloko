#!/usr/bin/env python
import json

def read_countries_file():
    f = open('countries.json')
    countries = json.load(f)
    f.close()
    return countries

class CountryData(object):
    def __init__(self):
        self.countries = read_countries_file()["countries"]

    def names_list(self):
        list =[]
        for country in self.countries:
            list.append(country['name'])
        return list

