import argparse
import xlrd # Import the package
import xlwt
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
from myfun import *
import csv
import sys
import xml.etree.cElementTree as ET

parser = argparse.ArgumentParser(description=' soil omisture simulation')

##1. Climate
##    - Un unico file in cui sono immagazzinati i dati relativi a Rain e ET , colonna 10 e 12 di BATT_2013.txt 
parser.add_argument('Climate')
col_clim_rain=0
col_clim_T=6
col_clim_rhmin=2
col_clim_Ud=3
col_clim_p=4
col_clim_n_N=5
col_clim_ET=1
col_clim_delta=7
col_clim_rn=8
col_clim_u2=9
col_clim_es=10
col_clim_ea=11
col_clim_gamma=12
col_clim_lambda=13
col_clim_alpha=14


####2. Soil
####    - dati relativi a soil: n, s_1, s*, s_w, s_taget, s_tilde per una matrice di ID soil 
####altri_input_pesco_Mellone_dati.txt
parser.add_argument('Soil')
col_soil_s_w=0
col_soil_s_1=1
col_soil_s_c=2
col_soil_n=3
col_soil_s_tilde=4
col_soil_s_target=5


####3. crop
parser.add_argument('Crop')
col_crop_Zr=0
col_crop_Kc=1
col_crop_Ymax=2
col_crop_etseas50=3
col_crop_aopt=4
col_crop_g_plus=5
col_crop_a=6
col_crop_b0=7
col_crop_s_xi=8

####4. Management
####    - File relativo ad irrigazione  colonna 11 di BATT_2013.txt 
parser.add_argument('Management')

## id cell
parser.add_argument('IDcell')

## use Blaney_Criddle 0=no 1=BC, 2 PM
parser.add_argument('ET')

#### random rain 0=mp 1=yes
parser.add_argument('rainrandom')

### outputfile,  xls o csv
parser.add_argument('outputfile')

##  vico2011  o vico2013
parser.add_argument('vico')

##  soil moisture start
parser.add_argument('soilmoisture_start')

args = parser.parse_args()
idcell=int(args.IDcell)
input_clim=args.Climate
input_soil=args.Soil
input_crop=args.Crop
input_manage=args.Management
if args.rainrandom.find("N")>=0:
    rainrandom=0
if args.rainrandom.find("Y")>=0:
    rainrandom=1
if args.rainrandom.find("N")<0 and args.rainrandom.find("Y")<0:
    print "wrong rain input: N,Y"
    sys.exit()

if args.ET.find("N")>=0:
    print " loading ET "
    use_bc=0
if args.ET.find("BC")>=0:
    print "BC "
    use_bc=1
if args.ET.find("PM")>=0:
    print("PM")
    use_bc=2
if args.ET.find("N")<0 and args.ET.find("BC")<0 and args.ET.find("PM")<0 :
    print "wrong ET input : NO,BC,PM"
    sys.exit()
    
outputfile=args.outputfile
vico=args.vico
###### LOAD INPUT FILES

## climate
if input_clim.find(".xls")>0:
        book_clim = xlrd.open_workbook(input_clim)# load climate
        sheet_clim = book_clim.sheet_by_index(0) # Get the first sheet
        T_bc=sheet_clim.col_values(col_clim_T, start_rowx=1, end_rowx=None)
        p_bc=sheet_clim.col_values(col_clim_p, start_rowx=1, end_rowx=None)
        rhmin_bc=sheet_clim.col_values(col_clim_rhmin, start_rowx=1, end_rowx=None)
        n_N_bc=sheet_clim.col_values(col_clim_n_N, start_rowx=1, end_rowx=None)
        Ud_bc=sheet_clim.col_values(col_clim_Ud, start_rowx=1, end_rowx=None)
        delta=sheet_clim.col_values(col_clim_delta, start_rowx=1, end_rowx=None)
        rn=sheet_clim.col_values(col_clim_rn, start_rowx=1, end_rowx=None)
        u2=sheet_clim.col_values(col_clim_u2, start_rowx=1, end_rowx=None)
        es=sheet_clim.col_values(col_clim_es, start_rowx=1, end_rowx=None)
        ea=sheet_clim.col_values(col_clim_ea, start_rowx=1, end_rowx=None)
        gamma=sheet_clim.cell_value(1,col_clim_gamma)
        alpha=sheet_clim.cell_value(1,col_clim_alpha)
        lamb=sheet_clim.cell_value(1,col_clim_lambda)
        if use_bc == 0 :
            ET_max=sheet_clim.col_values(col_clim_ET, start_rowx=1, end_rowx=None)
        if rainrandom==0:
            R=sheet_clim.col_values(col_clim_rain, start_rowx=1, end_rowx=None) #rain

             
if input_clim.find(".csv")>0:
       with open(input_clim,'rb') as csvfile:
            sheet_clim=csv.reader(csvfile, delimiter=',', quotechar='"')
            R=[];
            ET_max=[]
            T_bc=[]
            p_bc=[] 
            rhmin_bc=[] 
            n_N_bc=[] 
            Ud_bc=[]
            ET_max=[]
            delta=[]
            rn=[] 
            u2=[] 
            es=[] 
            ea=[]
            
            for row in sheet_clim:
                if sheet_clim.line_num > 1:
                    T_bc.append(float(row[col_clim_T].replace(',','.')))
                    p_bc.append(float(row[col_clim_p].replace(',','.')))
                    rhmin_bc.append(float(row[col_clim_rhmin].replace(',','.')))
                    n_N_bc.append(float(row[col_clim_n_N].replace(',','.')))
                    Ud_bc.append(float(row[col_clim_Ud].replace(',','.')))

                    delta.append(float(row[col_clim_delta].replace(',','.')))
                    rn.append(float(row[col_clim_rn].replace(',','.')))
                    u2.append(float(row[col_clim_u2].replace(',','.')))
                    es.append(float(row[col_clim_es].replace(',','.')))
                    ea.append(float(row[col_clim_ea].replace(',','.')))
                    if sheet_clim.line_num == 2:
                        gamma=float(row[col_clim_gamma].replace(',','.'))
                        alpha=float(row[col_clim_alpha].replace(',','.'))
                        lamb=float(row[col_clim_lambda].replace(',','.'))
                    if rainrandom==0:
                        R.append(float(row[col_clim_rain].replace(',','.')))
                    if use_bc == 0 :
                        ET_max.append(float(row[col_clim_ET].replace(',','.')))


if use_bc == 1 :
        ET_max=et_Blaney_Criddle(T_bc,p_bc,rhmin_bc,n_N_bc,Ud_bc)
        wb = xlwt.Workbook()
        ws = wb.add_sheet('sheet 1')
        for ctr in range(len(ET_max)):
            ws.write(ctr, 0, ET_max[ctr])
        wb.save('et_Blaney_Criddle.xls')

if use_bc == 2 :
        
        
        ET_max=et_PM(T_bc,delta,rn,u2,es,ea,gamma)
        wb = xlwt.Workbook()
        ws = wb.add_sheet('sheet 1')
        for ctr in range(len(ET_max)):
            ws.write(ctr, 0, ET_max[ctr])
        wb.save('et_PM.xls')

if rainrandom > 0:
    Ndays=len(T_bc)
    R=[0] * Ndays
    for t in range(Ndays):
        r=np.random.rand(1)
        if r<lamb:
            e=np.random.exponential(alpha,1)
            R[t]=e[0]
        if r>=lamb:
            R[t]=0
          
## soil
if input_soil.find(".xls")>0: 
        book_soil = xlrd.open_workbook(input_soil)# load soil
        sheet_soil = book_soil.sheet_by_index(0) # Get the first sheet
        p=Param()
        p.s_1=sheet_soil.cell_value(idcell,col_soil_s_1)
        p.s_c=sheet_soil.cell_value(idcell,col_soil_s_c)
        p.s_w=sheet_soil.cell_value(idcell,col_soil_s_w)
        p.n=sheet_soil.cell_value(idcell,col_soil_n)
        

if input_soil.find(".csv")>0:
        p=Param()
        with open(input_soil,'rb') as csvfile_soil:
            sheet_soil=csv.reader(csvfile_soil, delimiter=',', quotechar='"')
            for row in sheet_soil:
                if sheet_soil.line_num ==idcell+ 1: # idcell= 0,1,..
                    p.s_1=float(row[col_soil_s_1].replace(',','.')) 
                    p.s_c=float(row[col_soil_s_c].replace(',','.')) 
                    p.s_w=float(row[col_soil_s_w].replace(',','.')) 
                    p.n=float(row[col_soil_n].replace(',','.'))

## crop
if input_crop.find(".xls")>0:                    
        book_crop = xlrd.open_workbook(input_crop)
        sheet_crop = book_crop.sheet_by_index(0) # Get the first sheet
        Zr=sheet_crop.col_values(col_crop_Zr, start_rowx=1, end_rowx=None)
        Y_max=sheet_crop.cell_value(1,col_crop_Ymax)
        Et_seas_50=sheet_crop.cell_value(1,col_crop_etseas50)
        a_opt=sheet_crop.cell_value(1,col_crop_aopt)
        p.g_plus=sheet_crop.cell_value(1,col_crop_g_plus) 
        p.a=sheet_crop.cell_value(1,col_crop_a)         
        p.b0=sheet_crop.cell_value(1,col_crop_b0)         
        #p.s_xi = sheet_crop.cell_value(1,col_crop_s_xi)
        
if input_crop.find(".csv")>0:
        with open(input_crop,'rb') as csvfile:
                sheet_crop=csv.reader(csvfile, delimiter=',', quotechar='"')
                Zr=[];
                for row in sheet_crop:
                        if sheet_crop.line_num > 1:
                            Zr.append(float(row[col_crop_Zr].replace(',','.')))
                        if sheet_crop.line_num == 2:
                            Y_max=float(row[col_crop_Ymax].replace(',','.'))
                            Et_seas_50=float(row[col_crop_etseas50].replace(',','.'))
                            a_opt=float(row[col_crop_aopt].replace(',','.'))
                            
                            p.g_plus=float(row[col_crop_g_plus].replace(',','.'))
                            p.a=float(row[col_crop_a].replace(',','.'))
                            p.b0=float(row[col_crop_b0].replace(',','.'))
                            #p.s_xi=float(row[col_crop_s_xi].replace(',','.'))

## manage
if input_manage.find(".xls")>0:                           
        book_manage = xlrd.open_workbook(input_manage)
        sheet_manage = book_manage.sheet_by_index(0) # Get the first sheet
        I=sheet_manage.col_values(0, start_rowx=1, end_rowx=None)
        CU=sheet_manage.cell_value(1, 1)
       
if input_manage.find(".csv")>0:
        with open(input_manage,'rb') as csvfile:
            sheet_manage=csv.reader(csvfile, delimiter=',', quotechar='"')
            I=[]
            
            for row in sheet_manage:
                if sheet_manage.line_num == 2:
                    CU=(float(row[1].replace(',','.'))) 
                if sheet_manage.line_num > 1:
                    I.append(float(row[0].replace(',','.')))        
                   
                   
                  
######END LOAD INPUT FILES ##########

##s_start=p.s_c
s_start=float(args.soilmoisture_start)
Ndays=len(R)
ICU=[0] * (Ndays)
for t in range(Ndays):
    ICU[t]=I[t]*CU

    
out=soil_moisture_simulation_R_ET_Z_I(p,Ndays,s_start,R,ET_max,Zr,ICU);
outg=crop_development_simulation_R_ET_Z_I(p,Ndays,s_start,R,ET_max,Zr,ICU);

s=out.s
LQ_norm=out.LQ_norm
stress=out.stress
ET_norm=out.ET_norm


v_irr=out.vol_irr
cropdev=outg.b
s.remove(s[len(s)-1])
stress.remove(stress[len(stress)-1])
ET_norm.remove(ET_norm[len(ET_norm)-1])
cropdev.remove(cropdev[len(cropdev)-1])


et=[0] * (Ndays)
for t in range(Ndays):
    et[t]=ET_norm[t]*Zr[t]*p.n

y_vico_2011=Y_vico2011(sum(ET_norm),Y_max,Et_seas_50,a_opt)
p1=0
p2=0.8
y_vico_2013=p1+p2*outg.b[len(outg.b)-1]
if vico.find("EMP")>=0:
        y=y_vico_2011
        
if vico.find("DIC")>=0:
        y=y_vico_2013

if vico.find("EMP")<0 and vico.find("DIC")<0:
        print "WRONG VICO INPUT: EMP , DIC"
        sys.exit()
v_irr_end=v_irr[len(v_irr)-2]
sumR=sum(R)

#wp_vico_2011=WP(y_vico_2011,v_irr_end,sumR,0);
wp=WP(y,v_irr_end,sumR,0);

WaterFootprint = 1/wp
effectivewater=sum(et)/ (v_irr_end+sumR)

print p.s_xi
### output file

col_out_rain=0;
col_out_s=2;
col_out_stress=3;
col_out_lq=4;
col_out_ew=6;
col_out_wf=8;
col_out_y=7;
col_out_et=1;
col_out_crop=5;

if outputfile.find(".xls")>0:
        wb2 = xlwt.Workbook()
        ws2 = wb2.add_sheet('sheet 1')
        ws2.write(0, col_out_s, " Soil moisture")
        ws2.write(0, col_out_stress, " Stress")
        ws2.write(0, col_out_lq, " Lq")
        ws2.write(0, col_out_ew, " Effective user of water")
        ws2.write(0, col_out_wf,"  WaterFootprin")
        ws2.write(0, col_out_y, " Yeld")
        ws2.write(0, col_out_et, " ETnorm")
        ws2.write(0, col_out_crop, " crop development")
        ws2.write(0, col_out_rain, " rain")
        for ctr in range(len(s)):
            ws2.write(ctr+1, col_out_s, s[ctr])
        for ctr in range(len(stress)):
            ws2.write(ctr+1, col_out_stress, stress[ctr])
        for ctr in range(len(Zr)):
            ws2.write(ctr+1, col_out_lq, LQ_norm[ctr]*p.n*Zr[ctr])
        for ctr in range(len(ET_norm)):
            ws2.write(ctr+1, col_out_et, ET_norm[ctr])
        for ctr in range(len(cropdev)):
            ws2.write(ctr+1, col_out_crop, cropdev[ctr])
        for ctr in range(len(R)):
            ws2.write(ctr+1, col_out_rain, R[ctr])
        ws2.write(1, col_out_ew, effectivewater)
        ws2.write(1, col_out_wf, WaterFootprint)
        ws2.write(1, col_out_y, y)
        wb2.save(outputfile)
        
if outputfile.find(".csv")>0:
        
        with open(outputfile, 'wb') as csvfile:
            csvwriter=csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(['rain','ETnorm','Soil moisture','Stress','Lq','crop development','Effective user of water','Yeld','WaterFootprin'  ])
            csvwriter.writerow([R[0],ET_norm[0], s[0],stress[0],LQ_norm[0]*p.n*Zr[0],cropdev[0],effectivewater,y,WaterFootprint ])
            for ctr in range(len(s)-1):
                    csvwriter.writerow([R[ctr+1],ET_norm[ctr+1], s[ctr+1],stress[ctr+1],LQ_norm[ctr+1]*p.n*Zr[ctr+1],cropdev[ctr+1],0,0,0 ])
                   

## write project file
outputfileproj=outputfile[0:len(outputfile)-3]+'xml'                  
root=ET.Element("root")
doc=ET.SubElement(root,"doc")
ET.SubElement(doc,"field1",name="climate").text=input_clim
ET.SubElement(doc,"field2",name="management").text=input_manage
ET.SubElement(doc,"field3",name="soil").text=input_soil
ET.SubElement(doc,"field4",name="crop").text=input_crop
ET.SubElement(doc,"field5",name="id cell").text=args.IDcell
ET.SubElement(doc,"field6",name="ET").text=args.ET
ET.SubElement(doc,"field7",name="rain").text=args.rainrandom
ET.SubElement(doc,"field8",name="vico").text=args.vico
ET.SubElement(doc,"field9",name="Tseas").text=str(Ndays)
ET.SubElement(doc,"field10",name="s_start").text=str(s_start)
ET.SubElement(doc,"field11",name="output").text=outputfile
tree=ET.ElementTree(root)
tree.write(outputfileproj)



### plots
opacity = 0.7
bar_width = 0.5
list_leg1=['SOIL MOISTURE']
list_leg2=['IRRIGATION']
list_leg3=['RAINFALL']
t=range(len(s))
fig=plt.figure()
ax = fig.add_subplot(111)
ax.plot(t, s, 'k')
ax.legend (list_leg1,loc='upper left' )
ax.set_xlabel('Days')
ax.set_ylabel('SOIL MOISTURE',color='k')
ax2 = ax.twinx()
#ax2.plot(t, I,'--r')
rects1 = ax2.bar(t, I, bar_width,
                 alpha=opacity,
                 color='c',
                 label='IRRIGATION')
ax2.hold(True)
#ax2.plot(t,R,'--g')
rects2 = ax2.bar(t, R, bar_width,
                 color='b',
                 label='RAINFALL')
ax2.set_ylabel('IRRIGATION - RAINFALL',color='blue')
ax2.legend( 'IRRIGATION',loc='upper right')



fig=plt.figure()
list_leg4=['ET_norm']
list_leg5=['STRESS']
ax = fig.add_subplot(111)
ax.plot(t, ET_norm, 'g')
ax.legend ( list_leg4,loc='upper left' )
ax.set_xlabel('Days')
ax.set_ylabel('ET norm',color='green')
ax2 = ax.twinx()
ax2.plot(t, stress,'--r')
ax2.set_ylabel('STRESS',color='red')
ax2.legend( list_leg5,loc='upper right')

plt.show()

