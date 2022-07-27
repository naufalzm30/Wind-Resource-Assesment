
from cProfile import label
from datetime import datetime, timedelta
from logging import root
import string
from numpy import dtype, spacing
from method import *
import os, psutil;
import time
import pyglet
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, Text
from tkhtmlview import HTMLLabel
from PIL import Image, ImageTk
from operator import attrgetter
import pandas as pd
import matplotlib.cm as cm
from math import pi
from windrose import WindroseAxes
from tqdm import tqdm_gui


start_time = time.time()


# warna 
#104c84


# window= Tk()
# button = Button(text="open file",command=openFile)

# button.pack()
# window.mainloop()
def main():
    root_progress = Tk()
    progress  = ttk.Progressbar(root_progress, orient = HORIZONTAL, length=180)
    progress.pack()
    progress.config(mode='indeterminate')
    progress.start()
    pool_json_raw=openFile()

    file_json_raw = (glob.glob('{}\*.json'.format(pool_json_raw)))
    pool_json_raw=[]
    pool_json_csv=[]
    jcounter=0
    pool_data_windrose=[]
    pool_grafik_detik_a=[]
    pool_grafik_detik_b=[]
    pool_grafik_menit_c=[]
    pool_grafik_menit_d=[]
    for j in (file_json_raw):
        a=[]
        b=[]
        json_raw_second=panggil_json_raw(os.path.normpath(j))
        for i in json_raw_second:
            a.append(i["Time"])
            b.append(i["Kec_angin"])
        pool_grafik_detik_a.append(a)
        pool_grafik_detik_b.append(b)
        # plt.figure(jcounter+1)
        # plt.plot(a, b)
        # ax1 = plt.figure("per_second_{}".format(jcounter+1),figsize=(10, 3)).add_subplot(111)
        # ax1.plot(a, b) 
        # # start, end = ax1.get_xlim()
        # ax1.set_xticks(a[::10800])
        # ax1.set_ylabel("Kec angin m/s")
        # plt.close(plt.figure("per_second_{}".format(jcounter+1),figsize=(10, 3)))
        json_untuk_csv = proses_per_menit(json_raw_second)
        # print(json_untuk_csv)
        c=[]
        d=[]
        r=[]
        
        utara=[]
        timur_laut=[]
        timur=[]
        tenggara=[]
        selatan=[]
        barat_daya=[]
        barat=[]
        barat_laut=[]

        data_windrose=[]

        for z in (json_untuk_csv):
            c.append(z["Time"])
            d.append(z["Kec_angin"])
            r.append(z["Arah_angin"])
            match z['Arah_angin']:
                case 'U':
                    param_arah_angin={"Derajat_angin":z['Derajat_angin'],"Kec_angin":z['Kec_angin']}
                    utara.append(param_arah_angin)
                    data_windrose.append(param_arah_angin)
                case 'TL':
                    param_arah_angin={"Derajat_angin":z['Derajat_angin'],"Kec_angin":z['Kec_angin']}
                    timur_laut.append(param_arah_angin)
                    data_windrose.append(param_arah_angin)
                case 'T':
                    param_arah_angin={"Derajat_angin":z['Derajat_angin'],"Kec_angin":z['Kec_angin']}
                    timur.append(param_arah_angin)
                    data_windrose.append(param_arah_angin)
                case 'Tg':
                    param_arah_angin={"Derajat_angin":z['Derajat_angin'],"Kec_angin":z['Kec_angin']}
                    tenggara.append(param_arah_angin)
                    data_windrose.append(param_arah_angin)
                case 'S':
                    param_arah_angin={"Derajat_angin":z['Derajat_angin'],"Kec_angin":z['Kec_angin']}
                    selatan.append(param_arah_angin)
                    data_windrose.append(param_arah_angin)
                case 'BD':
                    param_arah_angin={"Derajat_angin":z['Derajat_angin'],"Kec_angin":z['Kec_angin']}
                    barat_daya.append(param_arah_angin)
                    data_windrose.append(param_arah_angin)
                case 'B':
                    param_arah_angin={"Derajat_angin":z['Derajat_angin'],"Kec_angin":z['Kec_angin']}
                    barat.append(param_arah_angin)
                    data_windrose.append(param_arah_angin)
                case 'BL':
                    param_arah_angin={"Derajat_angin":z['Derajat_angin'],"Kec_angin":z['Kec_angin']}
                    barat_laut.append(param_arah_angin)
                    data_windrose.append(param_arah_angin)
                

        # get data max
        # max_attr = max(barat_daya, key=lambda x: x['Kec_angin'])
        # min_attr = min(barat_daya, key=lambda x: x['Kec_angin'])
        # print(len(barat_daya))
        # print(max_attr)
        # print(min_attr)



         
        # df['Arah_angin']=df['Arah_angin'].astype('string')
        # print(df['Arah_angin'])
        # wx = WindroseAxes.from_ax()
        # wx.bar(df.Arah_angin, df.Kec_angin, normed=True, opening=0.8, edgecolor='white')
        # wx.set_legend()
        pool_data_windrose.append(data_windrose)
        
        pool_grafik_menit_c.append(c)
        pool_grafik_menit_d.append(d)

        # ax2 = plt.figure("per_menit_{}".format(jcounter+1),figsize=(10, 3)).add_subplot(111)
        # ax2.plot(c, d) 
        # # start, end = ax1.get_xlim()
        # ax2.set_xticks(c[::241])
        # ax2.set_ylabel("Kec angin m/s")
        # plt.close(plt.figure("per_menit_{}".format(jcounter+1),figsize=(10, 3)))

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
    nama_file_simpan=[]
    for k in (file_json_raw):
        
        file_name = os.path.basename(k).split('.')[0]
        file_name_custom=file_name.split('-')

        simpan_csv("WRA(P)-22-{}-{}".format(file_name_custom[1],file_name_custom[2]),pool_json_csv[kcounter],pool_path_simpan)
        simpan_csv("WRA-22-{}-{}".format(file_name_custom[1],file_name_custom[2]),pool_json_raw[kcounter],pool_path_simpan)
        simpan_json("WRA(P)-22-{}-{}".format(file_name_custom[1],file_name_custom[2]),(json.dumps(pool_json_csv[kcounter])),pool_path_simpan)
        nama_file_simpan.append("WRA-22-{}-{}".format(file_name_custom[1],file_name_custom[2]))
        # plt.figure(kcounter+1)
        # plt.savefig("{}\Line_Chart_Second_{}".format(pool_path_simpan,kcounter))

        # plt.figure("per_second_{}".format(kcounter+1),figsize=(10, 3)).set_canvas(new_manager.canvas)        
        # plt.savefig("{}\Grafik per detik WRA-22-{}-{}.png".format(pool_path_simpan,file_name_custom[1],file_name_custom[2]))
        # plt.close(plt.figure("per_second_{}".format(kcounter+1),figsize=(10, 3)))

        # plt.figure("per_menit_{}".format(kcounter+1),figsize=(10, 3)).set_canvas(new_manager2.canvas) 
        # plt.savefig("{}\Grafik per menit WRA-22-{}-{}.png".format(pool_path_simpan,file_name_custom[1],file_name_custom[2]))
        # plt.close(plt.figure("per_menit_{}".format(kcounter+1),figsize=(10, 3)))

        
        # savefig() supports eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff
        
        ax1 = plt.figure("per_second_{}".format(kcounter+1),figsize=(10, 3)).add_subplot(111)
        ax1.plot(pool_grafik_detik_a[kcounter], pool_grafik_detik_b[kcounter]) 
        # start, end = ax1.get_xlim()
        ax1.set_xticks(pool_grafik_detik_a[kcounter][::10800])
        ax1.set_ylabel("Kec angin m/s")
        plt.savefig("{}\Grafik per detik WRA-22-{}-{}.png".format(pool_path_simpan,file_name_custom[1],file_name_custom[2]))
        plt.close(plt.figure("per_second_{}".format(kcounter+1),figsize=(10, 3)))

        ax2 = plt.figure("per_menit_{}".format(kcounter+1),figsize=(10, 3)).add_subplot(111)
        ax2.plot(pool_grafik_menit_c[kcounter], pool_grafik_menit_d[kcounter]) 
        # start, end = ax1.get_xlim()
        ax2.set_xticks(pool_grafik_menit_c[kcounter][::241])
        ax2.set_ylabel("Kec angin m/s")
        plt.savefig("{}\Grafik per menit WRA-22-{}-{}.png".format(pool_path_simpan,file_name_custom[1],file_name_custom[2]))
        plt.close(plt.figure("per_menit_{}".format(kcounter+1),figsize=(10, 3)))
        

        df = pd.DataFrame(pool_data_windrose[kcounter])
        wx = WindroseAxes.from_ax()
        wx.contour(df['Derajat_angin'],df['Kec_angin'],bins=np.arange(0, 5), cmap=cm.hot, lw=3)
        wx.set_legend(bbox_to_anchor=[-0.1, 0],loc='lower left')
        plt.savefig("{}\Windrose WRA-22-{}-{}.png".format(pool_path_simpan,file_name_custom[1],file_name_custom[2]))
        plt.close()
        
        kcounter+=1
        if(k==file_json_raw[-1]):
            kcounter=0
    
    # for windrose in pool_data_windrose:
    #     df = pd.DataFrame(windrose)
    #     wx = WindroseAxes.from_ax()
    #     wx.contour(df['Derajat_angin'],df['Kec_angin'],bins=np.arange(0, 5, 4), cmap=cm.hot, lw=3)
    #     wx.set_legend(bbox_to_anchor=[-0.1, 0],loc='lower left')
    #     plt.savefig("{}\Windrose {}.png".format(pool_path_simpan,nama_file_simpan[wcounter]))
    #     plt.close()
    #     wcounter+=1

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

# label_button= Label(w,image=new_image,borderwidth=0)
# label_button.place(x=475,y=320,anchor='center')
# photoimage = PhotoImage(file="main.png", width=900)
# canvas.create_image(500, 200, image=photoimage)


# MyLabel = Label(w,text="tes\nhd",font=('Wonderbar',45))
# MyLabel.configure(bg='#104c84',fg='yellow',pady=100)
# MyLabel.pack()

# MyLabel1 = Label(w,text="hehe",font=('Wonderbar',25))
# MyLabel1.configure(bg='#104c84',fg='yellow')
# MyLabel1.pack()

myButton = Button(w, image=new_image,bd=0,command=main)
myButton.bind('<Enter>', on_enter)
myButton.bind('<Leave>',on_leave)
myButton.place(x=475,y=320,anchor=CENTER)

w.title("PADS 1.0")

p1 = PhotoImage(file = 'logo.png')

# Setting icon of master window
w.iconphoto(False, p1)
w.mainloop()