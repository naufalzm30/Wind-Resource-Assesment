import json
import csv
import numpy as np
from audioop import avg
import pandas as pd
from pandas import json_normalize
import xlsxwriter
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from tkinter import *
from tkinter import filedialog
from windrose import WindroseAxes

def openFile():
    filepaths = filedialog.askdirectory()
    return (filepaths)

def panggil_json_raw(path):
    with open(path) as json_file:
        raw = json.load(json_file)
        
        return raw  

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
    power_simpan=[]
    counter_kecepatan=0
    for i in json_raw_second:
        KA_simpan.append(float(i['Kec_angin']))
        DA_simpan.append(float(i['Derajat_angin']))
        power_simpan.append(float(i['Power']))
        a = list([i['ID_Turbin'],i['Date'],i['Time']])
        b = (i["Time"])
        
        waktu.append(b)
        param_not_fix.append(a)

    KA = np.array(KA_simpan)
    DA = np.array(DA_simpan)
    power=np.array(power_simpan)


    # # print(waktu)
    # plt.figure(count+1)
    # plt.plot(waktu, KA_simpan)
    # plt.savefig("graph_s_{}.jpg".format(count+1))

    KA_avg = np.round(np.mean(KA.reshape(-1, 60), axis=1),decimals=2)
    DA_avg = (np.round((np.mean(DA.reshape(-1, 60), axis=1)),decimals=0)).astype(int)
    power_avg=np.round(np.mean(power.reshape(-1, 60), axis=1),decimals=4)

    del KA_simpan
    del DA_simpan
    del power_simpan
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
        json_param = {"ID_Turbin":param_fix[count][0],"Date":param_fix[count][1],"Time":param_fix[count][2],"Kec_angin":float(KA_avg[count]),"Arah_angin":Arah_angin[count],"Derajat_angin":int(DA_avg[count]),"Power":float(power_avg[count])}
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


def buat_grafik(pool_grafik1,pool_grafik2,counter,pool_path_simpan,nama_file_simpan,penanda,gap):
    ax1 = plt.figure("per_{}_{}".format(penanda,counter+1),figsize=(10, 3)).add_subplot(111)
    ax1.plot(pool_grafik1[counter], pool_grafik2[counter]) 
    # start, end = ax1.get_xlim()
    ax1.set_xticks(pool_grafik1[counter][::gap])
    ax1.set_ylabel("Kec angin m/s")
    plt.savefig("{}\Grafik per {} {}.png".format(pool_path_simpan,penanda,nama_file_simpan))
    plt.close(plt.figure("per_{}_{}".format(penanda,counter+1),figsize=(10, 3)))

def buat_windrose(derajat,kec_angin,pool_path_simpan,nama_file_simpan,wind_type,dataType):
    wx = WindroseAxes.from_ax()
    
    if (wind_type=="bar"):
        wx.bar(derajat,kec_angin,normed=True, opening=0.8,bins=np.arange(0,12,2),nsector=8)
    else:
        wx.contour(derajat,kec_angin,normed=True,bins=np.arange(0, 12,2), cmap=cm.hot, lw=3,nsector=8)
    # wx.set_yticklabels(["20%","40%","60%","80%","100%"])
    wx.set_legend(bbox_to_anchor=[-0.1, 0],loc='lower left')
    plt.savefig("{}\Windrose {} {} {}.png".format(pool_path_simpan,wind_type,nama_file_simpan,dataType))
    plt.close()


def keluaran_analitik(json_untuk_csv):

    a=[]
    b=[]
    
    utara_kec=[]
    timur_laut_kec=[]
    timur_kec=[]
    tenggara_kec=[]
    selatan_kec=[]
    barat_daya_kec=[]
    barat_kec=[]
    barat_laut_kec=[]

    utara_power=[]
    timur_laut_power=[]
    timur_power=[]
    tenggara_power=[]
    selatan_power=[]
    barat_daya_power=[]
    barat_power=[]
    barat_laut_power=[]

    data_windrose=[]

    for z in (json_untuk_csv):
        a.append(z["Time"])
        b.append(z["Kec_angin"])
        match z['Arah_angin']:
            case 'U':
                param_arah_angin={"Derajat_angin":z['Derajat_angin'],"Kec_angin":z['Kec_angin']}

                utara_kec.append(z['Kec_angin'])
                utara_power.append(z['Power'])

                data_windrose.append(param_arah_angin)
            case 'TL':
                param_arah_angin={"Derajat_angin":z['Derajat_angin'],"Kec_angin":z['Kec_angin']}
                
                timur_laut_kec.append(z['Kec_angin'])
                timur_laut_power.append(z['Power'])

                data_windrose.append(param_arah_angin)
            case 'T':
                param_arah_angin={"Derajat_angin":z['Derajat_angin'],"Kec_angin":z['Kec_angin']}

                timur_kec.append(z['Kec_angin'])
                timur_power.append(z['Power'])

                data_windrose.append(param_arah_angin)
            case 'Tg':
                param_arah_angin={"Derajat_angin":z['Derajat_angin'],"Kec_angin":z['Kec_angin']}
                
                tenggara_kec.append(z['Kec_angin'])
                tenggara_power.append(z['Power'])

                data_windrose.append(param_arah_angin)
            case 'S':
                param_arah_angin={"Derajat_angin":z['Derajat_angin'],"Kec_angin":z['Kec_angin']}
                
                selatan_kec.append(z['Kec_angin'])
                selatan_power.append(z['Power'])

                data_windrose.append(param_arah_angin)
            case 'BD':
                param_arah_angin={"Derajat_angin":z['Power'],"Kec_angin":z['Kec_angin']}
                
                barat_daya_kec.append(z['Kec_angin'])
                barat_daya_power.append(z['Power'])

                data_windrose.append(param_arah_angin)
            case 'B':
                param_arah_angin={"Derajat_angin":z['Derajat_angin'],"Kec_angin":z['Kec_angin']}
                
                barat_kec.append(z['Kec_angin'])
                barat_power.append(z['Power'])

                data_windrose.append(param_arah_angin)
            case 'BL':
                param_arah_angin={"Derajat_angin":z['Derajat_angin'],"Kec_angin":z['Kec_angin']}
                
                barat_laut_kec.append(z['Kec_angin'])
                barat_laut_power.append(z['Power'])

                data_windrose.append(param_arah_angin)
    print(pd.DataFrame(data_windrose))
    max_kec=[]
    max_power=[]
    mean_kec=[]
    mean_power=[]
    std_kec=[]
    std_power=[]

    max_kec.append(max(utara_kec))        
    max_kec.append(max(timur_laut_kec))
    max_kec.append(max(timur_kec))
    max_kec.append(max(tenggara_kec))
    max_kec.append(max(selatan_kec))
    max_kec.append(max(barat_daya_kec))
    max_kec.append(max(barat_kec))
    max_kec.append(max(barat_laut_kec))


    max_power.append(max(utara_power))        
    max_power.append(max(timur_laut_power))
    max_power.append(max(timur_power))
    max_power.append(max(tenggara_power))
    max_power.append(max(selatan_power))
    max_power.append(max(barat_daya_power))
    max_power.append(max(barat_power))
    max_power.append(max(barat_laut_power))


    mean_kec.append(np.mean(utara_kec))        
    mean_kec.append(np.mean(timur_laut_kec))
    mean_kec.append(np.mean(timur_kec))
    mean_kec.append(np.mean(tenggara_kec))
    mean_kec.append(np.mean(selatan_kec))
    mean_kec.append(np.mean(barat_daya_kec))
    mean_kec.append(np.mean(barat_kec))
    mean_kec.append(np.mean(barat_laut_kec))


    mean_power.append(np.mean(utara_power))        
    mean_power.append(np.mean(timur_laut_power))
    mean_power.append(np.mean(timur_power))
    mean_power.append(np.mean(tenggara_power))
    mean_power.append(np.mean(selatan_power))
    mean_power.append(np.mean(barat_daya_power))
    mean_power.append(np.mean(barat_power))
    mean_power.append(np.mean(barat_laut_power))

    std_kec.append(np.std(utara_kec))        
    std_kec.append(np.std(timur_laut_kec))
    std_kec.append(np.std(timur_kec))
    std_kec.append(np.std(tenggara_kec))
    std_kec.append(np.std(selatan_kec))
    std_kec.append(np.std(barat_daya_kec))
    std_kec.append(np.std(barat_kec))
    std_kec.append(np.std(barat_laut_kec))


    std_power.append(np.std(utara_power))        
    std_power.append(np.std(timur_laut_power))
    std_power.append(np.std(timur_power))
    std_power.append(np.std(tenggara_power))
    std_power.append(np.std(selatan_power))
    std_power.append(np.std(barat_daya_power))
    std_power.append(np.std(barat_power))
    std_power.append(np.std(barat_laut_power))

    

    return (data_windrose,max_kec,max_power,mean_kec,mean_power,std_kec,std_power,a,b)