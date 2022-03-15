# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 23:08:26 2021

@author: arsko
"""
#find the cheapest ursus knife
import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
}

API_KEY = "" # enter your api key
APP_ID = 730
CODE = 344380

url = f"https://bitskins.com/api/v1/get_price_data_for_items_on_sale/?api_key={API_KEY}&code={CODE}&app_id={APP_ID}"

response = requests.get(url,headers=headers)
pages = json.loads(response.text)
for el in pages['data']['items']:
    if 'Ursus' in el['market_hash_name']:
        print(el['market_hash_name']+" "+el['lowest_price'])
