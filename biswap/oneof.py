# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 18:18:40 2021

@author: arsko
"""
###### Get data to draw graphs
import requests
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
import pickle

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
}

results = []

def Get_boost(a):
    res =""
    for el in a:
        if el != '/':
            res +=el 
        else:
            return int(res)

for i in range (0,300):
    print(i)
    response = requests.get(f"https://marketplace.biswap.org/back/transactions/market?partner=all&sortBy=newest&page={i}", headers=headers)
    if response.status_code != 200:
        time.sleep(2)
    else:
        pages = json.loads(response.text)
        for j in range(0,10):
            if pages['data'][j]['logs'][len(pages['data'][j]['logs'])-1]['name'] != 'AcceptOffer':
                continue
            else:
                if 'nft' not in pages['data'][j]:
                    continue
                else:
                    if 'attributes' not in pages['data'][j]['nft']['metadata']:
                        print('none at')
                        continue
                    else:
                        if 'value' not in pages['data'][j]['nft']['metadata']['attributes'][3]:
                            continue
                        else:
                            index = Get_boost(pages['data'][j]['nft']['metadata']['attributes'][3]['value'])
                            if index != 10:
                                continue
                            else:
                                if len(pages['data'][j]['logs'][len(pages['data'][j]['logs'])-1]['params']['price']) < 19:
                                    continue
                                else:
                                    results.append(int(pages['data'][j]['logs'][len(pages['data'][j]['logs'])-1]['params']['price'][:-18]))

with open('D:/univer/proj/b10.pickle', 'wb') as f:
    pickle.dump(results, f)
