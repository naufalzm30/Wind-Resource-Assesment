import xlsxwriter

from datetime import datetime

from openpyxl import Workbook
from openpyxl.chart import (
    ScatterChart,
    Reference,
    Series,
)
from openpyxl.drawing.image import Image

def simpan_excel(pool_path_simpan,nama_file_analitik,pool_json_raw,timeType,keluar_analitik):
    
    workbook = xlsxwriter.Workbook('{}\{} per {}.xlsx'.format(pool_path_simpan,nama_file_analitik,timeType))

    Analytics = workbook.add_worksheet('Analytics')
    Analytics.write('P2', 'Kec_angin')
    Analytics.write('Q2', 'Max')
    Analytics.write('Q3', 'Mean')
    Analytics.write('Q4', 'Std')
    Analytics.write('R1', 'U')
    Analytics.write('S1', 'TL')
    Analytics.write('T1', 'T')
    Analytics.write('U1', 'Tg')
    Analytics.write('V1', 'S')
    Analytics.write('W1', 'BD')
    Analytics.write('X1', 'B')
    Analytics.write('Y1', 'BL')
    Analytics.write('P6', 'Theoritical Power')
    Analytics.write('Q6', 'Max')
    Analytics.write('Q7', 'Mean')
    Analytics.write('Q8', 'Std')




    RAW_Data = workbook.add_worksheet('RAW_Data')
    RAW_Data.write('A1', 'ID_Turbin')
    RAW_Data.write('B1', 'Date')
    RAW_Data.write('C1', 'Time')
    RAW_Data.write('D1', 'Kec_angin')
    RAW_Data.write('E1', 'Arah_angin')
    RAW_Data.write('F1', 'Derajat_angin')
    RAW_Data.write('G1', 'Power')


    row = 1
    col = 0

    max_kec=keluar_analitik[0]
    max_power=keluar_analitik[1]
    mean_kec=keluar_analitik[2]
    mean_power=keluar_analitik[3]
    std_kec=keluar_analitik[4]
    std_power=keluar_analitik[5]

    counter_analitik=0
    for A_proses in max_kec:
        Analytics.write(row,col+17+counter_analitik,max_kec[counter_analitik])
        Analytics.write(row+1,col+17+counter_analitik,mean_kec[counter_analitik])
        Analytics.write(row+2,col+17+counter_analitik,std_kec[counter_analitik])

        Analytics.write(row+4,col+17+counter_analitik,max_power[counter_analitik])
        Analytics.write(row+5,col+17+counter_analitik,mean_power[counter_analitik])
        Analytics.write(row+6,col+17+counter_analitik,std_power[counter_analitik])


        
        if (counter_analitik==max_kec[-1]):
            counter_analitik=0
        else:
            counter_analitik+=1
    cell_format = workbook.add_format()
    cell_format.set_num_format('hh:mm:ss')

    for raw in (pool_json_raw):
        # Convert the date string into a datetime object.
        # time_strp = datetime.strptime(time_detik, "%H:%M:%S")


        date_time = datetime.strptime(raw['Time'], '%H:%M:%S')

        RAW_Data.write(row, col, raw['ID_Turbin'])
        RAW_Data.write(row, col+1, raw['Date'] )
        RAW_Data.write_datetime(row, col+2, date_time,cell_format )
        RAW_Data.write_number(row, col+3, raw['Kec_angin'] )
        RAW_Data.write(row, col+4, raw['Arah_angin'] )
        RAW_Data.write(row, col+5, raw['Derajat_angin'] )
        RAW_Data.write_number(row, col+6, raw['Power'] )

        if (raw==pool_json_raw[-1]):
            row=1
        else:
            row += 1

    if (timeType=="detik"):
        range=86401
        interval=10801
    elif (timeType=="menit"):
        range=1441
        interval=360

    # Create a chart object.
    chart = workbook.add_chart({'type': 'scatter','subtype':'straight'})
    chart.add_series({'categories': '=RAW_Data!$C$1:$C${}'.format(range),'values':'=RAW_Data!$D$1:$D${}'.format(range)})
    chart.set_legend({'delete_series': [0]})
    chart.set_x_axis({'date_axis': True,'interval_unit': interval,'num_font':  {'rotation': 45}})
    chart.set_y_axis({'name':'Kecepatan Angin (m/s)'})
    chart.set_size({'width': 800, 'height': 300})
    Analytics.insert_chart(1, 1, chart)


    workbook.close()


def cari_count(json_pool,kec_low,kec_high,kec_0_2):

    arah_angin=["U","TL","T","Tg","S","BD","B","BL"]
    


    jumlah=0
    for i in arah_angin:
        if kec_low!=10:
            coba = sum(((x['Arah_angin']==i) and ((x['Kec_angin']<kec_high) and (x['Kec_angin']>=kec_low)) ) for x in json_pool)
            
        else:
            coba = sum(((x['Arah_angin']==i) and ((x['Kec_angin']>=kec_low)) ) for x in json_pool)
        jumlah+=coba
        kec_0_2.append(coba)
    kec_0_2.append(jumlah)
        



def simpan_excel_openpyxl(pool_path_simpan,nama_file_analitik,pool_json_raw,timeType,keluar_analitik,file_name):
    workbook = Workbook()
    
    sheet1 = workbook.active
    sheet1.title = "Analytics"

    sheet2 = workbook.create_sheet("RAW_Data")

    sheet1['P2']= 'Kec_angin (m/s)'
    sheet1['Q2']= 'Max'
    sheet1['Q3']= 'Mean'
    sheet1['Q4']= 'Std'
    sheet1['R1']= 'U'
    sheet1['S1']= 'TL'
    sheet1['T1']= 'T'
    sheet1['U1']= 'Tg'
    sheet1['V1']= 'S'
    sheet1['W1']= 'BD'
    sheet1['X1']= 'B'
    sheet1['Y1']= 'BL'
    sheet1['P6']= 'Theoritical Power (Watt)'
    sheet1['Q6']= 'Max'
    sheet1['Q7']= 'Mean'
    sheet1['Q8']= 'Std'
    sheet1['I21']= '0-2 m/s'
    sheet1['I22']= '2-4 m/s'
    sheet1['I23']= '4-6 m/s'
    sheet1['I24']= '6-8 m/s'
    sheet1['I25']= '8-10 m/s'
    sheet1['I26']= '10> m/s'
    sheet1['I27']= 'Total Keseluruhan'
    sheet1['J19']= 'wind speed distribution(%)'
    sheet1['J20']= 'U'
    sheet1['K20']= 'TL'
    sheet1['L20']= 'T'
    sheet1['M20']= 'Tg'
    sheet1['N20']= 'S'
    sheet1['O20']= 'BD'
    sheet1['P20']= 'B'
    sheet1['Q20']= 'BL'





    sheet2['A1']='ID_Turbin'
    sheet2['B1']='Date'
    sheet2['C1']='Time'
    sheet2['D1']='Kec_angin'
    sheet2['E1']='Arah_angin'
    sheet2['F1']='Derajat_angin'
    sheet2['G1']='Power'

    max_kec=keluar_analitik[0]
    max_power=keluar_analitik[1]
    mean_kec=keluar_analitik[2]
    mean_power=keluar_analitik[3]
    std_kec=keluar_analitik[4]
    std_power=keluar_analitik[5]



    iterate_row=2
    for raw in (pool_json_raw):
        date_time = datetime.strptime(raw['Time'], '%H:%M:%S').time()

        sheet2.cell(row=iterate_row, column=1).value = raw['ID_Turbin']
        sheet2.cell(row=iterate_row, column=2).value = raw['Date']
        sheet2.cell(row=iterate_row, column=3).value = date_time
        
        sheet2.cell(row=iterate_row, column=4).value = raw['Kec_angin']
        sheet2.cell(row=iterate_row, column=5).value = raw['Arah_angin']
        sheet2.cell(row=iterate_row, column=6).value = raw['Derajat_angin']
        sheet2.cell(row=iterate_row, column=7).value = raw['Power']

        if (raw==pool_json_raw[-1]):
            iterate_row=2
        else:
            iterate_row += 1
    counter_analitik=0
    for A_proses in max_kec:
        sheet1.cell(row=iterate_row,column=18+counter_analitik).value=(max_kec[counter_analitik])
        sheet1.cell(row=iterate_row,column=18+counter_analitik).number_format='0.00'
        sheet1.cell(row=iterate_row+1,column=18+counter_analitik).value=(mean_kec[counter_analitik])
        sheet1.cell(row=iterate_row+1,column=18+counter_analitik).number_format='0.00'
        sheet1.cell(row=iterate_row+2,column=18+counter_analitik).value=(std_kec[counter_analitik])
        sheet1.cell(row=iterate_row+2,column=18+counter_analitik).number_format='0.00'

        sheet1.cell(row=iterate_row+4,column=18+counter_analitik).value=(max_power[counter_analitik])
        sheet1.cell(row=iterate_row+4,column=18+counter_analitik).number_format='0.00'
        sheet1.cell(row=iterate_row+5,column=18+counter_analitik).value=(mean_power[counter_analitik])
        sheet1.cell(row=iterate_row+5,column=18+counter_analitik).number_format='0.00'
        sheet1.cell(row=iterate_row+6,column=18+counter_analitik).value=(std_power[counter_analitik])
        sheet1.cell(row=iterate_row+6,column=18+counter_analitik).number_format='0.00'


        if (counter_analitik==max_kec[-1]):
            counter_analitik=0
        else:
            counter_analitik+=1

    if (timeType=="detik"):
        range=86401
        interval=10801
    elif (timeType=="menit"):
        range=1441
        interval=360


    chart = ScatterChart()

    xvalues = Reference(sheet2, min_col = 3,
                    min_row = 2, max_row = range)
                     
    yvalues = Reference(sheet2, min_col = 4,
                    min_row = 2, max_row = range)

    # create a 1st series of data
    series = Series(values = yvalues, xvalues = xvalues, title ="kec angin")
    
    # add series data to the chart object
    chart.series.append(series)
    
        
    # set the title of the x-axis
    chart.x_axis.title = "Time"
    
    # set the title of the y-axis
    chart.y_axis.title = " Kec Angin (m/s)"

    chart.width=22.5
    
    # add chart to the sheet
    # the top-left corner of a chart
    # is anchored to cell E2 .
    sheet1.add_chart(chart, "A2")


    img = Image('{}\Windrose bar {} per {}.png'.format(pool_path_simpan,file_name,timeType))
    
    #adjusting size
    img.height=450
    img.width =450
    
    #adding img to cell A3

    sheet1.add_image(img, 'A20')

    kec_0_2=[]
    kec_2_4=[]
    kec_4_6=[]
    kec_6_8=[]
    kec_8_10=[]
    kec_10_inf=[]

    cari_count(pool_json_raw,0,2,kec_0_2)
    cari_count(pool_json_raw,2,4,kec_2_4)
    cari_count(pool_json_raw,4,6,kec_4_6)
    cari_count(pool_json_raw,6,8,kec_6_8)
    cari_count(pool_json_raw,8,10,kec_8_10)
    cari_count(pool_json_raw,10,0,kec_10_inf)

    pivot=[kec_0_2,kec_2_4,kec_4_6,kec_6_8,kec_8_10,kec_10_inf]

    row_pivot=21
    U=0.0
    TL=0.0
    T=0.0
    Tg=0.0
    S=0.0
    BD=0.0
    B=0.0
    BL=0.0
    for p in pivot:
        column_pivot=10
        for isi_pivot in p:
            sheet1.cell(row=row_pivot,column=column_pivot).value=((isi_pivot/len(pool_json_raw)))
            sheet1.cell(row=row_pivot,column=column_pivot).number_format = '0.0000%'
            column_pivot+=1
        U+=p[0]
        TL+=p[1]
        T+=p[2]
        Tg+=p[3]
        S+=p[4]
        BD+=p[5]
        B+=p[6]
        BL+=p[7]
        row_pivot+=1

    # sheet1['J27']= "{:.2%}".format((U/len(pool_json_raw)))
    # sheet1['K27']= "{:.2%}".format((TL/len(pool_json_raw)))
    # sheet1['L27']= "{:.2%}".format((T/len(pool_json_raw)))
    # sheet1['M27']= "{:.2%}".format((Tg/len(pool_json_raw)))
    # sheet1['N27']= "{:.2%}".format((S/len(pool_json_raw)))
    # sheet1['O27']= "{:.2%}".format((BD/len(pool_json_raw)))
    # sheet1['P27']= "{:.2%}".format((B/len(pool_json_raw)))
    # sheet1['Q27']= "{:.2%}".format((BL/len(pool_json_raw)))
    sheet1['J27']= (U/len(pool_json_raw))
    sheet1['J27'].number_format='0.0000%'
    sheet1['K27']= (TL/len(pool_json_raw))
    sheet1['K27'].number_format='0.0000%'
    sheet1['L27']= (T/len(pool_json_raw))
    sheet1['L27'].number_format='0.0000%'
    sheet1['M27']= (Tg/len(pool_json_raw))
    sheet1['M27'].number_format='0.0000%'
    sheet1['N27']= (S/len(pool_json_raw))
    sheet1['N27'].number_format='0.0000%'
    sheet1['O27']= (BD/len(pool_json_raw))
    sheet1['O27'].number_format='0.0000%'
    sheet1['P27']= (B/len(pool_json_raw))
    sheet1['P27'].number_format='0.0000%'
    sheet1['Q27']= (BL/len(pool_json_raw))
    sheet1['Q27'].number_format='0.0000%'
    sheet1['R27']= "=SUM(J27:Q27)"
    sheet1['R27'].number_format='0.0%'





    workbook.save('{}\{} per {}.xlsx'.format(pool_path_simpan,nama_file_analitik,timeType))
