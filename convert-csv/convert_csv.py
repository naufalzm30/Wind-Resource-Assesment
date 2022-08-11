import csv
from csv import reader
import glob
from tkinter import filedialog
import os, psutil
from matplotlib.font_manager import json_dump;
import datetime
import json
import datetime as dt
import json
import numpy as np

import pandas as pd


def untuk_buat_folder_RTS(nama_RTS,path_exist):
  isExist = os.path.exists("{}\{}".format(path_exist,nama_RTS))

  if not isExist:
    os.makedirs("{}\{}".format(path_exist,nama_RTS))

  path_exist="{}\{}".format(path_exist,nama_RTS)
  return path_exist


filepaths = filedialog.askdirectory()
pool_raw=filepaths
print(filepaths)
file_csv_raw =glob.glob('{}\WRA\*.csv'.format(pool_raw))

file_csv_raw.extend(glob.glob('{}\RTS\**\*.csv'.format(pool_raw), recursive=True))

isExist = os.path.exists("{}\JSON_olah".format(pool_raw))

if not isExist:
  
  # Create a new directory because it does not exist 
  os.makedirs("{}\JSON_olah".format(pool_raw))

kec_angin=[]
count=0
for h in file_csv_raw:
    a= os.path.normpath(h)
    print(a)
    csv_file = pd.DataFrame(pd.read_csv("{}".format(a), sep = ";", header =None,index_col = False,skipinitialspace = True,skip_blank_lines=True))
    # print(csv_file[1])
    # retrieved_elements = list(filter(lambda x: 'WR' in x, csv_file[0]))
    # print(retrieved_elements[0])

    siap_json=[]
    print(csv_file[0][1])
    if ((csv_file[0][0][:2])=="WR"):
      path_exist="{}\JSON_olah\WRA".format(pool_raw)
      isExist = os.path.exists(path_exist)

      if not isExist:
        os.makedirs("{}\JSON_olah\WRA".format(pool_raw))



      power=[]
      power_ro=1.2
      power_A=1

      csv_file.columns =["ID_Device", "Date", "Time", "Kec_angin","Arah_angin","Derajat_angin"]
      csv_file = csv_file.assign(Power=lambda x: np.round(((power_ro*power_A*((x.Kec_angin)**3))/2),decimals=4))

      ID_Device=csv_file['ID_Device'].values.tolist()
      Date=csv_file['Date'].values.tolist()
      Time_raw=csv_file['Time'].values.tolist()
      Kec_angin=csv_file['Kec_angin'].values.tolist()
      Arah_angin=csv_file['Arah_angin'].values.tolist()
      Derajat_angin=csv_file['Derajat_angin'].values.tolist()
      Power=csv_file['Power'].values.tolist()
      Time=[]
      # print(Time_raw)
      for t in Time_raw:
        try:
          Time.append('{}'.format(datetime.datetime.strptime(t,"%H:%M:%S").time()))
        except ValueError as ve:
          Time.append('{}'.format(datetime.timedelta(seconds=(round(float(t)*86400)))))
          print(datetime.timedelta(seconds=(round(float(t)*86400))))
      print(Time[0])

      count=0
      for i in ID_Device:
        ke_json={"ID_Device":ID_Device[count],"Date":Date[count],"Time":Time[count],"Kec_angin":float(Kec_angin[count]),"Arah_angin":Arah_angin[count],"Derajat_angin":int(Derajat_angin[count]),"Power":float(Power[count])} 
        siap_json.append(ke_json)
        count+=1
    elif (csv_file[0][1]=="WRA"):
      path_exist="{}\JSON_olah\WRA".format(pool_raw)
      isExist = os.path.exists(path_exist)

      if not isExist:
        os.makedirs("{}\JSON_olah\WRA".format(pool_raw))

      csv_file.columns =["ID_Device", "Date", "Time", "Kec_angin","Arah_angin","Derajat_angin",'Power']
      csv_file.drop(csv_file.index[0], inplace=True)
      # print(csv_file)

      ID_Device=csv_file['ID_Device'].values.tolist()
      Date=csv_file['Date'].values.tolist()
      Time_raw=csv_file['Time'].values.tolist()
      Kec_angin=csv_file['Kec_angin'].values.tolist()
      Arah_angin=csv_file['Arah_angin'].values.tolist()
      Derajat_angin=csv_file['Derajat_angin'].values.tolist()
      Power=csv_file['Power'].values.tolist()
      Time=[]

      for t in Time_raw:
        try:
          Time.append('{}'.format(datetime.datetime.strptime(t,"%H:%M:%S").time()))
        except ValueError as ve:
          Time.append('{}'.format(datetime.timedelta(seconds=(round(float(t)*86400)))))
          print(datetime.timedelta(seconds=(round(float(t)*86400))))
      print(Time[0])

      count=0
      for i in ID_Device:
        ke_json={"ID_Device":ID_Device[count],"Date":Date[count],"Time":Time[count],"Kec_angin":float(Kec_angin[count]),"Arah_angin":Arah_angin[count],"Derajat_angin":int(Derajat_angin[count]),"Power":float(Power[count])} 
        siap_json.append(ke_json)
        count+=1




    else:
      path_exist="{}\JSON_olah\RTS".format(pool_raw)
      isExist = os.path.exists(path_exist)

      if not isExist:
        os.makedirs("{}\JSON_olah\RTS".format(pool_raw))

      if len(csv_file.axes[1])>4:
        for i in range(4,len(csv_file.axes[1])):
          del csv_file[i]


      csv_file.columns =["ID_Turbin", "Date", "Time", "RTS"]
      ID_Device=csv_file['ID_Turbin'].values.tolist()
      Date=csv_file['Date'].values.tolist()
      Time_raw=csv_file['Time'].values.tolist()
      RTS=csv_file['RTS'].values.tolist()

      Time=[]

      for t in Time_raw:
        # print(t)
        try:
          Time.append('{}'.format(datetime.datetime.strptime(t,"%H:%M:%S").time()))
        except ValueError as ve:
          Time.append('{}'.format(datetime.timedelta(seconds=(round(float(t)*86400)))))
          print(datetime.timedelta(seconds=(round(float(t)*86400))))

      count=0
      for i in ID_Device:
        ke_json={"ID_Turbin":ID_Device[count],"Date":Date[count],"Time":Time[count],"RTS":float(RTS[count])} 
        siap_json.append(ke_json)
        count+=1
      path_exist=untuk_buat_folder_RTS(ID_Device[0],path_exist)




    # print(path_exist)
    
    

    try:
          ambil_date=datetime.datetime.strptime(Date[0],"%d/%m/%Y")
    except ValueError as ve:
      try:
          ambil_date=datetime.datetime.strptime(Date[0],"%m/%d/%Y")
      except:
        ambil_date=datetime.datetime.strptime(Date[0],"%Y-%m-%d")
        


    untuk_filename=datetime.datetime.strftime(ambil_date,"%y-%m-%d")
    file_name = "{}-{}".format(ID_Device[0],untuk_filename)

    path="{}\{}".format(path_exist,file_name)



    
    # print(siap_json)

    # print(len(csv_file))

    # df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d %H:%M:%S')
    # csv_file['Time'] = pd.to_datetime(csv_file.Time, format="%H:%M:%S")
    # csv_file['Time']= csv_file['Time'].dt.strftime("%H:%M:%S")
    # csv_file["ID_Device"].str.strip()
    # csv_file["Date"].str.strip()
    # csv_file["Time"].str.strip()
    # csv_file["Derajat_angin"].str.strip()
    
    with open('{}.json'.format(path), 'w') as outfile:#as outfile:
        json.dump(siap_json,outfile,indent=4)
    
    del csv_file
    count+=1
# print('{}\hehe1.json'.format(pool_raw))



# file_name = os.path.basename(a).split('.')[0]
# path='WR-7-1.json'
# with open(path, "w") as outfile:
#     outfile.write(list_of_rows)
# read_obj.close()
