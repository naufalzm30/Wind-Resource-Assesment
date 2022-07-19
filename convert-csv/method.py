import json
import csv
import numpy as np
from audioop import avg
from pandas import json_normalize
import glob
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
def openFile():
    filepaths = filedialog.askdirectory()
    return (filepaths)

def panggil_json_raw(path):
    with open(path) as json_file:
        return json.load(json_file)  

def simpan_csv(nama_untuk_disimpan,json_yang_mau_disimpan,path_simpan):
    count = 0
    path='{}\{}.csv'.format(path_simpan,nama_untuk_disimpan)
    dataSave = open(path, 'w', newline='')

    csv_writer = csv.writer(dataSave,delimiter=';')
    
    for data in json_yang_mau_disimpan:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    dataSave.close()

def simpan_json(nama_untuk_disimpan,json_yang_masuk,path_simpan):

    path='{}\{}.json'.format(path_simpan,nama_untuk_disimpan)
    with open(path, "w") as outfile:
        outfile.write(json_yang_masuk)
    outfile.close()

def proses_per_menit(json_raw_second):
    count = 0
    KA_simpan=[]
    DA_simpan=[]
    param_not_fix=[]
    Arah_angin=[]
    waktu=[]
    for i in json_raw_second:
        KA_simpan.append(float(i['Kec_angin']))
        DA_simpan.append(float(i['Derajat_angin']))
        a = list([i['ID_Turbin'],i['Date'],i['Time']])
        b = (i["Time"])
        waktu.append(b)
        param_not_fix.append(a)
    KA = np.array(KA_simpan)
    DA = np.array(DA_simpan)
    # # print(waktu)
    # plt.figure(count+1)
    # plt.plot(waktu, KA_simpan)
    # plt.savefig("graph_s_{}.jpg".format(count+1))


    KA_avg = np.round(np.mean(KA.reshape(-1, 60), axis=1),decimals=2)
    DA_avg = (np.round((np.mean(DA.reshape(-1, 60), axis=1)),decimals=0)).astype(int)
    

    del KA_simpan
    del DA_simpan
    for i in DA_avg:

        if i in range(0,26,1):
            Arah_angin.append("U")
        elif i in range(26,66,1):
            Arah_angin.append("TL")
        elif i in range(66,116,1):
            Arah_angin.append("T")
        elif i in range(116,156,1):
            Arah_angin.append("Tg")
        elif i in range(156,206,1):
            Arah_angin.append("S")
        elif i in range(206,246,1):
            Arah_angin.append("BD")
        elif i in range(246,296,1):
            Arah_angin.append("B")
        elif i in range(296,336,1):
            Arah_angin.append("BL")
        elif i in range(336,360,1):
            Arah_angin.append("U")
    
        count+=1
        if (i==DA_avg[-1]):
            count=0

    # key_list=list(Param_lain)
    param_fix=[]
    # del Param_lain
    count=0
    for i in param_not_fix:
        
        if ((count+1) % 60 == 0):
            param_fix.append(param_not_fix[count])
            
        count+=1

    json_untuk_csv=[]
    count=0
    for i in param_fix:
        json_param = {"ID_Turbin":param_fix[count][0],"Date":param_fix[count][1],"Time":param_fix[count][2],"Kec_angin":float(KA_avg[count]),"Arah_angin":Arah_angin[count],"Derajat_angin":int(DA_avg[count])}
        json_untuk_csv.append(json_param)
        count+=1
        if(i==param_fix[-1]):
            count=0
    del param_fix
    del KA_avg
    del Arah_angin
    del DA_avg
    # print(json_untuk_csv)
    return (json_untuk_csv)

def plot_sendiri(c,d,count):
    plt.figure(count+1)
    plt.plot(d[count], c[count])
    return plt.figure()