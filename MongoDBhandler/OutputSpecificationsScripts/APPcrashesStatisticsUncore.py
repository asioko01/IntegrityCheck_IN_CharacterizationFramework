from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle

CORES=8


mongoHandler = MongoDBhandler()

mongoHandler.setDB("wseDemo")
mongoHandler.setColl("4instancesUncore870mV_2")
#mongoHandler.setColl("wse_8_incremental_noSdc_setVolBef_inputs2-5")
#mongoHandler.setColl("4instances")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})

numberOfCrashesFrequency={}
vol_to_crashCount={}
vol_to_crashes={}
coreId_to_crashFreq={}
for i in range(CORES):
    coreId_to_crashFreq[i]=0

for doc in mongoHandler._coll.find():
    workloads=doc["workloads"]
    expCrashCount=0
    for workload in workloads:
        #print("Exit_code "+str(workload["exitCode"]) +" System crash "+str(doc["system_crash"])+" Process crash "+str(workload["crash"]))
        if workload["crash"]==True and int(doc["workloads"][0]["inputs"])!=5:  
            expCrashCount=expCrashCount+1
            cores=workload["cores"]
            #print("EXEC_TIME "+str(workload["exec_time"]))
            for core in cores:
                coreId_to_crashFreq[core]=coreId_to_crashFreq.get(core,0)+1
    
    numberOfCrashesFrequency[expCrashCount]=numberOfCrashesFrequency.get(expCrashCount,0)+1
    add=0
    if expCrashCount>0 and int(doc["workloads"][0]["inputs"])!=5: #mark that this experiment encountered app crash
        add=1
    vol=doc["uncore_vol"]
    vol_to_crashes[vol]=vol_to_crashes.get(vol,0)+add
    
    vol=doc["uncore_vol"]
    vol_to_crashCount[vol]=vol_to_crashCount.get(vol,0)+expCrashCount

print("vol appCrashes")    
keys= sorted(vol_to_crashes.keys())
for key in keys:
    print(str(key)+" "+str(vol_to_crashes[key]))

print("\nvol appCrashCount")    
keys= sorted(vol_to_crashCount.keys())
for key in keys:
    print(str(key)+" "+str(vol_to_crashCount[key]))

print("\ncore appCrashCount")    
keys= sorted(coreId_to_crashFreq.keys())
for key in keys:
    print(str(key)+" "+str(coreId_to_crashFreq[key]))
    
print("\nappCrashCount frequency")    
keys= sorted(numberOfCrashesFrequency.keys())
for key in keys:
    print(str(key)+" "+str(numberOfCrashesFrequency[key]))
    

#result=mongoHandler._coll.find({"system_crash":True})
#print(str(result))

