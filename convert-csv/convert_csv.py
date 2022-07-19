import csv
from csv import reader
import glob
from tkinter import filedialog
import os, psutil
from matplotlib.font_manager import json_dump;
import codecs
import json
import datetime as dt
import json

import pandas as pd


filepaths = filedialog.askdirectory()
pool_raw=filepaths
print(filepaths)
file_csv_raw =glob.glob('{}\*.csv'.format(pool_raw))


count=0
for h in file_csv_raw:
    a= os.path.normpath(h)
    file_name = os.path.basename(a).split('.')[0]
    print(a)
    csv_file = pd.DataFrame(pd.read_csv("{}".format(a), sep = ";", header =None,index_col = False,skipinitialspace = True,skip_blank_lines=True))
    csv_file.columns =["ID_Turbin", "Date", "Time", "Kec_angin","Arah_angin","Derajat_angin"]
    # df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d %H:%M:%S')
    # csv_file['Time'] = pd.to_datetime(csv_file.Time, format="%H:%M:%S")
    # csv_file['Time']= csv_file['Time'].dt.strftime("%H:%M:%S")
    # csv_file["ID_Turbin"].str.strip()
    # csv_file["Date"].str.strip()
    # csv_file["Time"].str.strip()
    # csv_file["Derajat_angin"].str.strip()

    with open('{}\{}.json'.format(pool_raw,file_name), 'w') as outfile :#as outfile:
        csv_file.to_json('{}\{}.json'.format(pool_raw,file_name),orient='records')
    outfile.close()
    del csv_file
    count+=1
# print('{}\hehe1.json'.format(pool_raw))



# file_name = os.path.basename(a).split('.')[0]
# path='WR-7-1.json'
# with open(path, "w") as outfile:
#     outfile.write(list_of_rows)
# read_obj.close()
