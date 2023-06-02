import sys
#from xml.dom import minidom
from Experiment import Experiment
from Executor import Executor
#from ExecutorIDLE import Executor
import json
from MongoDBhandler import MongoDBhandler
import subprocess

confFile=sys.argv[1]
with open(confFile) as json_file:
    data=json.load(json_file)

if "mongoDB" in data and "mongoCol" in data:
    if "mongoIP" in data:
        mongoDBhandler = MongoDBhandler(ip=data["mongoIP"],port=27017,user="zach",password="uniserver2017")
    else:
        mongoDBhandler = MongoDBhandler()
        mongoDBhandler.setDB(data["mongoDB"])
        mongoDBhandler.setColl(data["mongoCol"])
        mongoDBhandler.setGlobal()
    
executor = Executor.convertJsonToObject(data)
list_experiments_json=data["experiments"]
experiments=[]
for experiment_json in list_experiments_json:
    experiments.append(Experiment.covertJSONtoObject(experiment_json))
CURRENTCORERUNNING1=0    
for experiment in experiments:
    for rep in range(experiment.repetitions):
        
        if "juno_a53" in str(experiment.platform):
            executor.configureJunoA53(experiment)
        elif "juno" in str(experiment.platform):
            executor.configureJuno(experiment)
        else:
            executor.configureTheTarget(experiment)
        executor.execute_full_exp(experiment,CURRENTCORERUNNING=CURRENTCORERUNNING1)
        CURRENTCORERUNNING1+=1
        if(CURRENTCORERUNNING1==4):
            CURRENTCORERUNNING1=0
        if "juno" in str(experiment.platform): # A dirty hack to deal with lost USB ports after JUNO power down
            command = "cd C:/Users/admin/Documents/DevCon/x86/ && chf_helper_renalbeUSBs.bat"
            # os.system("C:/cygwin64/bin/bash.exe -l -c \"/home/zhadji01/hs100.sh 192.168.159.129 9999 off\"")
            result = subprocess.check_output(command, shell=True)
            executor.closeSerial()
            executor.openSerial()

mongoDBhandler.closeConnection()



#xmldoc = minidom.parse(confFile)

#        for instruction_type in itemList:
#            name=instruction_type.attributes["id"].value;
#list_runs = xmldoc.getElementsByTagName("run")
##executor = Executor.convertXMLtoOBJ(xmldoc.getElementsByTagName("executor")[0])
#runs=[] # list that will hold all runs
#for xml_run in list_runs:
    #print (str(run.attributes["cmd_line"].value))
    #print (str(xml_run.attributes["frequency"].value))
    #command_line="ls",active_cores=0,idle_cores="2,3,4,5,6,7",start_voltage=980,end_voltage=0,vol_inc=10,frequency=2400,repetitions=1
#    runs.append(Experiment.covertXMLtoObject(xml_run))
    
#for run in runs:
#    for rep in range(run.repetitions):
#        executor.configureTheTarget(run)
#        executor.execute(run)