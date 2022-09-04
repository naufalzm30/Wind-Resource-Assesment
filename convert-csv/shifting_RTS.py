import glob
from method import openFile,panggil_json_raw
from datetime import datetime,timedelta
import pandas as pd
from itertools import groupby
from tqdm import tqdm
import json
import os

pool_json_raw=openFile()

isExist = os.path.exists("{}\Hasil_shifting".format(pool_json_raw))

if not isExist:
  
  # Create a new directory because it does not exist 
  os.makedirs("{}\Hasil_shifting".format(pool_json_raw))

print(pool_json_raw)
    
file_wt = (glob.glob('{}\RTS\**\*.json'.format(pool_json_raw)))

# list_wt=['WT3']
list_wt=['WT1','WT2','WT3','WT4','WT5','WT6','WT7']

for wt_saat_ini in tqdm(list_wt):

    if wt_saat_ini=="WT1":
        minutes_delta=4
        seconds_delta=4
    elif wt_saat_ini=="WT2":
        minutes_delta=4
        seconds_delta=47
    elif wt_saat_ini=="WT3":
        minutes_delta=0
        seconds_delta=38
    elif wt_saat_ini=="WT4":
        minutes_delta=6
        seconds_delta=2
    elif wt_saat_ini=="WT5":
        minutes_delta=4
        seconds_delta=48
    elif wt_saat_ini=="WT6":
        minutes_delta=3
        seconds_delta=57
    elif wt_saat_ini=="WT7":
        minutes_delta=1
        seconds_delta=59
    
    isExist = os.path.exists("{}\Hasil_shifting\{}".format(pool_json_raw,wt_saat_ini))
    path_simpan=("{}\Hasil_shifting\{}").format(pool_json_raw,wt_saat_ini)
    if not isExist:    
        # Create a new directory because it does not exist 
        os.makedirs("{}\Hasil_shifting\{}".format(pool_json_raw,wt_saat_ini))

    WT = list(filter(lambda x: wt_saat_ini in x, file_wt))
    pool_tiap_wt=[]
    for y in WT:
        t = panggil_json_raw(y)
        for i in t:
            pool_tiap_wt.append(i)
    for r in tqdm(pool_tiap_wt):
        # print(pd.DataFrame(pool_tiap_wt))
        # print(ambil_sampel)
        # minutes_delta=4
        # seconds_delta=4

        date_time= datetime.strptime(("{} {}").format(r["Time"],r["Date"]), "%H:%M:%S %Y-%m-%d") 
        hasil_shift=date_time+timedelta(minutes=minutes_delta, seconds=seconds_delta)
        # print(hasil_shift)
        update=(datetime.strftime(hasil_shift,"%Y-%m-%d %H:%M:%S")).split(' ')
        date_update = update[0]
        time_update=update[1]
        # file_name.split('-')
        r.update({'Date':date_update,'Time':time_update})
        # print(ambil_sampel)
        
    def key_func(k):
        return k['Date']
    
    # sort INFO data by 'company' key.
    pool_tiap_wt = sorted(pool_tiap_wt, key=key_func)
    
    for key, value in tqdm(groupby(pool_tiap_wt, key_func)):

        untuk_filename=datetime.strftime((datetime.strptime(key,"%Y-%m-%d")),"%y-%m-%d")
        file_name = "{}-{}".format(wt_saat_ini,untuk_filename)

        path_wt="{}\{}.json".format(path_simpan,file_name)
        # print(key)
        with open(path_wt, "w") as outfile:
            json.dump(list(value),outfile,indent=4)
        # print (value[0])



# time = "23:59:00"
# date="2022-8-14"

# tambah = "00:04:04"
# date_time = datetime.strptime(("{} {}").format(time,date), "%H:%M:%S %Y-%m-%d")
# time_tambah = datetime.strptime(tambah, "%H:%M:%S")

# result = date_time+timedelta(minutes=4, seconds=4)
# # seconds = result.timestamp()
# print(result)

