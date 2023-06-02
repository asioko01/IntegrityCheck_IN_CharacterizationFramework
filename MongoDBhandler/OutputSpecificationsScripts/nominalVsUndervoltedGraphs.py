from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *
from random import Random
import Topology
import operator
from pywin.framework.mdi_pychecker import STATIC

class run(object):
    def __init__(self,workloadName,voltage,powerValues,executionTime,activeCores):
        self.setWorkloadName(workloadName)
        self.setVoltage(voltage)
        self.setPowerValues(powerValues)
        self.setExecutionTime(executionTime)
        self.setActiveCores(activeCores)
    
    def setActiveCores(self,activeCores):
        assert type(activeCores) == list,"run.setActiveCores parameter should be list"
        self.activeCores=sort(activeCores)
    
    def setVoltage(self,voltage):
        assert type(voltage) == int,"setVoltage parameter should be int"
        self.voltage=voltage
    
    def setWorkloadName(self,workloadName):
        assert type(workloadName) == str,"workloadName should be str"
        self.workloadName=workloadName
        
    def setPowerValues(self,powerValues):
        assert type(powerValues) == list,"power values parameter should be list"
        self.powerValues = powerValues
        
    def setExecutionTime(self,executionTime):
        assert type(executionTime) == float,"execution time should be float"
        self.executionTime=executionTime
        
    def getPowerValuesLineByLine(self):
        toReturn=""
        for powerValue in self.powerValues:
            toReturn=toReturn+"\n"+str(powerValue)
    
    def getWorkloadVoltagePower(self):
        toReturn=""
        for powerValue in self.powerValues:
            toReturn=toReturn+str(self.workloadName)+" "+str(self.getActiveCoreStr())+" "+str(self.voltage)+" "+str(powerValue)+"\n"
        return toReturn
    
    def getActiveCoreStr(self):
        coresStr=""
        for core in self.activeCores:
            coresStr=coresStr+str(core)
        return coresStr
    
    @staticmethod
    def getActiveCoreStrStatic(inp):
        coresStr=""
        for core in inp:
            coresStr=coresStr+str(core)
        return coresStr
    
    def getPrettyName(self):
        return self.workloadName+"_"+self.getActiveCoreStr()
    
    def __eq__(self,other):
        return self.getPrettyName()==other.getPrettyName()
    
    def __hash__(self):
        return hash(self.getPrettyName())
    
    def __str__(self):
        return self.getPrettyName()+" "+self.workloadName+" "+self.getActiveCoreStr()+" "+str(self.voltage)+" "+str(self.executionTime)+" "+str(sum(self.powerValues)/len(self.powerValues))
        
def checkIfRunInDocIsPass(doc): #TODO currently we ignore if there are more workloads
    workload = doc["workloads"][0]
    if workload["crash"]==False and workload["sdc"]==False and doc["system_crash"]==False:
        return True
    #if workload["name"]=="dc.B.x": #TODO remove this hack.. is because some dc. runs mistaken recorded as SDC
    #    return True
    #    return False

def returnNaive(strToCheck):
    if strToCheck=="0":
        return  900
    if strToCheck=="1":
        return 910 
    if strToCheck=="2":
        return 900 
    if strToCheck=="3":
        return 900
    if strToCheck=="4":
        return 900 
    if strToCheck=="5":
        return 900 
    if strToCheck=="6":
        return 910 
    if strToCheck=="7":
        return 910 
    if strToCheck=="01":
        return 910
    if strToCheck=="23":
        return 910
    if strToCheck=="45":
        return 910 
    if strToCheck=="67":
        return 910 
    if strToCheck=="02":
        return 910 
    if strToCheck=="024":
        return 920 
    if strToCheck=="012":
        return 910 
    if strToCheck=="0123":
        return  930
    if strToCheck=="0246":
        return 930 
    if strToCheck=="0124":
        return 930 
    if strToCheck=="01234":
        return 950 
    if strToCheck=="01246":
        return 930 
    if strToCheck=="012345":
        return 940 
    if strToCheck=="012346":
        return 950 
    if strToCheck=="0123456":
        return 950 
    if strToCheck=="01234567":
        return 970
    else:
        return False 
        
##INPUTS
nominalVol=980
mongoHandler = MongoDBhandler()
mongoHandler.setDB("longTests")

collsToCheck =[]
collsToCheck.append("nominalNasSpec_withPMDpower")
collsToCheck.append("idealNasSpec_withPMDpower")
collsToCheck.append("nominalAndUndervoltNasSpec_withPMDpower")
stopOnTargetUnique=True
targetUnique=140
totalPMDs=4
totalCores=8
coresPerPMD=2
##END of inputs

nominalRunsList=[]
nominalToUnderVolt={}
underVoltedRunsSet={}
setInstancesCoverage=set()
topologyHisto={}
#topInsHisto=0
allTopInstances=Topology.Topology.getAllInstancesStatic(totalCores, totalPMDs, coresPerPMD)
topInstanceToCount={}
for i in range(len(allTopInstances)):
    topInstanceToCount[run.getActiveCoreStrStatic(allTopInstances[i])]=0

for coll in collsToCheck:
    mongoHandler.setColl(coll)
    for doc in mongoHandler._coll.find():
        if checkIfRunInDocIsPass(doc)== True: 
            workload = doc["workloads"][0] #TODO currently we ignore if there are more workloads
            workloadName = workload["name"] 
            voltage = int(doc["core_vol"])
            executionTime = float(workload["exec_time"])
            activeCores = workload["cores"]
            powerValues = doc["power"][0]["values"]
            newRun = run(workloadName, voltage, powerValues, executionTime, activeCores)
            
            if voltage == nominalVol:
                nominalRunsList.append(newRun)
            else:
                underVoltedRunsSet[newRun]=newRun

rand = Random(1)
rand.shuffle(nominalRunsList)

#for nominalRun in nominalRunsList:
#    print(str(nominalRun))

#for undervoltedRun in underVoltedRunsSet:
#    print(str(undervoltedRun))

matches=0
runToStop=0
totalExecutionTime=0
##create the nominal to undervolted correspondence
for nominalRun in nominalRunsList:
    if stopOnTargetUnique==True and len(setInstancesCoverage)==targetUnique:
        break
    else:
        if nominalRun in underVoltedRunsSet:
            undervoltedRun=underVoltedRunsSet[nominalRun]
            atopology=Topology.Topology.returnTopology(nominalRun.activeCores, totalPMDs,totalCores,coresPerPMD) 
            count=0
            if atopology in topologyHisto:
                count=topologyHisto[atopology]
            if(abs(undervoltedRun.executionTime-nominalRun.executionTime)<11 and count<25):
                nominalToUnderVolt[nominalRun]=undervoltedRun
                setInstancesCoverage.add(nominalRun.getActiveCoreStr())
                matches=matches+1
                runToStop=runToStop+1
                totalExecutionTime=totalExecutionTime+nominalRun.executionTime
                topInstanceToCount[nominalRun.getActiveCoreStr()]=topInstanceToCount[nominalRun.getActiveCoreStr()]+1
                if atopology in topologyHisto:
                    count=topologyHisto[atopology]
                    count=count+1
                    topologyHisto[atopology]=count
                else:
                    topologyHisto[atopology]=1
            else:
                nominalToUnderVolt[nominalRun]="missing"
        else:
            nominalToUnderVolt[nominalRun]="missing"

'''for nominalRun in nominalRunsList:
    if nominalRun in underVoltedRunsSet:
        print(str(nominalRun)+" "+str(nominalToUnderVolt[nominalRun]))
    else:
        print(str(nominalRun.workloadName)+" "+"missing")'''
    
    #print(str(nominalRun.getPowerValuesLineByLine()))

fnominal = open("nominal_out","w")
i=0
for nominalRun in nominalRunsList:
    if i==runToStop:
        break
    if type(nominalToUnderVolt[nominalRun])!=str:
        if nominalRun in underVoltedRunsSet:
            fnominal.write(str(nominalRun.getWorkloadVoltagePower()))
            i=i+1
fnominal.close()

flvl10 = open("lvl1.0_out","w")
fundervolt = open("undervolt_out","w")

i=0
for nominalRun in nominalRunsList:
    if runToStop==i:
        break
    if type(nominalToUnderVolt[nominalRun])!=str:
        i=i+1
        underVoltedRun=underVoltedRunsSet[nominalRun]
        fundervolt.write(str(underVoltedRun.getWorkloadVoltagePower()))
        print(str(nominalRun))
        for value in range(len(underVoltedRun.powerValues)):
            naive=returnNaive(nominalRun.getActiveCoreStr())
            if type(naive)==bool and naive==False:
                flvl10.write(str(970)+"\n")
            else:
                #flvl10.write(str(underVoltedRun.voltage)+"\n")
                flvl10.write(str(naive)+"\n")
fundervolt.close()
flvl10.close()

print("\n"+str(len(nominalRunsList))+" "+str(len(underVoltedRunsSet))+" "+str(len(setInstancesCoverage))+" "+str(matches)+" "+str(totalExecutionTime/60/60/24))
topologiesSorted=sorted(topologyHisto.keys(),key=operator.attrgetter('active_cores'))

for topology in topologiesSorted:
    print(str(topology)+" "+str(topologyHisto[topology])+" "+str(topologyHisto[topology]/matches))
for topInstance in allTopInstances:
    print(run.getActiveCoreStrStatic(topInstance)+" "+str(topInstanceToCount[run.getActiveCoreStrStatic(topInstance)]))