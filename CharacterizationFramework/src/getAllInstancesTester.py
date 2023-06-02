'''
Created on 21 Μαΐ 2019

@author: admin
'''
from Topology import Topology

totalPmds=16
totalCores=32
coresPerPMD=2

knownTopologies = []
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,1,0))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,0,1))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,0,2))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,0,3))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,1,1))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,0,4))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,2,0))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,1,2))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,2,1))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,1,3))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,3,0))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,2,2))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,3,1))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,4,0))

for topolog in knownTopologies:
    print(str(topolog)+" "+str(len(topolog.getAllInstances())))