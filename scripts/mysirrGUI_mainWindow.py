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

import imp
try:
    imp.find_module('xml')
except ImportError:
    print(' ERROR IMPORTING LIBRARY   xml')
try:
    imp.find_module('PySide')
except ImportError:
    print(' ERROR IMPORTING LIBRARY   PySide')

import sys
import os
import xml.etree.cElementTree as ET
from PySide.QtGui import *
from PySide.QtCore import *
from ui_mainWindow import Ui_mainWindow
from mysirr import getInputAndPlot
from mysirr import getInputAndPlotOptimizer
class MainWindow(QMainWindow, Ui_mainWindow):
    MaxRecentFiles = 5
    project_name='';
    def __init__(self):
        super(MainWindow, self).__init__()
        self.recentFileActs = []
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.assignWidgets()
        self.initfield()
        self.createActions()
        self.createMenus()
        self.show()
    
    def initfield(self):
        self.textEditOutput.append("out.xls")

    def assignWidgets(self):
        self.goButton.clicked.connect(self.goPushed)
        self.toolButtonClimate.clicked.connect(self.ClimatePushed)
        self.toolButtonSoil.clicked.connect(self.SoilPushed)
        self.toolButtonCrop.clicked.connect(self.CropPushed)
        self.toolButtonMan.clicked.connect(self.ManPushed)
        self.toolButtonOutput.clicked.connect(self.OutputPushed)
        QObject.connect(self.actionOpen_Project, SIGNAL("triggered()"), self.open)
        QObject.connect(self.actionSave_As, SIGNAL("triggered()"), self.saveas)
        QObject.connect(self.actionSave, SIGNAL("triggered()"), self.save)
    def loadprojectfile(self, projfile):
        if os.path.isfile(projfile):
            tree=ET.parse(projfile)
            root=tree.getroot()
            for child in root[0]:
                a=child.attrib;
                t=child.text
                name=a['name']
                if name.find("climate")>=0:
                    climate=t;
     
                if name.find("soil")>=0:
                    soil=t
               
                if name.find("crop")>=0:
                    crop=t
               
                if name.find("management")>=0:
                    management=t
               
                if name.find("id")>=0:
                    idcell=t
                
                if name.find("ET")>=0:
                    et=t
              
                if name.find("rain")>=0:
                    rain=t
                
                if name.find("vico")>=0:
                    vico=t
                
                if name.find("s_start")>=0:
                    s_start=t

                if name.find("optimization")>=0:
                    optimization=t
                    
             #update gui 
            self.textEditClimate.setPlainText(climate)
            self.textEditCrop.setPlainText(crop)
            self.textEditMan.setPlainText(management)
            self.textEditSoil.setPlainText(soil)
            if vico=='EMP':
                id_vico=0
            else:
                id_vico=1
            if rain=='Y':
                check_rain=True
            else:
                check_rain=False

            if optimization=='Y':
                check_optimization=True
            else:
                check_optimization=False

            if et=='N':
                id_et=0
            if et=='BC':
                id_et=1
            if et=='PM':
                id_et=2
            self.comboBoxVico.setCurrentIndex(id_vico)
            self.comboBoxET.setCurrentIndex(id_et)
            self.checkBoxRain.setChecked(check_rain)
            self.checkBoxOptimization.setChecked(check_optimization)
            self.spinBoxCell.setValue(int(idcell))
            self.doubleSpinBoxSstart.setValue(float(s_start))

            self.setCurrentFile(projfile)
            self.project_name=projfile
    def goPushed(self):
        self.fileClimate=self.textEditClimate.toPlainText()
        self.fileCrop=self.textEditCrop.toPlainText()
        self.fileSoil=self.textEditSoil.toPlainText()
        self.fileMan=self.textEditMan.toPlainText()
        self.fileout= self.textEditOutput.toPlainText()
        self.et=self.comboBoxET.currentText()
        self.vico=self.comboBoxVico.currentText()
        self.rain=self.checkBoxRain.isChecked()
        self.s_start=self.doubleSpinBoxSstart.value()
        self.cellid=self.spinBoxCell.value()
        self.inputerror=False
        self.optimization=self.checkBoxOptimization.isChecked()
        #check files
        if os.path.isfile(self.fileClimate)==False:
            self.goText.append("ERROR: file Climate doesn't exist ")
            self.inputerror=True
        if os.path.isfile(self.fileCrop)==False:
            self.goText.append("ERROR: file Crop doesn't exist ")
            self.inputerror=True
        if os.path.isfile(self.fileMan)==False:
            self.goText.append("ERROR: file Management doesn't exist ")
            self.inputerror=True
        if os.path.isfile(self.fileSoil)==False:
            self.goText.append("ERROR: file Soil doesn't exist ")
            self.inputerror=True
        sfile=self.fileout
        fxls=sfile.find(".xls")
        fcsv=sfile.find(".csv")
        if fxls<0 and fcsv<0:
            self.goText.append("ERROR: file output .xls or .csv  ")
            self.inputerror=True
            
        if self.inputerror==True:
             p=QMessageBox(self)
             p.setText("WARNING : SET INPUT FILES")
             p.show()
        if self.inputerror==False:
             self.goText.append("simulation started")
             if self.rain==True:
                 rain='Y'
             else:
                 rain='N'
             """command='python mysirr.py'
             command=command+' '+ self.fileClimate +' '+self.fileSoil+' '+self.fileCrop+' '+self.fileMan+' '+str(self.cellid)+' '+self.et+' '+rain+' '+self.fileout+' '+self.vico+' '+str(self.s_start)
             self.goText.append(command)
             os.system(command)"""

             rainrandom = 0
             if rain.find("N") >= 0:
                 rainrandom = 0
             if rain.find("Y") >= 0:
                 rainrandom = 1

             use_bc = 0
             if self.et.find("N") >= 0:
                 use_bc = 0
             if self.et.find("BC") >= 0:
                 use_bc = 1
             if self.et.find("PM") >= 0:
                 use_bc = 2

             #def getInputAndPlot(idcell, input_clim, input_soil, input_crop, input_manage, rainrandom, use_bc, outputfile, vico, soilmoisture_start)
             if self.optimization==False:
                getInputAndPlot(self.cellid, self.fileClimate, self.fileSoil, self.fileCrop, self.fileMan, rainrandom, use_bc, self.fileout, self.vico, self.s_start)
             else:

                 #s_tilde_min=0
                 #s_tilde_max=0.9
                 #s_target_max=1
                 mindist=0.01
                 s_step=0.01
                 self.goText.append("optimization started")
                 #param_opt=getInputAndPlotOptimizer(self.cellid, self.fileClimate, self.fileSoil, self.fileCrop, self.fileMan, rainrandom, use_bc, self.fileout, self.vico, self.s_start,s_tilde_min,s_tilde_max,s_target_max, mindist, s_step)
                 param_opt=getInputAndPlotOptimizer(self.cellid, self.fileClimate, self.fileSoil, self.fileCrop, self.fileMan, rainrandom, use_bc, self.fileout, self.vico, self.s_start, mindist, s_step)
                 self.goText.append("optimization completed")
                 self.goText.append("s tilde: "+str(param_opt[0])+ " s target: "+str(param_opt[1]))
    def ClimatePushed(self):
        filename=QFileDialog.getOpenFileName(self)
        if len(filename[0])>0:
                self.textEditClimate.setPlainText(filename[0])
    def SoilPushed(self):
        filename=QFileDialog.getOpenFileName(self)
        if len(filename[0])>0:
                self.textEditSoil.setPlainText(filename[0])
    def CropPushed(self):
        filename=QFileDialog.getOpenFileName(self)
        if len(filename[0])>0:
             self.textEditCrop.setPlainText(filename[0])
    def ManPushed(self):
        filename=QFileDialog.getOpenFileName(self)
        if len(filename[0])>0:
             self.textEditMan.setPlainText(filename[0])
    def OutputPushed(self):
        filename=QFileDialog.getSaveFileName(self)
        if len(filename[0])>0:
             self.textEditOutput.setPlainText(filename[0])
    def open(self):
         filename=QFileDialog.getOpenFileName(self)
         if len(filename[0])>0:
            #self.textEditOutput.setPlainText(filename[0])
            self.loadprojectfile(filename[0])
    def save(self):
        self.fileClimate=self.textEditClimate.toPlainText()
        self.fileCrop=self.textEditCrop.toPlainText()
        self.fileSoil=self.textEditSoil.toPlainText()
        self.fileMan=self.textEditMan.toPlainText()
        self.fileout= self.textEditOutput.toPlainText()
        self.et=self.comboBoxET.currentText()
        self.vico=self.comboBoxVico.currentText()
        self.rain=self.checkBoxRain.isChecked()
        self.optimization=self.checkBoxOptimization.isChecked()
        self.s_start=self.doubleSpinBoxSstart.value()
        self.cellid=self.spinBoxCell.value()
        self.inputerror=False
        #check files
        if os.path.isfile(self.fileClimate)==False:
            self.goText.append("ERROR: file Climate doesn't exist ")
            self.inputerror=True
        if os.path.isfile(self.fileCrop)==False:
            self.goText.append("ERROR: file Crop doesn't exist ")
            self.inputerror=True
        if os.path.isfile(self.fileMan)==False:
            self.goText.append("ERROR: file Management doesn't exist ")
            self.inputerror=True
        if os.path.isfile(self.fileSoil)==False:
            self.goText.append("ERROR: file Soil doesn't exist ")
            self.inputerror=True

        if self.inputerror==False:
             if self.rain==True:
                 rain='Y'
             else:
                 rain='N'
             if self.optimization==True:
                 optim='Y'
             else:
                 optim='N'
                ## write project file
        if len(self.project_name)>0:
            outputfileproj=self.project_name;               
            root=ET.Element("root")
            doc=ET.SubElement(root,"doc")
            ET.SubElement(doc,"field1",name="climate").text=self.fileClimate
            ET.SubElement(doc,"field2",name="management").text=self.fileMan
            ET.SubElement(doc,"field3",name="soil").text=self.fileSoil
            ET.SubElement(doc,"field4",name="crop").text=self.fileCrop
            ET.SubElement(doc,"field5",name="id cell").text=str(self.cellid)
            ET.SubElement(doc,"field6",name="ET").text=self.et
            ET.SubElement(doc,"field7",name="rain").text=rain
            ET.SubElement(doc,"field8",name="vico").text=self.vico
            ET.SubElement(doc,"field9",name="Tseas").text=str(0)
            ET.SubElement(doc,"field10",name="s_start").text=str(self.s_start)
            ET.SubElement(doc,"field11",name="output").text=self.fileout
            ET.SubElement(doc,"field12", name="optimization").text = optim
            tree=ET.ElementTree(root)
            tree.write(outputfileproj)
            self.setCurrentFile(outputfileproj)
       
    def saveas(self):

        self.fileClimate=self.textEditClimate.toPlainText()
        self.fileCrop=self.textEditCrop.toPlainText()
        self.fileSoil=self.textEditSoil.toPlainText()
        self.fileMan=self.textEditMan.toPlainText()
        self.fileout= self.textEditOutput.toPlainText()
        self.et=self.comboBoxET.currentText()
        self.vico=self.comboBoxVico.currentText()
        self.rain=self.checkBoxRain.isChecked()
        self.optimization=self.checkBoxOptimization.isChecked()
        self.s_start=self.doubleSpinBoxSstart.value()
        self.cellid=self.spinBoxCell.value()
        self.inputerror=False
        #check files
        if os.path.isfile(self.fileClimate)==False:
            self.goText.append("ERROR: file Climate doesn't exist ")
            self.inputerror=True
        if os.path.isfile(self.fileCrop)==False:
            self.goText.append("ERROR: file Crop doesn't exist ")
            self.inputerror=True
        if os.path.isfile(self.fileMan)==False:
            self.goText.append("ERROR: file Management doesn't exist ")
            self.inputerror=True
        if os.path.isfile(self.fileSoil)==False:
            self.goText.append("ERROR: file Soil doesn't exist ")
            self.inputerror=True

        if self.inputerror==False:
             if self.rain==True:
                 rain='Y'
             else:
                 rain='N'
             if self.optimization==True:
                 optim='Y'
             else:
                 optim='N'
             filename=QFileDialog.getSaveFileName(self)
             if len(filename[0])>0:
                 ## write project file
                outputfileproj=filename[0]                
                root=ET.Element("root")
                doc=ET.SubElement(root,"doc")
                ET.SubElement(doc,"field1",name="climate").text=self.fileClimate
                ET.SubElement(doc,"field2",name="management").text=self.fileMan
                ET.SubElement(doc,"field3",name="soil").text=self.fileSoil
                ET.SubElement(doc,"field4",name="crop").text=self.fileCrop
                ET.SubElement(doc,"field5",name="id cell").text=str(self.cellid)
                ET.SubElement(doc,"field6",name="ET").text=self.et
                ET.SubElement(doc,"field7",name="rain").text=rain
                ET.SubElement(doc,"field8",name="vico").text=self.vico
                ET.SubElement(doc,"field9",name="Tseas").text=str(0)
                ET.SubElement(doc,"field10",name="s_start").text=str(self.s_start)
                ET.SubElement(doc,"field11",name="output").text=self.fileout
                ET.SubElement(doc,"field12", name="optimization").text = optim
                tree=ET.ElementTree(root)
                tree.write(outputfileproj)
                self.setCurrentFile(outputfileproj)
                self.project_name=outputfileproj;

    def createActions(self):
            

            for i in range(MainWindow.MaxRecentFiles):
                self.recentFileActs.append(
                        QAction(self, visible=False,
                                triggered=self.openRecentFile))
    def openRecentFile(self):
        action = self.sender()
        if action:
            self.loadprojectfile(action.data())

    def createMenus(self):
        
        self.separatorAct = self.menuFile.addSeparator()
        for i in range(MainWindow.MaxRecentFiles):
            self.action_RecentProject.addAction(self.recentFileActs[i])
            #self.menuFile.addAction(self.recentFileActs[i])
        self.menuFile.addSeparator()
       
        self.updateRecentFileActions()
    
    def updateRecentFileActions(self):
        settings = QSettings('mysirrGUI', 'Recent Files')
        files = settings.value('recentFileList')

        files_no = 0
        if files:
            files_no = len(files)

        numRecentFiles = min(files_no, MainWindow.MaxRecentFiles)

        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, self.strippedName(files[i]))
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(files[i])
            self.recentFileActs[i].setVisible(True)

        for j in range(numRecentFiles, MainWindow.MaxRecentFiles):
            self.recentFileActs[j].setVisible(False)

        self.separatorAct.setVisible((numRecentFiles > 0))

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        
        settings = QSettings('mysirrGUI', 'Recent Files')
        files = list(settings.value('recentFileList', []))

        try:
            files.remove(fileName)
        except ValueError:
            pass

        files.insert(0, fileName)
        del files[MainWindow.MaxRecentFiles:]

        settings.setValue('recentFileList', files)

        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.updateRecentFileActions()
      
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit( ret )
