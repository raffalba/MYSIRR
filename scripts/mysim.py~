import xml.etree.cElementTree as ET
import os
import sys


projfile=sys.argv[1]

tree=ET.parse(projfile)
root=tree.getroot()
outputfile=sys.argv[2]
for child in root[0]:
    a=child.attrib;
    t=child.text
    name=a['name']
    if name.find("climate")>=0:
        climate=t;
        print 'climate: '+ t
    if name.find("soil")>=0:
        soil=t
        print 'soil: '+ t
    if name.find("crop")>=0:
        crop=t
        print 'crop: '+ t
    if name.find("management")>=0:
        management=t
        print 'management: '+ t
    if name.find("id")>=0:
        idcell=t
        print 'id cell: '+ t
    if name.find("ET")>=0:
        et=t
        print 'ET: '+ t
    if name.find("rain")>=0:
        rain=t
        print 'rain: '+ t
    if name.find("vico")>=0:
        vico=t
        print 'vico: '+ t
    if name.find("s_start")>=0:
        s_start=t
        print 's_start: '+ t

command='python mysirr.py'
command=command+' '+ climate+' '+soil+' '+crop+' '+management+' '+idcell+' '+et+' '+rain+' '+outputfile+' '+vico+' '+s_start
print command
os.system(command)
