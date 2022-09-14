
from cProfile import label
from datetime import datetime, timedelta
from itertools import count, cycle
from numpy import dtype, spacing


from method import *
from excelsior import *


import datetime
import datetime as dt
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


# class ImageLabel(tk.Label):
#     """
#     A Label that displays images, and plays them if they are gifs
#     :im: A PIL Image instance or a string filename
#     """
#     def load(self, im):
#         if isinstance(im, str):
#             im = Image.open(im)
#         frames = []
 
#         try:
#             for i in count(1):
#                 frames.append(ImageTk.PhotoImage(im.copy()))
#                 im.seek(i)
#         except EOFError:
#             pass
#         self.frames = cycle(frames)
 
#         try:
#             self.delay = im.info['duration']
#         except:
#             self.delay = 100
 
#         if len(frames) == 1:
#             self.config(image=next(self.frames))
#         else:
#             self.next_frame()
 
#     def unload(self):
#         self.config(image=None)
#         self.frames = None
 
#     def next_frame(self):
#         if self.frames:
#             self.config(image=next(self.frames))
#             self.after(self.delay, self.next_frame)


start_time = time.time()


# warna 
#104c84

def _quit():
    w.quit()
    w.destroy() 

w=tk.Tk()
w.protocol("WM_DELETE_WINDOW", _quit)
w.geometry('950x400')
w.resizable(False, False)
w.configure(bg='#104c84')

bg = PhotoImage(file="asset\main.png")



my_label = Label(w, image=bg)
my_label.place(x=0,y=0, relheight=1,relwidth=1)


progress  = ttk.Progressbar(w, orient = HORIZONTAL, length=180)

progress.config(mode='indeterminate')

def main():
    progress.pack(pady=55, side=tk.BOTTOM)
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
        progress.start()
        
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

   

    for k in (file_json_raw):
        w.update()
        
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
    import ctypes  # An included library with Python install.
    def Mbox(title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)
    Mbox('proses wra', 'Proses Selesai', 1)

    progress.pack_forget()

    
    


def image_proses(source):
    basewidth = 135
    img = Image.open(source)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize))
    new_image= ImageTk.PhotoImage(img)
    return new_image




def untuk_buat_folder_RTS(nama_RTS,path_exist):
    isExist = os.path.exists("{}\{}".format(path_exist,nama_RTS))

    if not isExist:
        os.makedirs("{}\{}".format(path_exist,nama_RTS))

    path_exist="{}\{}".format(path_exist,nama_RTS)
    return path_exist

def convert_csv():
    os.system('cls||clear')
    progress.pack(pady=55, side=tk.BOTTOM)
    progress.start()
    filepaths = filedialog.askdirectory()
    pool_raw = filepaths
    print(filepaths)
    file_csv_raw = glob.glob('{}\WRA\*.csv'.format(pool_raw))

    file_csv_raw.extend(
        glob.glob('{}\RTS\**\*.csv'.format(pool_raw), recursive=True))

    isExist = os.path.exists("{}\JSON_olah".format(pool_raw))

    if not isExist:

        # Create a new directory because it does not exist
        os.makedirs("{}\JSON_olah".format(pool_raw))

    kec_angin = []
    count = 0
    for h in file_csv_raw:
        a = os.path.normpath(h)
        print(a)
        csv_file = pd.DataFrame(pd.read_csv("{}".format(
            a), sep=";", header=None, index_col=False, skipinitialspace=True, skip_blank_lines=True))
        # print(csv_file[1])
        # retrieved_elements = list(filter(lambda x: 'WR' in x, csv_file[0]))
        # print(retrieved_elements[0])

        siap_json = []
        print(csv_file[0][1])
        if ((csv_file[0][0][:2]) == "WR"):
            path_exist = "{}\JSON_olah\WRA".format(pool_raw)
            isExist = os.path.exists(path_exist)

            if not isExist:
                os.makedirs("{}\JSON_olah\WRA".format(pool_raw))

            power = []
            power_ro = 1.2
            power_A = 1

            csv_file.columns = ["ID_Device", "Date", "Time",
                                "Kec_angin", "Arah_angin", "Derajat_angin"]
            csv_file = csv_file.assign(Power=lambda x: np.round(
                ((power_ro*power_A*((x.Kec_angin)**3))/2), decimals=4))

            ID_Device = csv_file['ID_Device'].values.tolist()
            Date = csv_file['Date'].values.tolist()
            Time_raw = csv_file['Time'].values.tolist()
            Kec_angin = csv_file['Kec_angin'].values.tolist()
            Arah_angin = csv_file['Arah_angin'].values.tolist()
            Derajat_angin = csv_file['Derajat_angin'].values.tolist()
            Power = csv_file['Power'].values.tolist()
            Time = []
            # print(Time_raw)
            for t in Time_raw:
                try:
                    Time.append('{}'.format(
                        datetime.datetime.strptime(t, "%H:%M:%S").time()))
                except ValueError as ve:
                    Time.append('{}'.format(datetime.timedelta(
                        seconds=(round(float(t)*86400)))))
                    print(datetime.timedelta(seconds=(round(float(t)*86400))))
            print(Time[0])

            count = 0
            for i in ID_Device:
                ke_json = {"ID_Device": ID_Device[count], "Date": Date[count], "Time": Time[count], "Kec_angin": float(
                    Kec_angin[count]), "Arah_angin": Arah_angin[count], "Derajat_angin": int(Derajat_angin[count]), "Power": float(Power[count])}
                siap_json.append(ke_json)
                count += 1
        elif (csv_file[0][1] == "WRA"):
            path_exist = "{}\JSON_olah\WRA".format(pool_raw)
            isExist = os.path.exists(path_exist)

            if not isExist:
                os.makedirs("{}\JSON_olah\WRA".format(pool_raw))

            csv_file.columns = ["ID_Device", "Date", "Time",
                                "Kec_angin", "Arah_angin", "Derajat_angin", 'Power']
            csv_file.drop(csv_file.index[0], inplace=True)
            # print(csv_file)

            ID_Device = csv_file['ID_Device'].values.tolist()
            Date = csv_file['Date'].values.tolist()
            Time_raw = csv_file['Time'].values.tolist()
            Kec_angin = csv_file['Kec_angin'].values.tolist()
            Arah_angin = csv_file['Arah_angin'].values.tolist()
            Derajat_angin = csv_file['Derajat_angin'].values.tolist()
            Power = csv_file['Power'].values.tolist()
            Time = []

            for t in Time_raw:
                try:
                    Time.append('{}'.format(
                        datetime.datetime.strptime(t, "%H:%M:%S").time()))
                except ValueError as ve:
                    Time.append('{}'.format(datetime.timedelta(
                        seconds=(round(float(t)*86400)))))
                    print(datetime.timedelta(seconds=(round(float(t)*86400))))
            print(Time[0])

            count = 0
            for i in ID_Device:
                ke_json = {"ID_Device": ID_Device[count], "Date": Date[count], "Time": Time[count], "Kec_angin": float(
                    Kec_angin[count]), "Arah_angin": Arah_angin[count], "Derajat_angin": int(Derajat_angin[count]), "Power": float(Power[count])}
                siap_json.append(ke_json)
                count += 1

        else:
            path_exist = "{}\JSON_olah\RTS".format(pool_raw)
            isExist = os.path.exists(path_exist)

            if not isExist:
                os.makedirs("{}\JSON_olah\RTS".format(pool_raw))

            if len(csv_file.axes[1]) > 4:
                for i in range(4, len(csv_file.axes[1])):
                    del csv_file[i]

            csv_file.columns = ["ID_Turbin", "Date", "Time", "RTS"]
            ID_Device = csv_file['ID_Turbin'].values.tolist()
            Date = csv_file['Date'].values.tolist()
            Time_raw = csv_file['Time'].values.tolist()
            RTS = csv_file['RTS'].values.tolist()

            Time = []

            for t in Time_raw:
                # print(t)
                try:
                    Time.append('{}'.format(
                        datetime.datetime.strptime(t, "%H:%M:%S").time()))
                except ValueError as ve:
                    Time.append('{}'.format(datetime.timedelta(
                        seconds=(round(float(t)*86400)))))
                    print(datetime.timedelta(seconds=(round(float(t)*86400))))

            count = 0
            for i in ID_Device:
                ke_json = {"ID_Turbin": ID_Device[count], "Date": Date[count],
                          "Time": Time[count], "RTS": float(RTS[count])}
                siap_json.append(ke_json)
                count += 1
            path_exist = untuk_buat_folder_RTS(ID_Device[0], path_exist)

        # print(path_exist)

        try:
            ambil_date = datetime.datetime.strptime(Date[0], "%d/%m/%Y")
        except ValueError as ve:
            try:
                ambil_date = datetime.datetime.strptime(Date[0], "%m/%d/%Y")
            except:
                ambil_date = datetime.datetime.strptime(Date[0], "%Y-%m-%d")

        untuk_filename = datetime.datetime.strftime(ambil_date, "%y-%m-%d")
        file_name = "{}-{}".format(ID_Device[0], untuk_filename)

        path = "{}\{}".format(path_exist, file_name)

        # print(siap_json)

        # print(len(csv_file))

        # df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d %H:%M:%S')
        # csv_file['Time'] = pd.to_datetime(csv_file.Time, format="%H:%M:%S")
        # csv_file['Time']= csv_file['Time'].dt.strftime("%H:%M:%S")
        # csv_file["ID_Device"].str.strip()
        # csv_file["Date"].str.strip()
        # csv_file["Time"].str.strip()
        # csv_file["Derajat_angin"].str.strip()

        with open('{}.json'.format(path), 'w') as outfile:  # as outfile:
            json.dump(siap_json, outfile, indent=4)

        del csv_file
        count += 1
    import ctypes  # An included library with Python install.
    def Mbox(title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)
    Mbox('convert csv to json', 'Proses Selesai', 1)

    progress.pack_forget()

proses_1=image_proses('asset/baru 2.jpeg')
proses_2=image_proses('asset/baru 1.jpeg')




def on_enter(e,source,button):
    
    if button=="myButton":
        myButton.configure(image=source)
    elif button=="myButton2":
        myButton2.configure(image=source)


def on_leave(e,source,button):
    
    if button=="myButton":
        myButton.configure(image=source)
    elif button=="myButton2":
        myButton2.configure(image=source)

# asset_loading = PhotoImage(file="asset\loading.gif")

# loading = Label(w, image=asset_loading)
# loading.place()

myButton = tk.Button(w,bd=0,command=main)
myButton.configure(image=proses_1)
myButton.bind('<Enter>', lambda e, source= proses_2, button="myButton": on_enter(e, source, button))
myButton.bind('<Leave>',lambda e, source= proses_1, button="myButton": on_leave(e, source, button))
myButton.place(x=175,y=260,anchor=CENTER)

myButton2 = tk.Button(w,bd=0,command=convert_csv)
myButton2.configure(image=proses_1)
myButton2.bind('<Enter>', lambda e, source= proses_2, button="myButton2": on_enter(e, source, button))
myButton2.bind('<Leave>',lambda e, source= proses_1, button="myButton2": on_leave(e, source, button))
myButton2.place(x=335,y=260,anchor=CENTER)

# myButton2 = Button(w, image=new_image,bd=0,command=main)
# myButton2.bind('<Enter>', on_enter)
# myButton2.bind('<Leave>',on_leave)
# myButton2.place(x=375,y=220,anchor=CENTER)

w.title("PADS 1.0")

p1 = PhotoImage(file = 'asset\logo.png')

# Setting icon of master window
w.iconphoto(False, p1)
w.mainloop()