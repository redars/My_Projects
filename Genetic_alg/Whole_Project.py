from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import random
from itertools import *
from statistics import mean
import matplotlib.pyplot as plt
import pickle
######### Graphic
Fs = []
Generations = [] 
######### Settings
population = 100
max_gen = 40

url = "https://www.avtodispetcher.ru/distance/table/r103906-kaliningradskaya+oblast%2527/"
#url = "https://www.avtodispetcher.ru/distance/table/r51490-moskovskaya+oblast%2527/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.216 YaBrowser/21.5.4.607 Yowser/2.5 Safari/537.36",
}

cut = 3 #Do not touch it

######### Parse Info

def Get_Distance(l):
    distance = ''
    for i in range(0,len(l)):
        if l[i].isdigit():
            distance +=l[i]
        if l[i] == "\xa0":
            return int(distance)
        i+=1

response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
right_column = soup.find_all("div", {"class": "param_value"})
info = []
pack = []
n = 0
for el in right_column:
    if n == 2:
        pack.append(Get_Distance(list(el.text)))
        info.append(pack)
        pack = []
        n = 0
    else:
        pack.append(el.text)
        n+=1
        
######### Creating cityes list and collecting info to make a Dataframe   
 
cityes = []
to_show = []
pack = []

for i in range (0,len(info)):
    if info[i][0] not in cityes:
        cityes.append(info[i][0])
    if i == 0:
        pack.append(cityes[0])
    if pack[0] == info[i][0]:
        pack.append(info[i][2])
    else:
        to_show.append(pack)
        pack = []
        pack.append(info[i][0])
        pack.append(info[i][2])
    if i == len(info)-1:
        to_show.append([info[i][0],info[i][2]]) 
        to_show.append([info[i][1]])
        cityes.append(info[i][1])

for i in range(0,len(to_show[0])):
    to_show[i].insert(1, 0)
    if i-1 >= 0:
        j = i-1
        n = i+1
        while j > -1:
            to_show[i].insert(1, to_show[j][n])
            j-=1
    i+=1
dic = {}

for i in range(0,len(to_show)):
    dic.update({to_show[i][0]: to_show[i][1:]})
       
df = pd.DataFrame(dic,columns=cityes)  

for el in to_show:
    el.pop(0)

######### Methods

# To get different cuts
def Check(a,b):
    for el in a:
        for item in b:
            if el == item:
                return True
            
# To check if we have the same route
def Same(a,b):
    res = 0
    for i in range(0,len(a)-1):
        if a[i] == b[i]:
            res+=1
    if res == len(a):
        return True
    else:
        return False
# To get route length
def Calculate(way,to_show):
    res = 0
    for i in range(0,len(way)-1):
        res += to_show[way[i]][way[i+1]]
    res += to_show[way[0]][way[len(way)-1]]
    return res

#Mutations
def Change_Mut(route):
    r = random.randint(0,len(route)-1)
    r2 = random.randint(0,len(route)-1)
    while r == r2 or r>r2 :
        r = random.randint(0,len(route)-1)
        r2 = random.randint(0,len(route)-1)
    route[r] +=route[r2]
    route[r2] = route[r] - route[r2]
    route[r]-= route[r2]
    return route

def Insert_Mut(route):
    r = random.randint(0,len(route)-1)
    r2 = random.randint(0,len(route)-1)
    while r == r2 or r>r2:
        r = random.randint(0,len(route)-1)
        r2 = random.randint(0,len(route)-1)
    route.insert(r,route[r2])
    route.pop(r2+1)
    return route

def Inversion_Mut(route):
    r = random.randint(0,len(route)-1)
    r2 = random.randint(0,len(route)-1)
    l = []
    start = []
    end = []
    while r == r2 or r>r2:
        r = random.randint(0,len(route)-1)
        r2 = random.randint(0,len(route)-1)
    for i in range(0,r):
        start.append(route[i])
    for i in range(r2+1,len(route)):
        end.append(route[i])
    for i in range(r,r2+1):
        l.append(route[i])
    rever = l[::-1]
    start.extend(rever)
    start.extend(end)
    return start

######### Full Enumeration to get the best route
lan = []
n= 0
for i in range (0,len(cityes)):
    lan.append(n)
    n+=1
all_enum = []
all_dist = []
for el in permutations(lan):
    all_enum.append(el)
    all_dist.append(Calculate(el,to_show))
minimum_way = min(all_dist)
min_route = all_enum[all_dist.index(minimum_way)]
word_route = ""
for el in min_route:
    word_route+= (str(cityes[el])+'--> ')
print("Minimum route by full enum is: "+str(minimum_way)+" km ; Route: "+str(word_route)+str(cityes[min_route[0]]))

######### Creating 10 random ways


ways = []

for i in range(0,population):
    way = []
    num = len(to_show)
    for j in range(0,num):
        A = random.randint(0, num-1)
        while A in way:
            A = random.randint(0, num-1)
        way.append(A)       
    ways.append(way)

#with open('C:/Users/arsko/Practice/config/routes.pickle', 'rb') as f:
#    ways = pickle.load(f)

distances = []
for el in ways:
    distances.append(Calculate(el,to_show))
Generation = 0
while Generation <= max_gen:

######### Selection
    Generation +=1
    selection = []
    for i in range(0,len(distances)):
        A = random.randint(0, len(distances)-1)
        while A in selection:
            A = random.randint(0, len(distances)-1)
        selection.append(A)
    
    for i in range(0,len(selection)-1,2):
        if distances[selection[i]]>distances[selection[i+1]]:
            for j in range(0,len(ways[selection[i]])):
                ways[selection[i]][j] = ways[selection[i+1]][j]
        else:
            for j in range(0,len(ways[selection[i+1]])):
                ways[selection[i+1]][j] = ways[selection[i]][j]
    
    ######### Hybrid
    
        
    selection = []
    
    for i in range(0,len(distances)):
        A = random.randint(0, len(distances)-1)
        while A in selection:
            A = random.randint(0, len(distances)-1)
        selection.append(A)
        
    new_ways = []
    
    #main algoritm
        
    for i in range(0,len(selection),2):
          B = ways[selection[i+1]] 
          A = ways[selection[i]]
          new_A = []
          new_B = []
          r = random.randint(0,len(B)-1-cut)
          r0 = random.randint(0,len(B)-1-cut)
          r1 = [A[r],A[r+1],A[r+2]]
          r2 = [B[r0],B[r0+1],B[r0+2]]
          if Same(A,B) is False:
              while Check(r1,r2):
                  r = random.randint(0,len(B)-1-cut)
                  r0 = random.randint(0,len(B)-1-cut)
                  r1 = [A[r],A[r+1],A[r+2]]
                  r2 = [B[r0],B[r0+1],B[r0+2]]
          for j in range(0,len(A)):
              if B[j] not in r1 and j!= r and j!= r+1 and j!= r+2:
                  new_A.append(B[j])
              if B[j] in r1 and j!= r and j!= r+1 and j!= r+2:
                  if B[A.index(B[j])] in r1:
                      if B[A.index(B[A.index(B[j])])] in r1:
                          new_A.append(B[A.index(B[A.index(B[A.index(B[j])])])])
                      else:
                          new_A.append(B[A.index(B[A.index(B[j])])])
                  else:
                      new_A.append(B[A.index(B[j])])
              if j == r or j == r+1 or j == r+2:
                  new_A.append(A[j])
          for j in range(0,len(B)):
              if A[j] not in r2 and j!= r0 and j!= r0+1 and j!= r0+2:
                  new_B.append(A[j])
              if A[j] in r2 and j!= r0 and j!= r0+1 and j!= r0+2:
                  if A[B.index(A[j])] in r2:
                      if A[B.index(A[B.index(A[j])])] in r2:
                          new_B.append(A[B.index(A[B.index(A[B.index(A[j])])])])
                      else:
                          new_B.append(A[B.index(A[B.index(A[j])])])
                  else:
                      new_B.append(A[B.index(A[j])])
              if j == r0 or j== r0+1 or j== r0+2:
                  new_B.append(B[j])
          new_ways.append(new_A)
          new_ways.append(new_B)
    
    ######### Mutation
    new_population = []
    for el in new_ways:
        r = random.uniform(0.0, 1.0)
        if r <= 0.01:
            mutType = random.randint(1,3)
            if mutType == 1:
                route = Change_Mut(el)
            if mutType == 2:
                route = Insert_Mut(el)
            if mutType == 3:
                route = Inversion_Mut(el)
        else:
            route = el
        new_population.append(route)
    distances = []
    for el in new_population:
        distances.append(Calculate(el,to_show))
    for i in range(0,len(new_population)):
        ways[i] = new_population[i]
    minItem = min(distances)
    Fs.append(mean(distances))
    Generations.append(Generation)

index = distances.index(minItem)
result_route = new_population[index]
word_route = ""
for el in result_route:
    word_route+= (str(cityes[el])+'--> ')
print("Minimum route by GA is: "+str(minItem)+" km ; Route: "+str(word_route)+str(cityes[result_route[0]]))

gr =[]
for i in range(0,len(Generations)):
    gr.append([Fs[i],Generations[i]])
    
Fg = pd.DataFrame(gr,columns=["F","Generation"])
plt.plot(Fg["Generation"], Fg["F"])
plt.savefig('C:/Users/arsko/Practice/Images/'+"population_Is_"+str(population)+'.pdf')   