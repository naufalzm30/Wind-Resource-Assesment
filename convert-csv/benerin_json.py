import glob
from tkinter import filedialog
import os
import json


filepaths = filedialog.askdirectory()
pool_raw=filepaths
file_json_raw =glob.glob('{}\*.json'.format(pool_raw))
# print(file_json_raw)
count=0
json_olah=[]
# print(file_json_raw)
for i in file_json_raw:
    a= os.path.normpath(i)
    with open(a) as json_file:
        json_raw=json.load(json_file) 
    if (len(json_raw)):
        # print(float(json_raw[:]['Kec_angin']))
        print(a)
        print("\n")
    print(float(json_raw[:]['Kec_angin']))
    json_olah.append(json_raw)
# print(json_olah[0][0]["Arah_Angin"])
