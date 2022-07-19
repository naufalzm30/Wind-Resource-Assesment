
from cProfile import label
from datetime import datetime, timedelta
from numpy import dtype, spacing
from method import *
import os, psutil;
import time
import pyglet
import tkinter as tk
from tkinter import filedialog, Text
from tkhtmlview import HTMLLabel
from PIL import Image, ImageTk
start_time = time.time()

# warna 
#104c84


# window= Tk()
# button = Button(text="open file",command=openFile)

# button.pack()
# window.mainloop()
def main():
    pool_json_raw=openFile()

    file_json_raw = (glob.glob('{}\*.json'.format(pool_json_raw)))
    pool_json_raw=[]
    pool_json_csv=[]
    jcounter=0

    for j in file_json_raw:
        a=[]
        b=[]
        json_raw_second=panggil_json_raw(os.path.normpath(j))
        for i in json_raw_second:
            a.append(i["Time"])
            b.append(i["Kec_angin"])
        # plt.figure(jcounter+1)
        # plt.plot(a, b)
        ax1 = plt.figure("per_second_{}".format(jcounter+1),figsize=(10, 3)).add_subplot(111)
        ax1.plot(a, b) 
        # start, end = ax1.get_xlim()
        ax1.set_xticks(a[::10800])
        ax1.set_ylabel("Kec angin m/s")

        json_untuk_csv = proses_per_menit(json_raw_second)

        c=[]
        d=[]
        for z in json_untuk_csv:
            c.append(z["Time"])
            d.append(z["Kec_angin"])

        ax2 = plt.figure("per_menit_{}".format(jcounter+1),figsize=(10, 3)).add_subplot(111)
        ax2.plot(c, d) 
        # start, end = ax1.get_xlim()
        ax2.set_xticks(c[::241])
        ax2.set_ylabel("Kec angin m/s")


        pool_json_raw.append(json_raw_second)
        pool_json_csv.append(json_untuk_csv)
        jcounter+=1

        if(j==file_json_raw[-1]):
            jcounter=0
    print(len(pool_json_csv))
    pool_path_simpan = openFile()
    print(pool_path_simpan)
    kcounter=0
    for k in file_json_raw:
        
        file_name = os.path.basename(k).split('.')[0]
        file_name_custom=file_name.split('-')

        simpan_csv("WRA(P)-22-{}-{}".format(file_name_custom[1],file_name_custom[2]),pool_json_csv[kcounter],pool_path_simpan)
        simpan_csv("WRA-22-{}-{}".format(file_name_custom[1],file_name_custom[2]),pool_json_raw[kcounter],pool_path_simpan)
        simpan_json("WRA(P)-22-{}-{}".format(file_name_custom[1],file_name_custom[2]),(json.dumps(pool_json_csv[kcounter])),pool_path_simpan)
        # plt.figure(kcounter+1)
        # plt.savefig("{}\Line_Chart_Second_{}".format(pool_path_simpan,kcounter))
        plt.figure("per_second_{}".format(kcounter+1),figsize=(10, 3))
        plt.savefig("{}\Grafik per detik WRA-22-{}-{}.png".format(pool_path_simpan,file_name_custom[1],file_name_custom[2]))
        plt.figure("per_menit_{}".format(kcounter+1),figsize=(10, 3))
        plt.savefig("{}\Grafik per menit WRA-22-{}-{}.png".format(pool_path_simpan,file_name_custom[1],file_name_custom[2]))
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