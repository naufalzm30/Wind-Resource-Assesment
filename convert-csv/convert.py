
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
                
        #JANGAN DI HAPUS INI BUAT DAPETIN MIN MAX
        # get data max
        # max_attr = max(barat_daya, key=lambda x: x['Kec_angin'])
        # min_attr = min(barat_daya, key=lambda x: x['Kec_angin'])
        # print(len(barat_daya))
        # print(max_attr)
        # print(min_attr)


        pool_data_windrose.append(data_windrose)
        
        pool_grafik_menit_c.append(c)
        pool_grafik_menit_d.append(d)



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
    for k in tqdm(file_json_raw):
        
        file_name = os.path.basename(k).split('.')[0]
        file_name_custom=file_name.split('-')

        simpan_csv("WRA(P)-22-{}-{}".format(file_name_custom[2],file_name_custom[3]),pool_json_csv[kcounter],pool_path_simpan)
        simpan_csv("WRA-22-{}-{}".format(file_name_custom[2],file_name_custom[3]),pool_json_raw[kcounter],pool_path_simpan)
        simpan_json("WRA(P)-22-{}-{}".format(file_name_custom[2],file_name_custom[3]),(json.dumps(pool_json_csv[kcounter])),pool_path_simpan)
        nama_file_simpan.append("WRA-22-{}-{}".format(file_name_custom[2],file_name_custom[3]))
            


        # Create a Pandas dataframe from some data.
        # df = pd.DataFrame({'Time':pool_grafik_detik_a[kcounter],'Kec_angin':pool_grafik_detik_b[kcounter]})
        
        # df['Time']= df['Time'].astype('string')


        # df_m = pd.DataFrame({'Time':pool_grafik_menit_c[kcounter],'Kec_angin':pool_grafik_menit_d[kcounter]})
        
        # df_m['Time']= df_m['Time'].astype('string')

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        # writer = pd.ExcelWriter('{}\dashboard WRA-22-{}-{}.xlsx'.format(pool_path_simpan,file_name_custom[2],file_name_custom[3]), engine='xlsxwriter')

        workbook = xlsxwriter.Workbook('{}\WRA(A)-22-{}-{}.xlsx'.format(pool_path_simpan,file_name_custom[2],file_name_custom[3]))
        worksheet_1 = workbook.add_worksheet('per_detik')
        worksheet_2 = workbook.add_worksheet('per_menit')

        # time_format = workbook.add_format({'num_format': 'h:mm:ss'})
        worksheet_1.write('A1', 'Time')
        worksheet_1.write('B1', 'Kec_angin')
        worksheet_2.write('A1', 'Time')
        worksheet_2.write('B1', 'Kec_angin')

        row = 1
        col = 0

        for time_detik in (pool_grafik_detik_a[kcounter]):
            # Convert the date string into a datetime object.
            # time_strp = datetime.strptime(time_detik, "%H:%M:%S")

            worksheet_1.write(row, col, time_detik)
            worksheet_1.write(row, col+1, pool_grafik_detik_b[kcounter][row-1] )

            if (time_detik==pool_grafik_detik_a[kcounter][-1]):
                row=1
            else:
                row += 1
        print(row)
        for time_menit in (pool_grafik_menit_c[kcounter]):
            # Convert the date string into a datetime object.
            # time_strp = datetime.strptime(time_menit, "%H:%M:%S")

            worksheet_2.write(row, col, time_menit)
            worksheet_2.write(row, col+1, pool_grafik_menit_d[kcounter][row-1] )

            if (time_menit==pool_grafik_menit_c[kcounter][-1]):
                row=1
            else:
                row += 1
        # worksheet_1.set_column('A:A', None, time_format) 
        # worksheet_2.set_column('A:A', None, time_format) 
        # Convert the dataframe to an XlsxWriter Excel object.
        # df.to_excel(writer, sheet_name='per_detik',index=False)

        # df_m.to_excel(writer, sheet_name='per_menit',index=False)

        # Get the xlsxwriter workbook and worksheet objects.
        # workbook  = writer.book

        # my_format = workbook.add_format()
        # my_format.set_num_format('hh:mm:ss')
        # worksheet_1 = writer.sheets['per_detik']
        # worksheet_2 = writer.sheets['per_menit']
        # worksheet_1.set_column('A:A', None, my_format)
        # worksheet_2.set_column('A:A', None, my_format)

        # Create a chart object.
        chart = workbook.add_chart({'type': 'line'})
        chart_menit=workbook.add_chart({'type': 'line'})


        # Get the dimensions of the dataframe.
        # (max_row, max_col) = df.shape

        # Configure the series of the chart from the dataframe data.
        chart.add_series({'categories': '=per_detik!$A$1:$A$86401','values':'=per_detik!$B$1:$B$86401'})

        chart.set_legend({'delete_series': [0]})

        chart.set_x_axis({'text_axis': True,'interval_unit': 10801,'num_font':  {'rotation': 45}})

        chart.set_y_axis({'name':'Kecepatan Angin (m/s)'})

        chart_menit.add_series({'categories': '=per_menit!$A$1:$A$1441','values':'=per_menit!$B$1:$B$1441'})

        chart_menit.set_x_axis({'text_axis': True})

        chart_menit.set_y_axis({'name':'Kecepatan Angin (m/s)'})

        chart_menit.set_legend({'delete_series': [0]})
        # Insert the chart into the worksheet.
        worksheet_1.insert_chart(1, 3, chart)

        worksheet_2.insert_chart(1, 3, chart_menit)

        workbook.close()


        ax1 = plt.figure("per_second_{}".format(kcounter+1),figsize=(10, 3)).add_subplot(111)
        ax1.plot(pool_grafik_detik_a[kcounter], pool_grafik_detik_b[kcounter]) 
        # start, end = ax1.get_xlim()
        ax1.set_xticks(pool_grafik_detik_a[kcounter][::10800])
        ax1.set_ylabel("Kec angin m/s")
        plt.savefig("{}\Grafik per detik WRA-22-{}-{}.png".format(pool_path_simpan,file_name_custom[2],file_name_custom[3]))
        plt.close(plt.figure("per_second_{}".format(kcounter+1),figsize=(10, 3)))

        ax2 = plt.figure("per_menit_{}".format(kcounter+1),figsize=(10, 3)).add_subplot(111)
        ax2.plot(pool_grafik_menit_c[kcounter], pool_grafik_menit_d[kcounter]) 
        # start, end = ax1.get_xlim()
        ax2.set_xticks(pool_grafik_menit_c[kcounter][::241])
        ax2.set_ylabel("Kec angin m/s")
        plt.savefig("{}\Grafik per menit WRA-22-{}-{}.png".format(pool_path_simpan,file_name_custom[2],file_name_custom[3]))
        plt.close(plt.figure("per_menit_{}".format(kcounter+1),figsize=(10, 3)))
        

        df = pd.DataFrame(pool_data_windrose[kcounter])
        wx = WindroseAxes.from_ax()
        wx.contour(df['Derajat_angin'],df['Kec_angin'],bins=np.arange(0, 5), cmap=cm.hot, lw=3)
        wx.set_legend(bbox_to_anchor=[-0.1, 0],loc='lower left')
        plt.savefig("{}\Windrose contour WRA-22-{}-{}.png".format(pool_path_simpan,file_name_custom[2],file_name_custom[3]))
        plt.close()

        wx = WindroseAxes.from_ax()
        wx.bar(df['Derajat_angin'],df['Kec_angin'],opening=0.8)
        wx.set_legend(bbox_to_anchor=[-0.1, 0],loc='lower left')
        plt.savefig("{}\Windrose bar WRA-22-{}-{}.png".format(pool_path_simpan,file_name_custom[2],file_name_custom[3]))
        plt.close()
        
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