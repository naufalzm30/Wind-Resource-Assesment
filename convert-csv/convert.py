
from cProfile import label
from datetime import datetime, timedelta
from itertools import count
from numpy import dtype, spacing
from method import *

from excelsior import *
import os, psutil;
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, Text
from tkhtmlview import HTMLLabel
from PIL import Image, ImageTk
from operator import attrgetter
import pandas as pd
import glob
from tqdm import tqdm
import xlsxwriter


start_time = time.time()


# warna 
#104c84


def main():
    root_progress = Tk()
    progress  = ttk.Progressbar(root_progress, orient = HORIZONTAL, length=180)
    progress.pack()
    progress.config(mode='indeterminate')
    progress.start()
    pool_json_raw=openFile()

    file_json_raw = (glob.glob('{}\WRA\*.json'.format(pool_json_raw)))
    counter_h=0
    for h in file_json_raw:
        file_json_raw[counter_h]=os.path.normpath(h)
        counter_h+=1
 
    pool_json_raw=[]
    pool_json_csv=[]
    jcounter=0
    pool_data_windrose_detik=[]
    pool_data_windrose_menit=[]
    pool_grafik_detik_a=[]
    pool_grafik_detik_b=[]
    pool_grafik_menit_c=[]
    pool_grafik_menit_d=[]
    keluaran_analitik_detik=[]
    keluaran_analitik_menit=[]
    for j in tqdm(file_json_raw):
        
        a=[]
        b=[]
        json_raw_second=panggil_json_raw(os.path.normpath(j))
 
        json_untuk_csv = proses_per_menit(json_raw_second)
        # print(json_untuk_csv)
        
        data_windrose_detik,max_kec_detik,max_power_detik,mean_kec_detik,mean_power_detik,std_kec_detik,std_power_detik,a,b=keluaran_analitik(json_raw_second)

        keluaran_analitik_detik.append([max_kec_detik,max_power_detik,mean_kec_detik,mean_power_detik,std_kec_detik,std_power_detik])

        data_windrose_menit,max_kec_menit,max_power_menit,mean_kec_menit,mean_power_menit,std_kec_menit,std_power_menit,c,d=keluaran_analitik(json_untuk_csv)

        keluaran_analitik_menit.append([max_kec_menit,max_power_menit,mean_kec_menit,mean_power_menit,std_kec_menit,std_power_menit])
    
        pool_grafik_detik_a.append(a)
        pool_grafik_detik_b.append(b)
        
        pool_grafik_menit_c.append(c)
        pool_grafik_menit_d.append(d)
        pool_data_windrose_detik.append(data_windrose_detik)
        pool_data_windrose_menit.append(data_windrose_menit)
    
        pool_json_raw.append(json_raw_second)
        pool_json_csv.append(json_untuk_csv)
        jcounter+=1

        if(j==file_json_raw[-1]):
            jcounter=0
    print(len(pool_json_csv))
    
    progress.stop()
    root_progress.destroy()

    pool_path_simpan = openFile()
    print(pool_path_simpan)
    kcounter=0
    # buat_folder

    all_folder_needed=[
        "{}\RAW".format(pool_path_simpan),
        "{}\RAW\Per_Detik".format(pool_path_simpan),
        "{}\RAW\Per_Detik\CSV".format(pool_path_simpan),
        "{}\RAW\Per_Detik\JSON".format(pool_path_simpan),
        "{}\RAW\Per_Menit".format(pool_path_simpan),
        "{}\RAW\Per_Menit\CSV".format(pool_path_simpan),
        "{}\RAW\Per_Menit\JSON".format(pool_path_simpan),
        "{}\Grafik".format(pool_path_simpan),
        "{}\Grafik\Per_Detik".format(pool_path_simpan),
        "{}\Grafik\Per_Menit".format(pool_path_simpan),
        "{}\Windrose Bar".format(pool_path_simpan),
        "{}\Windrose Contour".format(pool_path_simpan),
        "{}\Windrose Bar\Per_Detik".format(pool_path_simpan),
        "{}\Windrose Bar\Per_Menit".format(pool_path_simpan),
        "{}\Windrose Contour\Per_Detik".format(pool_path_simpan),
        "{}\Windrose Contour\Per_Menit".format(pool_path_simpan),
        "{}\Analytics".format(pool_path_simpan),
        "{}\Analytics\Per_Detik".format(pool_path_simpan),
        "{}\Analytics\Per_Menit".format(pool_path_simpan)
        ]

    for i in all_folder_needed:
        isExist = os.path.exists(i)

        if not isExist:       
            # Create a new directory because it does not exist 
            os.makedirs("{}".format(i))

   

    for k in tqdm(file_json_raw):
        
        file_name = os.path.basename(k).split('.')[0]
        file_name_custom=file_name.split('-')
        print("\n"+file_name)
        nama_file_proses = ("{}(P)-{}-{}-{}".format(file_name_custom[0],file_name_custom[1],file_name_custom[2],file_name_custom[3]))
        nama_file_analitik = ("{}(A)-{}-{}-{}".format(file_name_custom[0],file_name_custom[1],file_name_custom[2],file_name_custom[3]))
        




        simpan_csv(nama_file_proses,pool_json_csv[kcounter],pool_path_simpan,"m")
        simpan_csv(file_name,pool_json_raw[kcounter],pool_path_simpan,"d")
        simpan_json(nama_file_proses,(json.dumps(pool_json_csv[kcounter])),pool_path_simpan,"m")
        simpan_json(file_name,(json.dumps(pool_json_raw[kcounter])),pool_path_simpan,"d")
        



        buat_grafik(pool_grafik_detik_a,pool_grafik_detik_b,kcounter,pool_path_simpan,file_name,"second",10800)
        buat_grafik(pool_grafik_menit_c,pool_grafik_menit_d,kcounter,pool_path_simpan,file_name,"menit",241)

        df_detik = pd.DataFrame(pool_data_windrose_detik[kcounter])

        df_menit = pd.DataFrame(pool_data_windrose_menit[kcounter])
       
        buat_windrose(df_detik['Derajat_angin'],df_detik['Kec_angin'],pool_path_simpan,file_name,"contour","per detik")

        buat_windrose(df_detik['Derajat_angin'],df_detik['Kec_angin'],pool_path_simpan,file_name,"bar","per detik")


        buat_windrose(df_menit['Derajat_angin'],df_menit['Kec_angin'],pool_path_simpan,file_name,"contour","per menit")

        buat_windrose(df_menit['Derajat_angin'],df_menit['Kec_angin'],pool_path_simpan,file_name,"bar","per menit")

        simpan_excel_openpyxl(pool_path_simpan,nama_file_analitik,pool_json_raw[kcounter],"detik",keluaran_analitik_detik[kcounter],file_name)
        simpan_excel_openpyxl(pool_path_simpan,nama_file_analitik,pool_json_csv[kcounter],"menit",keluaran_analitik_menit[kcounter],file_name)

        kcounter+=1
        if(k==file_json_raw[-1]):
            kcounter=0
    
    print("convert sudah selesai :)")

    process = psutil.Process(os.getpid())  
    print(process.memory_percent())
    print(psutil.Process().memory_info().rss / (1024 * 1024))

    print ("My program took", time.time() - start_time, "to run")



def _quit():
    w.quit()
    w.destroy() 

w=tk.Tk()
w.protocol("WM_DELETE_WINDOW", _quit)
w.geometry('950x400')
w.resizable(False, False)
w.configure(bg='#104c84')

bg = PhotoImage(file="main.png")



my_label = Label(w, image=bg)
my_label.place(x=0,y=0, relheight=1,relwidth=1)






def on_enter(e):
    global new_image
    basewidth = 135
    img = Image.open('baru 1.jpeg')
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize))
    new_image= ImageTk.PhotoImage(img)
    myButton.config(image=new_image)


def on_leave(e):
    global new_image
    basewidth = 135
    img = Image.open('baru 2.jpeg')
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize))
    new_image= ImageTk.PhotoImage(img)
    myButton.config(image=new_image)


basewidth = 135
img = Image.open('baru 2.jpeg')
wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img = img.resize((basewidth, hsize))
new_image= ImageTk.PhotoImage(img)

myButton = Button(w, image=new_image,bd=0,command=main)
myButton.bind('<Enter>', on_enter)
myButton.bind('<Leave>',on_leave)
myButton.place(x=475,y=320,anchor=CENTER)

w.title("PADS 1.0")

p1 = PhotoImage(file = 'logo.png')

# Setting icon of master window
w.iconphoto(False, p1)
w.mainloop()