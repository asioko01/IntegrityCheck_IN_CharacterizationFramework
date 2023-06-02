from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *

mongoHandler = MongoDBhandler()

#mongoHandler.setDB("Xg2EmViruses")
#mongoHandler.setColl("test")
mongoHandler.setDB("juno")
#mongoHandler.setColl("a72_testEMC0activeC0C1")
#
mongoHandler.setColl("a72_measureEM72-75MHz2activeC0C1")

#mongoHandler.setDB("wseDemo")
#mongoHandler.setColl("wse_8_incremental_noSdc_setVolBef_inputs2-5")
#mongoHandler.setColl("4instances")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})

#for doc in mongoHandler._coll.find({"system_crash":True}):
workloadToPairs={}
for doc in mongoHandler._coll.find():
    #print("\nFreq(MHz) "+str(doc["workloads"][0]["name"]))
    maxamp=0
    tmp=[]
    highFreq=0
    
    for freq,amp in doc["EM"]:
        #print(str(freq)+" "+str(amp))
        tmp.append((freq,amp))
        if float(amp) > maxamp:
            maxamp=float(amp)
            highFreq=freq
            
    workloadToPairs[doc["workloads"][0]["name"]]=tmp
    print("HighestAmpFor "+ str(doc["workloads"][0]["name"])+" "+str(maxamp)+" "+str(highFreq))

for workload in workloadToPairs.keys():
    tmp= workloadToPairs[workload]
    print("\nFreq(MHz) "+str(workload))
    for freq,amp in tmp:
        print(str(freq)+" "+str(amp))