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
crash_times=[]
count = 0

#for doc in mongoHandler._coll.find({"system_crash":True}):
for doc in mongoHandler._coll.find():
    toAdd=0
    count = count + 1

    if doc["system_crash"]==True: #and int(doc["workloads"][0]["inputs"])==4:
        toAdd=1
        crash_times.append(doc["workloads"][0]["exec_time"])
        #print(str(doc))
    vol=doc["uncore_vol"]
    vol_to_crashes[vol]=vol_to_crashes.get(vol,0)+toAdd
    #if vol==920 and doc["system_crash"]==True:
    #    print("THE high v "+str(doc))
    
    # dataset generation
    power = doc["power"][0]["min_max_avg"]
    if (power == None):
        power = [None, None, None]
    elif (len(power) == 1):
        power = [power[0], power[0], power[0]]
    if (doc["workloads"][0]["quality_metric"] == None):
        qos = None
    else:
        qos = doc["workloads"][0]["quality_metric"]["value"]
    
    exec_time = doc["workloads"][0]["exec_time"]
    system_crash = doc["system_crash"]
    
    application_crash = False
    for workload in doc["workloads"]:
        if workload["crash"]==True and int(doc["workloads"][0]["inputs"])!=5:  
            application_crash = True
    
    vol=doc["core_vol"]
    vol_to_crashes[vol]=vol_to_crashes.get(vol,0)+toAdd
    #if vol==920 and doc["system_crash"]==True:
    #    print("THE high v "+str(doc))
    
    #print(doc)
    #print("vol: " + str(vol) + "\texectime: " + str(exec_time) + "\tpmin: " + str(power[0]) + "\tpmax: " + str(power[1]) + "\tpavg: " + str(power[2]) + "\tqos: " + str(qos))
    print(str(vol) + "\t" + str(exec_time) + "\t" + str(power[0]) + "\t" + str(power[1]) + "\t" + str(power[2]) + "\t" + str(qos) + "\t" + str(application_crash) + "\t" + str(system_crash))
    
    
print ("total experiments")
print(count)

print("vol crashes")
keys= sorted(vol_to_crashes.keys())
for key in keys:
    print(str(key)+" "+str(vol_to_crashes[key]))

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

