from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *

mongoHandler = MongoDBhandler()

mongoHandler.setDB("wseDemo")
mongoHandler.setColl("4instancesUncore")
#mongoHandler.setColl("wse_8_incremental_noSdc_setVolBef_inputs2-5")
#mongoHandler.setColl("4instances")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})

vol_to_crashes={}
vol_to_sys_crashes={}
vol_to_app_crashes={}
crash_times=[]
count = 0

found = False

#for doc in mongoHandler._coll.find({"system_crash":True}):
for doc in mongoHandler._coll.find():
    toAdd=0
    toAdd_sys=0
    toAdd_app=0

    application_crash = False
    system_crash = False
    
    vol=doc["uncore_vol"]
    
    if (vol == 860):
        count = count + 1
    if (vol == 950):
        found = False;
    
    for workload in doc["workloads"]:
        if workload["crash"]==True and int(doc["workloads"][0]["inputs"])!=5:  
            application_crash = True

    if doc["system_crash"]==True: #and int(doc["workloads"][0]["inputs"])==4:
        system_crash = True;
    
    if ((found == False) and (system_crash or application_crash)):
        if system_crash:
            toAdd_sys=1
            crash_type = "     system"
        else:
            toAdd_app=1
            crash_type = "application"
        found = True;
        toAdd=1
        crash_times.append(crash_type + "\t" + str(doc["workloads"][0]["exec_time"]))
        #print(str(doc))
    
    if ((vol == 850) and (system_crash==False and application_crash==False)):
        print("850 did not crash at all!!!")
    
    vol_to_crashes[vol]=vol_to_crashes.get(vol,0)+toAdd
    vol_to_sys_crashes[vol]=vol_to_sys_crashes.get(vol,0)+toAdd_sys
    vol_to_app_crashes[vol]=vol_to_app_crashes.get(vol,0)+toAdd_app
    #if vol==920 and doc["system_crash"]==True:
    #    print("THE high v "+str(doc))
    
    # dataset generation
    
print ("total experiments")
print(count) 

print("vol crashes")
keys= sorted(vol_to_crashes.keys())
for key in keys:
    print(str(key)+" "+str(vol_to_crashes[key])+" sys: "+str(vol_to_sys_crashes[key])+" app: "+str(vol_to_app_crashes[key]))

print("\ncrash times")
for value in crash_times:
    print(value)

#bins=[]
#for i in range(int(max(crash_times))+1):
#    bins.append(i)
#hist, bin_edges=histogram(crash_times,bins) 
#print(hist)    
#for i in range(len(hist)):
    #print(str(bin_edges[i])+" "+str(hist[i]))
#    print(str(hist[i]))
#for crash_time in crash_times:
#    print(str(crash_time))
#result=mongoHandler._coll.find({"system_crash":True})
#print(str(result))

