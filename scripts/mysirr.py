# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MY SIRR
       Minimalist agro-hYdrologicalmodel for Sustainable IRRigation management- soil moisture and crop dynamics
 MY SIRR
                              -------------------
        versione             : v.3.0
        author	             : Raffaele Albano
        contact              : http://www2.unibas.it/raffaelealbano/?page_id=115
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

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

#Global Variable

##1. Climate
##    - It stores: Rainfall, (i.e.observed values), parameters for evaluate rainfall with a stochastic approach, (i.e., lambda and alpha),
##  Evapotraspitration and parameters to estimate ET0 with Blaney-Criddle or Penman-Monteith equation.

col_clim_rain = 0
col_clim_T = 6
col_clim_rhmin = 2
col_clim_Ud = 3
col_clim_p = 4
col_clim_n_N = 5
col_clim_ET = 1
col_clim_delta = 7
col_clim_rn = 8
col_clim_u2 = 9
col_clim_es = 10
col_clim_ea = 11
col_clim_gamma = 12
col_clim_lambda = 13
col_clim_alpha = 14

####2. Soil
####    - soil parameters, n, s_fc, s*, s_w, in form of matrix (ID cell for differnt soil type)

col_soil_s_w = 0
col_soil_s_1 = 1
col_soil_s_c = 2
col_soil_n = 3

####3. crop

col_crop_Zr = 0
col_crop_Kc = 1
col_crop_Ymax = 2
col_crop_etseas50 = 3
col_crop_aopt = 4
col_crop_g_plus = 5
col_crop_a = 6
col_crop_b0 = 7
col_crop_s_xi = 8


####4. Management
####    - Irrigation application efficiency, time and amount


## id cell - select soil type


## use Blaney_Criddle 0=no 1=BC, 2 PM


#### random rain 0=mp 1=yes


### outputfile,  xls o csv


##  Yeld empirical (vico2011) or dichotomic (vico2013) formula


##  soil moisture start (initial condition)


def getInputAndPlot(idcell, input_clim, input_soil, input_crop, input_manage, rainrandom, use_bc, outputfile, vico, soilmoisture_start):

    ###### LOAD INPUT FILES

    ## climate
    if input_clim.find(".xls") > 0:
        book_clim = xlrd.open_workbook(input_clim)  # load climate
        sheet_clim = book_clim.sheet_by_index(0)  # Get the first sheet
        T_bc = sheet_clim.col_values(col_clim_T, start_rowx=1, end_rowx=None)
        p_bc = sheet_clim.col_values(col_clim_p, start_rowx=1, end_rowx=None)
        rhmin_bc = sheet_clim.col_values(col_clim_rhmin, start_rowx=1, end_rowx=None)
        n_N_bc = sheet_clim.col_values(col_clim_n_N, start_rowx=1, end_rowx=None)
        Ud_bc = sheet_clim.col_values(col_clim_Ud, start_rowx=1, end_rowx=None)
        delta = sheet_clim.col_values(col_clim_delta, start_rowx=1, end_rowx=None)
        rn = sheet_clim.col_values(col_clim_rn, start_rowx=1, end_rowx=None)
        u2 = sheet_clim.col_values(col_clim_u2, start_rowx=1, end_rowx=None)
        es = sheet_clim.col_values(col_clim_es, start_rowx=1, end_rowx=None)
        ea = sheet_clim.col_values(col_clim_ea, start_rowx=1, end_rowx=None)
        gamma = sheet_clim.cell_value(1, col_clim_gamma)
        alpha = sheet_clim.cell_value(1, col_clim_alpha)
        lamb = sheet_clim.cell_value(1, col_clim_lambda)
        if use_bc == 0:
            ET_max = sheet_clim.col_values(col_clim_ET, start_rowx=1, end_rowx=None)
        if rainrandom == 0:
            R = sheet_clim.col_values(col_clim_rain, start_rowx=1, end_rowx=None)  # rain

    if input_clim.find(".csv") > 0:
        with open(input_clim, 'rb') as csvfile:
            sheet_clim = csv.reader(csvfile, delimiter=',', quotechar='"')
            R = [];
            ET_max = []
            T_bc = []
            p_bc = []
            rhmin_bc = []
            n_N_bc = []
            Ud_bc = []
            ET_max = []
            delta = []
            rn = []
            u2 = []
            es = []
            ea = []

            for row in sheet_clim:
                if sheet_clim.line_num > 1:
                    T_bc.append(float(row[col_clim_T].replace(',', '.')))
                    p_bc.append(float(row[col_clim_p].replace(',', '.')))
                    rhmin_bc.append(float(row[col_clim_rhmin].replace(',', '.')))
                    n_N_bc.append(float(row[col_clim_n_N].replace(',', '.')))
                    Ud_bc.append(float(row[col_clim_Ud].replace(',', '.')))

                    delta.append(float(row[col_clim_delta].replace(',', '.')))
                    rn.append(float(row[col_clim_rn].replace(',', '.')))
                    u2.append(float(row[col_clim_u2].replace(',', '.')))
                    es.append(float(row[col_clim_es].replace(',', '.')))
                    ea.append(float(row[col_clim_ea].replace(',', '.')))
                    if sheet_clim.line_num == 2:
                        gamma = float(row[col_clim_gamma].replace(',', '.'))
                        alpha = float(row[col_clim_alpha].replace(',', '.'))
                        lamb = float(row[col_clim_lambda].replace(',', '.'))
                    if rainrandom == 0:
                        R.append(float(row[col_clim_rain].replace(',', '.')))
                    if use_bc == 0:
                        ET_max.append(float(row[col_clim_ET].replace(',', '.')))

    if use_bc == 1:
        ET_max = et_Blaney_Criddle(T_bc, p_bc, rhmin_bc, n_N_bc, Ud_bc)
        wb = xlwt.Workbook()
        ws = wb.add_sheet('sheet 1')
        for ctr in range(len(ET_max)):
            ws.write(ctr, 0, ET_max[ctr])
        wb.save('et_Blaney_Criddle.xls')

    if use_bc == 2:

        ET_max = et_PM(T_bc, delta, rn, u2, es, ea, gamma)
        wb = xlwt.Workbook()
        ws = wb.add_sheet('sheet 1')
        for ctr in range(len(ET_max)):
            ws.write(ctr, 0, ET_max[ctr])
        wb.save('et_PM.xls')

    if rainrandom > 0:
        Ndays = len(T_bc)
        R = [0] * Ndays
        for t in range(Ndays):
            r = np.random.rand(1)
            if r < lamb:
                e = np.random.exponential(alpha, 1)
                R[t] = e[0]
            if r >= lamb:
                R[t] = 0

    ## soil
    if input_soil.find(".xls") > 0:
        book_soil = xlrd.open_workbook(input_soil)  # load soil
        sheet_soil = book_soil.sheet_by_index(0)  # Get the first sheet
        p = Param()
        p.s_1 = sheet_soil.cell_value(idcell, col_soil_s_1)
        p.s_c = sheet_soil.cell_value(idcell, col_soil_s_c)
        p.s_w = sheet_soil.cell_value(idcell, col_soil_s_w)
        p.n = sheet_soil.cell_value(idcell, col_soil_n)

    if input_soil.find(".csv") > 0:
        p = Param()
        with open(input_soil, 'rb') as csvfile_soil:
            sheet_soil = csv.reader(csvfile_soil, delimiter=',', quotechar='"')
            for row in sheet_soil:
                if sheet_soil.line_num == idcell + 1:  # idcell= 0,1,..
                    p.s_1 = float(row[col_soil_s_1].replace(',', '.'))
                    p.s_c = float(row[col_soil_s_c].replace(',', '.'))
                    p.s_w = float(row[col_soil_s_w].replace(',', '.'))
                    p.n = float(row[col_soil_n].replace(',', '.'))

    ## crop
    if input_crop.find(".xls") > 0:
        book_crop = xlrd.open_workbook(input_crop)
        sheet_crop = book_crop.sheet_by_index(0)  # Get the first sheet
        Zr = sheet_crop.col_values(col_crop_Zr, start_rowx=1, end_rowx=None)
        Y_max = sheet_crop.cell_value(1, col_crop_Ymax)
        Et_seas_50 = sheet_crop.cell_value(1, col_crop_etseas50)
        a_opt = sheet_crop.cell_value(1, col_crop_aopt)
        p.g_plus = sheet_crop.cell_value(1, col_crop_g_plus)
        p.a = sheet_crop.cell_value(1, col_crop_a)
        p.b0 = sheet_crop.cell_value(1, col_crop_b0)
        # p.s_xi = sheet_crop.cell_value(1,col_crop_s_xi)

    if input_crop.find(".csv") > 0:
        with open(input_crop, 'rb') as csvfile:
            sheet_crop = csv.reader(csvfile, delimiter=',', quotechar='"')
            Zr = [];
            for row in sheet_crop:
                if sheet_crop.line_num > 1:
                    Zr.append(float(row[col_crop_Zr].replace(',', '.')))
                if sheet_crop.line_num == 2:
                    Y_max = float(row[col_crop_Ymax].replace(',', '.'))
                    Et_seas_50 = float(row[col_crop_etseas50].replace(',', '.'))
                    a_opt = float(row[col_crop_aopt].replace(',', '.'))

                    p.g_plus = float(row[col_crop_g_plus].replace(',', '.'))
                    p.a = float(row[col_crop_a].replace(',', '.'))
                    p.b0 = float(row[col_crop_b0].replace(',', '.'))
                    # p.s_xi=float(row[col_crop_s_xi].replace(',','.'))

    ## manage
    if input_manage.find(".xls") > 0:
        book_manage = xlrd.open_workbook(input_manage)
        sheet_manage = book_manage.sheet_by_index(0)  # Get the first sheet
        I = sheet_manage.col_values(0, start_rowx=1, end_rowx=None)
        CU = sheet_manage.cell_value(1, 1)

    if input_manage.find(".csv") > 0:
        with open(input_manage, 'rb') as csvfile:
            sheet_manage = csv.reader(csvfile, delimiter=',', quotechar='"')
            I = []

            for row in sheet_manage:
                if sheet_manage.line_num == 2:
                    CU = (float(row[1].replace(',', '.')))
                if sheet_manage.line_num > 1:
                    I.append(float(row[0].replace(',', '.')))



                    ######END LOAD INPUT FILES ##########

    ##s_start=p.s_c
    s_start = float(soilmoisture_start)
    p.s_xi=p.s_c
    Ndays = len(R)
    ICU = [0] * (Ndays)
    for t in range(Ndays):
        ICU[t] = I[t] * CU

    out = soil_moisture_simulation_R_ET_Z_I(p, Ndays, s_start, R, ET_max, Zr, ICU);
    outg = crop_development_simulation_R_ET_Z_I(p, Ndays, s_start, R, ET_max, Zr, ICU);

    s = out.s
    LQ_norm = out.LQ_norm
    stress = out.stress
    ET_norm = out.ET_norm

    v_irr = out.vol_irr
    cropdev = outg.b
    s.remove(s[len(s) - 1])
    stress.remove(stress[len(stress) - 1])
    ET_norm.remove(ET_norm[len(ET_norm) - 1])
    cropdev.remove(cropdev[len(cropdev) - 1])

    et = [0] * (Ndays)
    for t in range(Ndays):
        et[t] = ET_norm[t] * Zr[t] * p.n

    y_vico_2011 = Y_vico2011(sum(et), Y_max, Et_seas_50, a_opt)
    p1 = 0
    p2 = 0.8
    y_vico_2013 = p1 + p2 * outg.b[len(outg.b) - 1]
    if vico.find("EMP") >= 0:
        y = y_vico_2011

    if vico.find("DIC") >= 0:
        y = y_vico_2013

    if vico.find("EMP") < 0 and vico.find("DIC") < 0:
        print "WRONG VICO INPUT: EMP , DIC"
        sys.exit()
    v_irr_end = v_irr[len(v_irr) - 2]
    sumR = sum(R)

    # wp_vico_2011=WP(y_vico_2011,v_irr_end,sumR,0);
    wp = WP(y, v_irr_end, sumR, 0);

    WaterFootprint = 1 / wp
    effectivewater = sum(et) / (v_irr_end + sumR)

    print p.s_xi
    ### output file

    col_out_rain = 0;
    col_out_irr=1;
    col_out_s = 3;
    col_out_stress = 4;
    col_out_lq = 5;
    col_out_ew = 7;
    col_out_wf = 9;
    col_out_y = 8;
    col_out_et = 2;
    col_out_crop = 6;
   

    if outputfile.find(".xls") > 0:
        wb2 = xlwt.Workbook()
        ws2 = wb2.add_sheet('sheet 1')
        ws2.write(0, col_out_s, "Relative Soil moisture")
        ws2.write(0, col_out_stress, " Stress")
        ws2.write(0, col_out_lq, " Lqnorm")
        ws2.write(0, col_out_ew, " Effective user of water")
        ws2.write(0, col_out_wf, "  WP(Kg/m3)")
        ws2.write(0, col_out_y, " Yeld(tonn/ha)")
        ws2.write(0, col_out_et, " ETnorm")
        ws2.write(0, col_out_crop, " crop development")
        ws2.write(0, col_out_rain, " rain(mm)")
        ws2.write(0, col_out_irr, " Irrigation(mm)")
        for ctr in range(len(s)):
            ws2.write(ctr + 1, col_out_s, s[ctr])
        for ctr in range(len(stress)):
            ws2.write(ctr + 1, col_out_stress, stress[ctr])
        for ctr in range(len(Zr)):
            ws2.write(ctr + 1, col_out_lq, LQ_norm[ctr])
        for ctr in range(len(ET_norm)):
            ws2.write(ctr + 1, col_out_et, ET_norm[ctr])
        for ctr in range(len(cropdev)):
            ws2.write(ctr + 1, col_out_crop, cropdev[ctr])
        for ctr in range(len(R)):
            ws2.write(ctr + 1, col_out_rain, R[ctr])
        for ctr in range(len(R)):
            ws2.write(ctr + 1, col_out_irr, I[ctr])
        ws2.write(1, col_out_ew, effectivewater)
        ws2.write(1, col_out_wf, wp*100)
        ws2.write(1, col_out_y, y)
        wb2.save(outputfile)

    if outputfile.find(".csv") > 0:

        with open(outputfile, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(
                ['rain', 'Irrigation(mm)','ETnorm(mm)', 'Relative Soil moisture', 'Stress', 'Lqnorm', 'crop development', 'Effective user of water',
                 'Yeld(tonn/ha)', 'WP(Kg/m3)'])
            csvwriter.writerow(
                [R[0],I[0], ET_norm[0], s[0], stress[0], LQ_norm[0] * p.n * Zr[0], cropdev[0], effectivewater, y,
                 wp*100])
            for ctr in range(len(s) - 1):
                csvwriter.writerow(
                    [R[ctr + 1],I[ctr + 1], ET_norm[ctr + 1], s[ctr + 1], stress[ctr + 1], LQ_norm[ctr + 1],
                     cropdev[ctr + 1], 0, 0, 0])

    ## write project file
    outputfileproj = outputfile[0:len(outputfile) - 3] + 'xml'
    root = ET.Element("root")
    doc = ET.SubElement(root, "doc")
    if rainrandom==1:
        rain='Y'
    else:
        rain='N'
    if use_bc==0:
        et_type='N'
    if use_bc==1:
        et_type='BC'
    if use_bc==2:
        et_type='PM'
    ET.SubElement(doc, "field1", name="climate").text = input_clim
    ET.SubElement(doc, "field2", name="management").text = input_manage
    ET.SubElement(doc, "field3", name="soil").text = input_soil
    ET.SubElement(doc, "field4", name="crop").text = input_crop
    ET.SubElement(doc, "field5", name="id cell").text = str(idcell)
    ET.SubElement(doc, "field6", name="ET").text = et_type
    ET.SubElement(doc, "field7", name="rain").text = rain #str(rainrandom)
    ET.SubElement(doc, "field8", name="vico").text = str(vico)
    ET.SubElement(doc, "field9", name="Tseas").text = str(Ndays)
    ET.SubElement(doc, "field10", name="s_start").text = str(s_start)
    ET.SubElement(doc, "field11", name="output").text = outputfile
    ET.SubElement(doc, "field12", name="optimization").text = 'N'
    tree = ET.ElementTree(root)
    tree.write(outputfileproj)


    ### plots
    opacity = 0.7
    bar_width = 0.5
    list_leg1 = ['RELATIVE SOIL MOISTURE']
    list_leg2 = ['IRRIGATION']
    list_leg3 = ['RAINFALL']
    t = range(len(s))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(t, s, 'k')
    ax.legend(list_leg1, loc='upper left')
    ax.set_xlabel('Days')
    ax.set_ylabel('RELATIVE SOIL MOISTURE[-]', color='k')
    ax2 = ax.twinx()
    # ax2.plot(t, I,'--r')
    rects1 = ax2.bar(t, I, bar_width,
                     alpha=opacity,
                     color='c',
                     label='IRRIGATION')
    ax2.hold(True)
    # ax2.plot(t,R,'--g')
    rects2 = ax2.bar(t, R, bar_width,
                     color='b',
                     label='RAINFALL')
    ax2.set_ylabel('IRRIGATION - RAINFALL[mm]', color='blue')
    ax2.legend('IRRIGATION', loc='upper right')

    fig = plt.figure()
    list_leg4 = ['ET_norm']
    list_leg5 = ['STRESS']
    ax = fig.add_subplot(111)
    ax.plot(t, ET_norm, 'g')
    ax.legend(list_leg4, loc='upper left')
    ax.set_xlabel('Days')
    ax.set_ylabel('ET norm[-]', color='green')
    ax2 = ax.twinx()
    ax2.plot(t, stress, '--r')
    ax2.set_ylabel('STRESS[-]', color='red')
    ax2.legend(list_leg5, loc='upper right')

    plt.show()


###### optimization 
def frange(start,stop,step):
    i=start
    while i < stop:
        yield i
        i+=step

#def getInputAndPlotOptimizer(idcell, input_clim, input_soil, input_crop, input_manage, rainrandom, use_bc, outputfile, vico, soilmoisture_start,s_tilde_min,s_tilde_max,s_target_max, mindist, s_step ):
def getInputAndPlotOptimizer(idcell, input_clim, input_soil, input_crop, input_manage, rainrandom, use_bc, outputfile, vico, soilmoisture_start, mindist, s_step ):
    print vico
    ###### LOAD INPUT FILES

    ## climate
    if input_clim.find(".xls") > 0:
        book_clim = xlrd.open_workbook(input_clim)  # load climate
        sheet_clim = book_clim.sheet_by_index(0)  # Get the first sheet
        T_bc = sheet_clim.col_values(col_clim_T, start_rowx=1, end_rowx=None)
        p_bc = sheet_clim.col_values(col_clim_p, start_rowx=1, end_rowx=None)
        rhmin_bc = sheet_clim.col_values(col_clim_rhmin, start_rowx=1, end_rowx=None)
        n_N_bc = sheet_clim.col_values(col_clim_n_N, start_rowx=1, end_rowx=None)
        Ud_bc = sheet_clim.col_values(col_clim_Ud, start_rowx=1, end_rowx=None)
        delta = sheet_clim.col_values(col_clim_delta, start_rowx=1, end_rowx=None)
        rn = sheet_clim.col_values(col_clim_rn, start_rowx=1, end_rowx=None)
        u2 = sheet_clim.col_values(col_clim_u2, start_rowx=1, end_rowx=None)
        es = sheet_clim.col_values(col_clim_es, start_rowx=1, end_rowx=None)
        ea = sheet_clim.col_values(col_clim_ea, start_rowx=1, end_rowx=None)
        gamma = sheet_clim.cell_value(1, col_clim_gamma)
        alpha = sheet_clim.cell_value(1, col_clim_alpha)
        lamb = sheet_clim.cell_value(1, col_clim_lambda)
        if use_bc == 0:
            ET_max = sheet_clim.col_values(col_clim_ET, start_rowx=1, end_rowx=None)
        if rainrandom == 0:
            R = sheet_clim.col_values(col_clim_rain, start_rowx=1, end_rowx=None)  # rain

    if input_clim.find(".csv") > 0:
        with open(input_clim, 'rb') as csvfile:
            sheet_clim = csv.reader(csvfile, delimiter=',', quotechar='"')
            R = [];
            ET_max = []
            T_bc = []
            p_bc = []
            rhmin_bc = []
            n_N_bc = []
            Ud_bc = []
            ET_max = []
            delta = []
            rn = []
            u2 = []
            es = []
            ea = []

            for row in sheet_clim:
                if sheet_clim.line_num > 1:
                    T_bc.append(float(row[col_clim_T].replace(',', '.')))
                    p_bc.append(float(row[col_clim_p].replace(',', '.')))
                    rhmin_bc.append(float(row[col_clim_rhmin].replace(',', '.')))
                    n_N_bc.append(float(row[col_clim_n_N].replace(',', '.')))
                    Ud_bc.append(float(row[col_clim_Ud].replace(',', '.')))

                    delta.append(float(row[col_clim_delta].replace(',', '.')))
                    rn.append(float(row[col_clim_rn].replace(',', '.')))
                    u2.append(float(row[col_clim_u2].replace(',', '.')))
                    es.append(float(row[col_clim_es].replace(',', '.')))
                    ea.append(float(row[col_clim_ea].replace(',', '.')))
                    if sheet_clim.line_num == 2:
                        gamma = float(row[col_clim_gamma].replace(',', '.'))
                        alpha = float(row[col_clim_alpha].replace(',', '.'))
                        lamb = float(row[col_clim_lambda].replace(',', '.'))
                    if rainrandom == 0:
                        R.append(float(row[col_clim_rain].replace(',', '.')))
                    if use_bc == 0:
                        ET_max.append(float(row[col_clim_ET].replace(',', '.')))

    if use_bc == 1:
        ET_max = et_Blaney_Criddle(T_bc, p_bc, rhmin_bc, n_N_bc, Ud_bc)
        wb = xlwt.Workbook()
        ws = wb.add_sheet('sheet 1')
        for ctr in range(len(ET_max)):
            ws.write(ctr, 0, ET_max[ctr])
        wb.save('et_Blaney_Criddle.xls')

    if use_bc == 2:

        ET_max = et_PM(T_bc, delta, rn, u2, es, ea, gamma)
        wb = xlwt.Workbook()
        ws = wb.add_sheet('sheet 1')
        for ctr in range(len(ET_max)):
            ws.write(ctr, 0, ET_max[ctr])
        wb.save('et_PM.xls')

    if rainrandom > 0:
        Ndays = len(T_bc)
        R = [0] * Ndays
        for t in range(Ndays):
            r = np.random.rand(1)
            if r < lamb:
                e = np.random.exponential(alpha, 1)
                R[t] = e[0]
            if r >= lamb:
                R[t] = 0

    ## soil
    if input_soil.find(".xls") > 0:
        book_soil = xlrd.open_workbook(input_soil)  # load soil
        sheet_soil = book_soil.sheet_by_index(0)  # Get the first sheet
        p = Param()
        p.s_1 = sheet_soil.cell_value(idcell, col_soil_s_1)
        p.s_c = sheet_soil.cell_value(idcell, col_soil_s_c)
        p.s_w = sheet_soil.cell_value(idcell, col_soil_s_w)
        p.n = sheet_soil.cell_value(idcell, col_soil_n)

    if input_soil.find(".csv") > 0:
        p = Param()
        with open(input_soil, 'rb') as csvfile_soil:
            sheet_soil = csv.reader(csvfile_soil, delimiter=',', quotechar='"')
            for row in sheet_soil:
                if sheet_soil.line_num == idcell + 1:  # idcell= 0,1,..
                    p.s_1 = float(row[col_soil_s_1].replace(',', '.'))
                    p.s_c = float(row[col_soil_s_c].replace(',', '.'))
                    p.s_w = float(row[col_soil_s_w].replace(',', '.'))
                    p.n = float(row[col_soil_n].replace(',', '.'))

    ## crop
    if input_crop.find(".xls") > 0:
        book_crop = xlrd.open_workbook(input_crop)
        sheet_crop = book_crop.sheet_by_index(0)  # Get the first sheet
        Zr = sheet_crop.col_values(col_crop_Zr, start_rowx=1, end_rowx=None)
        Y_max = sheet_crop.cell_value(1, col_crop_Ymax)
        Et_seas_50 = sheet_crop.cell_value(1, col_crop_etseas50)
        a_opt = sheet_crop.cell_value(1, col_crop_aopt)
        p.g_plus = sheet_crop.cell_value(1, col_crop_g_plus)
        p.a = sheet_crop.cell_value(1, col_crop_a)
        p.b0 = sheet_crop.cell_value(1, col_crop_b0)
        # p.s_xi = sheet_crop.cell_value(1,col_crop_s_xi)

    if input_crop.find(".csv") > 0:
        with open(input_crop, 'rb') as csvfile:
            sheet_crop = csv.reader(csvfile, delimiter=',', quotechar='"')
            Zr = [];
            for row in sheet_crop:
                if sheet_crop.line_num > 1:
                    Zr.append(float(row[col_crop_Zr].replace(',', '.')))
                if sheet_crop.line_num == 2:
                    Y_max = float(row[col_crop_Ymax].replace(',', '.'))
                    Et_seas_50 = float(row[col_crop_etseas50].replace(',', '.'))
                    a_opt = float(row[col_crop_aopt].replace(',', '.'))

                    p.g_plus = float(row[col_crop_g_plus].replace(',', '.'))
                    p.a = float(row[col_crop_a].replace(',', '.'))
                    p.b0 = float(row[col_crop_b0].replace(',', '.'))
                    # p.s_xi=float(row[col_crop_s_xi].replace(',','.'))

    ## manage
    if input_manage.find(".xls") > 0:
        book_manage = xlrd.open_workbook(input_manage)
        sheet_manage = book_manage.sheet_by_index(0)  # Get the first sheet
        I = sheet_manage.col_values(0, start_rowx=1, end_rowx=None)
        CU = sheet_manage.cell_value(1, 1)
        s_tilde_min=sheet_manage.cell_value(1, 2)
        s_target_max=sheet_manage.cell_value(1, 3)

    if input_manage.find(".csv") > 0:
        with open(input_manage, 'rb') as csvfile:
            sheet_manage = csv.reader(csvfile, delimiter=',', quotechar='"')
            I = []

            for row in sheet_manage:
                if sheet_manage.line_num == 2:
                    CU = (float(row[1].replace(',', '.')))
                    s_tilde_min=(float(row[2].replace(',', '.')))
                    s_target_max=(float(row[3].replace(',', '.')))
                if sheet_manage.line_num > 1:
                    I.append(float(row[0].replace(',', '.')))



                    ######END LOAD INPUT FILES ##########

    ##s_start=p.s_c
    s_start = float(soilmoisture_start)
    Ndays = len(R)
    ICU = [0] * (Ndays)
    for t in range(Ndays):
        ICU[t] = I[t] * CU


   ### FIND OPTIMAL S_TILDE S_TARGET #####

    param1=[]
    param2=[]
    obj=[]
    
    if s_tilde_min+mindist>s_target_max:
        mindist=(s_target_max-s_tilde_min)/5
    s_tilde_max=s_target_max-2*mindist;
    p.s_xi=p.s_c
    for s_tilde in frange(s_tilde_min,s_tilde_max,s_step):
        for s_target in frange(s_tilde+mindist,s_target_max,s_step):
            param1.append(s_tilde)
            param2.append(s_target)
            p.s_tilde=s_tilde
            p.s_target=s_target
            out = soil_moisture_simulation_R_ET_Z_v2(p, Ndays, s_start, R, ET_max, Zr);
            outg = crop_development_simulation_R_ET_Z_v2(p, Ndays, s_start, R, ET_max, Zr);
            I=out.I
            s = out.s
            LQ_norm = out.LQ_norm
            stress = out.stress
            ET_norm = out.ET_norm

            v_irr = out.vol_irr
            cropdev = outg.b
            s.remove(s[len(s) - 1])
            stress.remove(stress[len(stress) - 1])
            ET_norm.remove(ET_norm[len(ET_norm) - 1])
            cropdev.remove(cropdev[len(cropdev) - 1])
            I.remove(I[len(I) - 1])
            et = [0] * (Ndays)
            for t in range(Ndays):
                et[t] = ET_norm[t] * Zr[t] * p.n

            y_vico_2011 = Y_vico2011(sum(et), Y_max, Et_seas_50, a_opt)
            p1 = 0
            p2 = 0.8
            y_vico_2013 = p1 + p2 * outg.b[len(outg.b) - 1]
            if vico.find("EMP") >= 0:
                y = y_vico_2011

            if vico.find("DIC") >= 0:
                y = y_vico_2013

            if vico.find("EMP") < 0 and vico.find("DIC") < 0:
                print "WRONG VICO INPUT: EMP , DIC"
                sys.exit()
            v_irr_end = v_irr[len(v_irr) - 2]
            sumR = sum(R)

            # wp_vico_2011=WP(y_vico_2011,v_irr_end,sumR,0);
            wp = WP(y, v_irr_end, sumR, 0);
            obj.append(wp)


    obj=np.array(obj)
    id_opt=obj.argmax()
   #######################################
    p.s_tilde=param1[id_opt]
    p.s_target=param2[id_opt]
    param_opt=[ p.s_tilde,p.s_target]
    print p.s_tilde
    print p.s_target
    out = soil_moisture_simulation_R_ET_Z_v2(p, Ndays, s_start, R, ET_max, Zr);
    outg = crop_development_simulation_R_ET_Z_v2(p, Ndays, s_start, R, ET_max, Zr);
    I=out.I
    s = out.s
    LQ_norm = out.LQ_norm
    stress = out.stress
    ET_norm = out.ET_norm

    v_irr = out.vol_irr
    cropdev = outg.b
    s.remove(s[len(s) - 1])
    stress.remove(stress[len(stress) - 1])
    ET_norm.remove(ET_norm[len(ET_norm) - 1])
    cropdev.remove(cropdev[len(cropdev) - 1])
    I.remove(I[len(I) - 1])
    et = [0] * (Ndays)
    for t in range(Ndays):
        et[t] = ET_norm[t] * Zr[t] * p.n

    y_vico_2011 = Y_vico2011(sum(et), Y_max, Et_seas_50, a_opt)
    p1 = 0
    p2 = 0.8
    y_vico_2013 = p1 + p2 * outg.b[len(outg.b) - 1]
    if vico.find("EMP") >= 0:
        y = y_vico_2011

    if vico.find("DIC") >= 0:
        y = y_vico_2013

    if vico.find("EMP") < 0 and vico.find("DIC") < 0:
        print "WRONG VICO INPUT: EMP , DIC"
        sys.exit()
    v_irr_end = v_irr[len(v_irr) - 2]
    sumR = sum(R)

    # wp_vico_2011=WP(y_vico_2011,v_irr_end,sumR,0);
    wp = WP(y, v_irr_end, sumR, 0);

    WaterFootprint = 1 / wp
    effectivewater = sum(et) / (v_irr_end + sumR)

    print p.s_xi
    ### output file

    col_out_rain = 0;
    col_out_irr=1;
    col_out_s = 3;
    col_out_stress = 4;
    col_out_lq = 5;
    col_out_ew = 7;
    col_out_wf = 9;
    col_out_y = 8;
    col_out_et = 2;
    col_out_crop = 6;
   

    if outputfile.find(".xls") > 0:
        wb2 = xlwt.Workbook()
        ws2 = wb2.add_sheet('sheet 1')
        ws2.write(0, col_out_s, "Relative Soil moisture")
        ws2.write(0, col_out_stress, " Stress")
        ws2.write(0, col_out_lq, " Lqnorm")
        ws2.write(0, col_out_ew, " Effective user of water")
        ws2.write(0, col_out_wf, "  WP(Kg/m3)")
        ws2.write(0, col_out_y, " Yeld(tonn/ha)")
        ws2.write(0, col_out_et, " ETnorm")
        ws2.write(0, col_out_crop, " crop development")
        ws2.write(0, col_out_rain, " rain[mm]")
        ws2.write(0, col_out_irr, " Irrigation[mm]")
        for ctr in range(len(s)):
            ws2.write(ctr + 1, col_out_s, s[ctr])
        for ctr in range(len(stress)):
            ws2.write(ctr + 1, col_out_stress, stress[ctr])
        for ctr in range(len(Zr)):
            ws2.write(ctr + 1, col_out_lq, LQ_norm[ctr])
        for ctr in range(len(ET_norm)):
            ws2.write(ctr + 1, col_out_et, ET_norm[ctr])
        for ctr in range(len(cropdev)):
            ws2.write(ctr + 1, col_out_crop, cropdev[ctr])
        for ctr in range(len(R)):
            ws2.write(ctr + 1, col_out_rain, R[ctr])
        for ctr in range(len(R)):
            ws2.write(ctr + 1, col_out_irr, I[ctr])
        ws2.write(1, col_out_ew, effectivewater)
        ws2.write(1, col_out_wf, wp*100)
        ws2.write(1, col_out_y, y)
        wb2.save(outputfile)

    if outputfile.find(".csv") > 0:

        with open(outputfile, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(
                ['rain (mm)', 'Irrigation (mm)','ETnorm', 'Relative Soil moisture', 'Stress', 'Lqnorm', 'crop development', 'Effective user of water',
                 'Yeld(tonn/ha)', 'WP(Kg/m3)'])
            csvwriter.writerow(
                [R[0],I[0], ET_norm[0], s[0], stress[0], LQ_norm[0] * p.n * Zr[0], cropdev[0], effectivewater, y,
                 wp*100])
            for ctr in range(len(s) - 1):
                csvwriter.writerow(
                    [R[ctr + 1],I[ctr + 1], ET_norm[ctr + 1], s[ctr + 1], stress[ctr + 1], LQ_norm[ctr + 1],
                     cropdev[ctr + 1], 0, 0, 0])

    ## write project file
    outputfileproj = outputfile[0:len(outputfile) - 3] + 'xml'
    root = ET.Element("root")
    doc = ET.SubElement(root, "doc")
    if rainrandom==1:
        rain='Y'
    else:
        rain='N'

    if use_bc==0:
        et_type='N'
    if use_bc==1:
        et_type='BC'
    if use_bc==2:
        et_type='PM'

    ET.SubElement(doc, "field1", name="climate").text = input_clim
    ET.SubElement(doc, "field2", name="management").text = input_manage
    ET.SubElement(doc, "field3", name="soil").text = input_soil
    ET.SubElement(doc, "field4", name="crop").text = input_crop
    ET.SubElement(doc, "field5", name="id cell").text = str(idcell)
    ET.SubElement(doc, "field6", name="ET").text = et_type
    ET.SubElement(doc, "field7", name="rain").text =rain # str(rainrandom)
    ET.SubElement(doc, "field8", name="vico").text = str(vico)
    ET.SubElement(doc, "field9", name="Tseas").text = str(Ndays)
    ET.SubElement(doc, "field10", name="s_start").text = str(s_start)
    ET.SubElement(doc, "field11", name="output").text = outputfile
    ET.SubElement(doc, "field12", name="optimization").text = 'Y'
    tree = ET.ElementTree(root)
    tree.write(outputfileproj)

    ### plots
    opacity = 0.7
    bar_width = 0.5
    list_leg1 = ['RELATIVE SOIL MOISTURE']
    list_leg2 = ['IRRIGATION']
    list_leg3 = ['RAINFALL']
    t = range(len(s))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(t, s, 'k')
    ax.legend(list_leg1, loc='upper left')
    ax.set_xlabel('Days')
    ax.set_ylabel('RELATIVE SOIL MOISTURE[-]', color='k')
    ax2 = ax.twinx()
    # ax2.plot(t, I,'--r')
    rects1 = ax2.bar(t, I, bar_width,
                     alpha=opacity,
                     color='c',
                     label='IRRIGATION')
    ax2.hold(True)
    # ax2.plot(t,R,'--g')
    rects2 = ax2.bar(t, R, bar_width,
                     color='b',
                     label='RAINFALL')
    ax2.set_ylabel('IRRIGATION - RAINFALL [mm]', color='blue')
    ax2.legend('IRRIGATION', loc='upper right')

    fig = plt.figure()
    list_leg4 = ['ET_norm']
    list_leg5 = ['STRESS']
    ax = fig.add_subplot(111)
    ax.plot(t, ET_norm, 'g')
    ax.legend(list_leg4, loc='upper left')
    ax.set_xlabel('Days')
    ax.set_ylabel('ET norm[-]', color='green')
    ax2 = ax.twinx()
    ax2.plot(t, stress, '--r')
    ax2.set_ylabel('STRESS[-]', color='red')
    ax2.legend(list_leg5, loc='upper right')

    plt.show()
    return param_opt




def inputWrapper(args):
    idcell1 = int(args.IDcell)
    input_clim1 = args.Climate
    input_soil1 = args.Soil
    input_crop1 = args.Crop
    input_manage1 = args.Management

    rainrandom1 = 0
    if args.rainrandom.find("N") >= 0:
        rainrandom1 = 0
    if args.rainrandom.find("Y") >= 0:
        rainrandom1 = 1
    if args.rainrandom.find("N") < 0 and args.rainrandom.find("Y") < 0:
        print "wrong rain input: N,Y"
        sys.exit()

    use_bc1 = 0
    if args.ET.find("N") >= 0:
        print " loading ET "
        use_bc1 = 0
    if args.ET.find("BC") >= 0:
        print "BC "
        use_bc1 = 1
    if args.ET.find("PM") >= 0:
        print("PM")
        use_bc1 = 2
    if args.ET.find("N") < 0 and args.ET.find("BC") < 0 and args.ET.find("PM") < 0:
        print "wrong ET input : NO,BC,PM"
        sys.exit()

    outputfile1 = args.outputfile
    vico1 = args.vico

    soilmoisture_start1 = args.soilmoisture_start

    getInputAndPlot(idcell1, input_clim1, input_soil1, input_crop1, input_manage1, rainrandom1, use_bc1, outputfile1,
                    vico1, soilmoisture_start1)






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=' soil omisture simulation')
    parser.add_argument('Climate')
    parser.add_argument('Soil')
    parser.add_argument('Crop')
    parser.add_argument('Management')
    parser.add_argument('IDcell')
    parser.add_argument('ET')
    parser.add_argument('rainrandom')
    parser.add_argument('outputfile')
    parser.add_argument('vico')
    parser.add_argument('soilmoisture_start')

    ## input file and method for their evaluation
    args = parser.parse_args()
    inputWrapper(args)



