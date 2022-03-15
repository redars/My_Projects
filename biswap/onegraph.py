# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 18:22:32 2021

@author: arsko
"""
### Drawing
import pickle
import pandas as pd
from matplotlib import pyplot as plt

file = open('D:/univer/proj/b10.pickle', 'rb')
results = pickle.load(file)
file.close()
dframes = []
leng = len(results)
arr = []
for i in range (0,len(results)):
    arr.append(i)
df = pd.DataFrame({'Order': arr, 'Price': results[::-1]})
df.plot(x='Order', y='Price')
i = 10
plt.savefig(f'D:/univer/proj/images/roboost_{i}.png')
