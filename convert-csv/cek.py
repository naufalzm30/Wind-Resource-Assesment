# import json
# import os, psutil;
# from tkinter import filedialog, Text
# import glob
# import numpy as np

# filepaths = filedialog.askdirectory()

# file_json_raw = (glob.glob('{}\*.json'.format(filepaths)))

# def panggil_json_raw(path):
#     with open(path) as json_file:
        
#         power=[]
#         power_ro=1.2
#         power_A=1
#         raw = json.load(json_file)
#         for i in raw:
#             power_simpan = (float(i['Kec_angin']))
#             power_i=((power_ro*power_A*((power_simpan)**3))/2)
#             power.append(power_i)
#             i.update({"Power":np.round(power_i,decimals=4)})
#         # print(raw[0])
#         # count=0
#         # for j in raw:
#         #     j.update({"Power":power[count]})
#         #     count+=1


#         return raw

# for j in (file_json_raw):
#     json_raw_second=panggil_json_raw(os.path.normpath(j))
    
#     print(json_raw_second[245])
import numpy as np
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import matplotlib.cm as cm

data_bar=[1.5,1.5,1.5,1.5,2.5,2.5,3.5,3.5,3.5,4.1]
derajat_bar=[0,45,90,135,180,225,270,315,360,270]

contoh_object=[
    {
        "arah_angin":"U",
        "kec_angin":2
    
    },{
        "arah_angin":"U",
        "kec_angin":3
    
    },{
        "arah_angin":"T",
        "kec_angin":0.9
    
    },{
        "arah_angin":"U",
        "kec_angin":0.9
    
    }
]

# for i in contoh_object:
#     if i['arah_angin']=="U":
coba_1 = sum(((x['arah_angin']=='U') and ((x['kec_angin']<3) and (x['kec_angin']>0)) ) for x in contoh_object)

print(coba_1)




wx = WindroseAxes.from_ax()
    
wx.bar(derajat_bar,data_bar,normed=True,opening=0.4,bins=np.arange(0,5),nsector=8)
# wx.set_yticklabels(["20%","40%","60%","80%","100%"])
wx.set_legend(bbox_to_anchor=[-0.1, 0],loc='lower left')
# plt.savefig("{}\Windrose {} {} {}.png".format(pool_path_simpan,wind_type,nama_file_simpan,dataType))
plt.show()

wx1 = WindroseAxes.from_ax()
    
wx1.contour(derajat_bar,data_bar,bins=np.arange(0, 5), cmap=cm.hot, lw=3)# wx.set_yticklabels(["20%","40%","60%","80%","100%"])
wx1.set_legend(bbox_to_anchor=[-0.1, 0],loc='lower left')
# plt.savefig("{}\Windrose {} {} {}.png".format(pool_path_simpan,wind_type,nama_file_simpan,dataType))
plt.show()