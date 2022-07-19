import json
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
with open('WRA1_2269.json') as json_file:
    hehe=json.load(json_file)  
import numpy as np

import datetime
from datetime import datetime

import pandas as pd

# a=[]
# b=[]
# for i in hehe:
#     a.append(i["Time"])
#     b.append(i["Kec_angin"])


c=[[5.5,5.9,8.4,9.1,11.6],[2.3,4.3,5.2,6.3,7.6]]
time=[["00:00:00","00:00:01","00:00:02","00:00:03","00:00:04"],["00:00:00","00:00:01","00:00:02","00:00:03","00:00:04"]]
d=[]

for i in time:   
    count_time=0
    time_baru=[]
    for h in i:
        time_str = i[count_time]
        time_object = datetime.strptime(time_str, "%H:%M:%S").time()
        time_baru.append(str(time_object))
        count_time+=1
    d.append(time_baru)

# print(d)

gg=[]
count=0


def plot_sendiri(c,d,count):
    plt.figure(count+1,figsize=(10, 3))
    ax1 = plt.figure(count+1,figsize=(10, 3))

    ax1.plot(d[count], c[count]) 
    start, end = ax1.get_xlim()
    ax1.set_xticks(np.arange(start, end, 2))
    print(d)
    print(str(start))
    print(str(end))
    return plt.figure(figsize=(10, 3))

for i in c:
    plot_sendiri(c,d,count)
    
    count+=1
# plt.savefig("graph_s.jpg")
# print(b)
count=0
for j in c:
    plt.figure(count+1,figsize=(10, 3))
    plt.savefig("hehe_{}".format(count))
    # plt.show()
    count+=1
