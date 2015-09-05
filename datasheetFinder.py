#!/usr/bin/python3
import requests


class DatasheetFinder:

    def __init__(self, apiKey):
        self.apiKey = apiKey

    def searchForProducts(self, partnumber):
        apiUrl = "http://api.element14.com/catalog/products"
        params = {
            "callInfo.responseDataFormat": "JSON",
            "callInfo.callback": "",
            "callInfo.omitXmlSchema": "false",
            "term": "any:" + str(partnumber),
            "storeInfo.id": "uk.farnell.com",
            "callInfo.apiKey": self.apiKey,
            "resultsSettings.offset": 0,
            "resultsSettings.numberOfResults": 10,
            "resultsSettings.responseGroup": "medium",
            "resultsSettings.refinements": "",
        }
        r = requests.get(apiUrl, params=params)

        products = r.json()["keywordSearchReturn"]["products"]

        return products
