from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *
from Topology import Topology

mongoHandler = MongoDBhandler()
#mongoHandler.setDB("spec2006parsec")
#mongoHandler.setColl("spec2006parsec")
#mongoHandler.setDB("microViruses")
#mongoHandler.setColl("L1I")
#mongoHandler.setDB("microViruses")
#mongoHandler.setColl("testerScript")
mongoHandler.setDB("longTests")
mongoHandler.setColl("realWorkloadUnderVolt")
#mongoHandler.setColl("idealAllvirusMappings_withPMDpower")
#mongoHandler.setDB("worstCaseExploration")
#mongoHandler.setColl("worstCaseExploration")
#mongoHandler.setColl("xg3EmvirusChar_withPMDpower")
#mongoHandler.setColl("xg3EmvirusCharWorstCaseTopologyInstances")
#mongoHandler.setDB("xg2Spec2017")
#mongoHandler.setColl("8rate")

#mongoHandler.setDB("juno")
#mongoHandler.setColl("a72_testDroop")

#mongoHandler.setDB("juno")
#mongoHandler.setColl("a53_specRef")
#mongoHandler.setDB("juno")
#mongoHandler.setColl("a72_i++133mVvirus")

#mongoHandler.setDB("juno")
#mongoHandler.setColl("test")
#mongoHandler.setDB("test")
#mongoHandler.setDB("wseDemo")
#mongoHandler.setColl("4instances")
#mongoHandler.setDB("xg3")
#mongoHandler.setColl("nas_32_3_uncore_32MB")
#mongoHandler.setDB("juno")
#mongoHandler.setColl("a53")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})

#for doc in mongoHandler._coll.find({"system_crash":True}):
benchToVmin={}
topologyToVmin ={}

for doc in mongoHandler._coll.find():
        #print ("JUST DOC "+str(doc))
        #print(str(doc['err_messages']))
    #if  doc["platform"]=="juno_a53":
        #print(str(doc))
        #for workload in doc["workloads"]:
            #print(str(workload["exec_time"]))
        #print(str(doc['workloads'][0]))
        #if int(doc ["core_to_freq"][0])!=950:
        #    continue;
        workloads=doc["workloads"]
        fail=False
        sdcFail=False
        appFail=False
        systemFail=False
        for workload in workloads:
            if workload["sdc"]==True:
                fail=True
                sdcFail=True
                break
            if workload["crash"]==True:
                fail=True
                appFail=True
                break
        if doc["system_crash"]==True:
            fail=True
            systemFail=True
        failMsg=str(workload["name"])+" "+str(doc["core_vol"])+" "+str(workload["exec_time"])
        
        if sdcFail==True:
            failMsg="1 "+failMsg
        else:
            failMsg="0 "+failMsg
        
        if appFail==True:
            failMsg="1 "+failMsg
        else:
            failMsg="0 "+failMsg
        
        if systemFail==True:
            failMsg="1 "+failMsg
        else:
            failMsg="0 "+failMsg
        
        if (fail==True):
            failMsg="1 "+failMsg
            name=workload["name"]
            core_vol=doc["core_vol"]
            vmin=benchToVmin.get(name,0)
            if core_vol>vmin:
                benchToVmin[name]=core_vol
                top = Topology.returnTopology(workload["cores"], 16, 32, 2)
                topologyToVmin[top]=core_vol+20
        else:
            failMsg="0 "+failMsg
        print (str(failMsg))
      
for name in benchToVmin.keys():
    print(str(name)+ " "+str(benchToVmin[name])) 

for top in topologyToVmin.keys():
    print(str(top)+" "+str(top.activeCores())+" "+str(topologyToVmin[top]))

    