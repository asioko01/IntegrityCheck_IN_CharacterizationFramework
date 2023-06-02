from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle

CORES=8


mongoHandler = MongoDBhandler()

mongoHandler.setDB("xg3")
mongoHandler.setColl("aproxe01_virus_vmin_zachvirus")
mongoHandler.setColl("a53ganton12VminIdle180s_goodfinal")
#mongoHandler.setColl("wse_8_incremental_noSdc_setVolBef_inputs2-5")
#mongoHandler.setColl("4instances")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})

numberOfSdcsFrequency={}
vol_to_sdcCount={}
vol_to_sdc={}
coreId_to_sdcFreq={}
for i in range(CORES):
    coreId_to_sdcFreq[i]=0

for doc in mongoHandler._coll.find():
    workloads=doc["workloads"]
    expCrashCount=0
    #print(doc)
    for workload in workloads:
        #print("Exit_code "+str(workload["exitCode"]) +" System crash "+str(doc["system_crash"])+" Process crash "+str(workload["crash"]))
        if workload["sdc"]==True:
            expCrashCount=expCrashCount+1
            cores=workload["cores"]
            #print("EXEC_TIME "+str(workload["exec_time"]))
            for core in cores:
                coreId_to_sdcFreq[core]=coreId_to_sdcFreq.get(core,0)+1
    
    numberOfSdcsFrequency[expCrashCount]=numberOfSdcsFrequency.get(expCrashCount,0)+1
    add=0
    if expCrashCount>0: #mark that this experiment encountered app crash
        add=1
    vol=doc["core_vol"]
    vol_to_sdc[vol]=vol_to_sdc.get(vol,0)+add
    
    vol=doc["core_vol"]
    vol_to_sdcCount[vol]=vol_to_sdc.get(vol,0)+expCrashCount

print("vol sdc")    
keys= sorted(vol_to_sdc.keys())
for key in keys:
    print(str(key)+" "+str(vol_to_sdc[key]))

print("\nvol sdcCount")    
keys= sorted(vol_to_sdcCount.keys())
for key in keys:
    print(str(key)+" "+str(vol_to_sdcCount[key]))

print("\ncore sdcCount")    
keys= sorted(coreId_to_sdcFreq.keys())
for key in keys:
    print(str(key)+" "+str(coreId_to_sdcFreq[key]))
    
print("\nsdcCount frequency")    
keys= sorted(numberOfSdcsFrequency.keys())
for key in keys:
    print(str(key)+" "+str(numberOfSdcsFrequency[key]))
    

#result=mongoHandler._coll.find({"system_crash":True})
#print(str(result))

