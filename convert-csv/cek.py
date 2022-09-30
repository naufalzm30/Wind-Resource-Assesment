# # import json
# # import os, psutil;
# # from tkinter import filedialog, Text
# # import glob
# # import numpy as np

# # filepaths = filedialog.askdirectory()

# # file_json_raw = (glob.glob('{}\*.json'.format(filepaths)))

# # def panggil_json_raw(path):
# #     with open(path) as json_file:
        
# #         power=[]
# #         power_ro=1.2
# #         power_A=1
# #         raw = json.load(json_file)
# #         for i in raw:
# #             power_simpan = (float(i['Kec_angin']))
# #             power_i=((power_ro*power_A*((power_simpan)**3))/2)
# #             power.append(power_i)
# #             i.update({"Power":np.round(power_i,decimals=4)})
# #         # print(raw[0])
# #         # count=0
# #         # for j in raw:
# #         #     j.update({"Power":power[count]})
# #         #     count+=1


# #         return raw

# # for j in (file_json_raw):
# #     json_raw_second=panggil_json_raw(os.path.normpath(j))
    
# #     print(json_raw_second[245])
# import numpy as np
# import matplotlib.pyplot as plt
# from windrose import WindroseAxes
# import matplotlib.cm as cm

# data_bar=[1.5,1.5,1.5,1.5,2.5,2.5,3.5,3.5,3.5,4.1]
# derajat_bar=[0,45,90,135,180,225,270,315,360,270]

# contoh_object=[
#     {
#         "arah_angin":"U",
#         "kec_angin":2
    
#     },{
#         "arah_angin":"U",
#         "kec_angin":3
    
#     },{
#         "arah_angin":"T",
#         "kec_angin":0.9
    
#     },{
#         "arah_angin":"U",
#         "kec_angin":0.9
    
#     }
# ]

# # for i in contoh_object:
# #     if i['arah_angin']=="U":
# coba_1 = sum(((x['arah_angin']=='U') and ((x['kec_angin']<3) and (x['kec_angin']>0)) ) for x in contoh_object)

# print(coba_1)




# wx = WindroseAxes.from_ax()
    
# wx.bar(derajat_bar,data_bar,normed=True,opening=0.4,bins=np.arange(0,5),nsector=8)
# # wx.set_yticklabels(["20%","40%","60%","80%","100%"])
# wx.set_legend(bbox_to_anchor=[-0.1, 0],loc='lower left')
# # plt.savefig("{}\Windrose {} {} {}.png".format(pool_path_simpan,wind_type,nama_file_simpan,dataType))
# plt.show()

# wx1 = WindroseAxes.from_ax()
    
# wx1.contour(derajat_bar,data_bar,bins=np.arange(0, 5), cmap=cm.hot, lw=3)# wx.set_yticklabels(["20%","40%","60%","80%","100%"])
# wx1.set_legend(bbox_to_anchor=[-0.1, 0],loc='lower left')
# # plt.savefig("{}\Windrose {} {} {}.png".format(pool_path_simpan,wind_type,nama_file_simpan,dataType))
# plt.show()







# a=['00:00:00',
# '00:00:01',
# '00:00:02',
# '00:00:03',
# '00:00:04',
# '00:00:05']

# b=[
#     {"Time":"00:00:00","value":5},
#     {"Time":"00:00:01","value":6},
#     {"Time":"00:00:04","value":5},
#     {"Time":"00:00:05","value":5}
# ]
# c=[]
# time_cek=[] 
# for k in b:
#     time_cek.append(k['Time'])

# print(b[0])

# def indexExists(list,index):
#     try:
#         list[index]
#         return True
#     except IndexError:
#         return False


# count=0
# count_b=0
# for i in a:
#     if ((a[count])<(time_cek[count_b])) or (indexExists(b,count_b)==False):
#         masukin={"Time":a[count],"value":0}
#         c.insert(count,masukin)
#         count+=1
#         print(c)
#     else:
#         c.append(b[count_b])
#         count+=1
#         count_b+=1
#         print(c)
# b=c
# print(a)
# print(b)
# print(c)


# import datetime
# def time_excel(time):
#     date_time = datetime.datetime.strptime(time, "%H:%M:%S")
#     a_timedelta = date_time - datetime.datetime(1900, 1, 1,)
#     seconds = a_timedelta.total_seconds()
#     # '{0:.5f}'.format(seconds/86400)
#     output=(seconds/86400)
#     return (output)

# print(time_excel("12:35:00"))










# # import necessary modules
# import bokeh
# from bokeh.charts import Scatter, output_notebook, show
# import pandas as pd
  
# # output to notebook
# output_notebook()
  
# # read data in dataframe
# df = pd.read_csv(r"D:/kaggle / mcdonald / menu.csv")
  
# # create scatter plot
# p = Scatter(df, x = "Carbohydrates", y = "Saturated Fat",
#             title = "Saturated Fat vs Carbohydrates",
#             xlabel = "Carbohydrates", ylabel = "Saturated Fat",
#             color = "orange")
   
# # show the results
# show(p) 



# from datetime import datetime,timedelta
# time = "23:59:00"
# date="2022-8-14"

# tambah = "00:04:04"
# date_time = datetime.strptime(("{} {}").format(time,date), "%H:%M:%S %Y-%m-%d")
# time_tambah = datetime.strptime(tambah, "%H:%M:%S")

# result = date_time+timedelta(minutes=4, seconds=4)

# # seconds = result.timestamp()
# print(result)


import time
import multiprocessing as mp



def sleep_coba(s,a):
    print(" sleeping selama 1 detik")
    time.sleep(1)
    print(s, "done ", a)


if __name__== "__main__":
    t1_start = time.perf_counter()

    print(t1_start)
    multi_proses=[]
    for i in range(10):
        p1=mp.Process(target=sleep_coba,args=[i,"hehe"])
        p1.start()
        multi_proses.append(p1)

    for p in multi_proses:
        p.join()
    
    t1_stop = time.perf_counter()
    finish=time.perf_counter()

    print("finish di ",t1_stop-t1_start," detik")



