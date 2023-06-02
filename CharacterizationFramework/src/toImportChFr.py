'''
Created on Mar 13, 2017

@author: zhadji01
'''

import sys
from xml.dom import minidom
from Experiment import Experiment
from Executor import Executor


class ChFrPortable(object):
    

    def __init__(self,confFile):
        self.confFile=confFile
        
    def run(self):
        xmldoc = minidom.parse(self.confFile)
        #        for instruction_type in itemList:
        #            name=instruction_type.attributes["id"].value;
        list_runs = xmldoc.getElementsByTagName("run")
        executor = Executor.convertXMLtoOBJ(xmldoc.getElementsByTagName("executor")[0])
        runs=[] # list that will hold all runs
        for xml_run in list_runs:
            #print (str(run.attributes["cmd_line"].value))
            #print (str(xml_run.attributes["frequency"].value))
            #command_line="ls",active_cores=0,idle_cores="2,3,4,5,6,7",start_voltage=980,end_voltage=0,vol_inc=10,frequency=2400,repetitions=1
            runs.append(Experiment.covertJSONtoObject(xml_run))
            
        for run in runs:
            for rep in range(run.repetitions):
                executor.configureTheTarget(run)
                executor.execute(run)