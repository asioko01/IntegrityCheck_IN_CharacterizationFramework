from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
#from curses.has_key import system

mongoHandler = MongoDBhandler()
mongoHandler.setDB("wseDemo")
mongoHandler.setColl("4instances900mV")
#mongoHandler.setDB("wseDemo")
#mongoHandler.setColl("wse_8_incremental_noSdc_setVolBef_inputs2-5")
#mongoHandler.setColl("4instances")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})
errTypes=["undefIns","tainted","unhandled"]

vol_to_HeiErrorCount={}
vol_to_tainted={}
vol_to_undefIns={}
vol_to_unhandl={}

errType_toAppCrashCount={}
errType_toSystemCrashCount={}
uniqueRecordsThatEncounteredErrType={}

#self.pmd_errors=None  #array of pmd_error object
#self.pmd_l2_errors=None  # array pmd_l2_errors object
#self.l3_errors=None #array of l3_error object
#self.mcu_errors=None  #array of mcu_error objects
#self.pcie_errors=None # array of pci_error objects
#self.sata_errors=None #array of sata_error objects

#for doc in mongoHandler._coll.find({"system_crash":True}):
for doc in mongoHandler._coll.find():
    #print(doc['err_messages'])
    #if int(doc["workloads"][0]["inputs"])!=4:
    #    continue
    vol=doc["core_vol"]
    toAdd=0
    if len(doc["pmd_errors"])!=0: 
        toAdd=1
        #if doc["system_crash"]==True:
        print("HEI MESSAGE ENCOUNTERED IN DOC "+str(doc)) 
    if len(doc["pmd_l2_errors"])!=0:
        toAdd=1 
        if doc["system_crash"]==True:
            print("HEI MESSAGE ENCOUNTERED IN DOC "+str(doc)) 
    if len(doc["l3_errors"])!=0:
        toAdd=1
        if doc["system_crash"]==True: 
            print("HEI MESSAGE ENCOUNTERED IN DOC "+str(doc)) 
    if len(doc["mcu_errors"])!=0:
        toAdd=1
        if doc["system_crash"]==True: 
            print("HEI MESSAGE ENCOUNTERED IN DOC "+str(doc)) 
    if len(doc["pcie_errors"])!=0:
        toAdd=1
        if doc["system_crash"]==True: 
            print("HEI MESSAGE ENCOUNTERED IN DOC "+str(doc)) 
    if len(doc["sata_errors"])!=0:
        toAdd=1
        if doc["system_crash"]==True:
            print("HEI MESSAGE ENCOUNTERED IN DOC "+str(doc)) 
    if "HEI" in doc["err_messages"]: #or "hwmon" in doc["err_messages"]:
        if doc["system_crash"]==True:
            toAdd=1
            print("HEI MESSAGE ENCOUNTERED IN DOC "+str(doc))
        else:
            toAdd=1
            print("NON CRASH HEI MESSAGE ENCOUNTERED IN DOC "+str(doc))

    '''if "tainted" in doc["err_messages"]:
        system_crash = doc["system_crash"]
        exec_times=[]
        crashFound=False
        for workload in doc["workloads"]:
            exec_times.append(float(workload["exec_time"]))
            if workload["crash"]==True:
                crashFound=True
        #print("processTainted"+" "+str(doc["_id"])+" "+str(doc["core_vol"])+" "+str(system_crash)+" "+str(crashFound)+" "+str(exec_times))
        vol_to_tainted[vol]=vol_to_tainted.get(vol,0)+1
        errType_toAppCrashCount["tainted"]=errType_toAppCrashCount.get("tainted",0)+int(crashFound)
        errType_toSystemCrashCount["tainted"]=errType_toSystemCrashCount.get("tainted",0)+int(system_crash)
        uniqueRecordsThatEncounteredErrType[doc["_id"]]=1
        print(str(doc["err_messages"]))
        
    if "undefined instruction" in doc["err_messages"]:
        system_crash = doc["system_crash"]
        exec_times=[]
        crashFound=False
        for workload in doc["workloads"]:
            exec_times.append(float(workload["exec_time"]))
            if workload["crash"]==True:
                crashFound=True
        #print("UNDEFINED_INSTRUCTION_ENCOUNTERED"+" "+str(doc["_id"])+" "+str(doc["core_vol"])+" "+str(system_crash)+" "+str(crashFound)+" "+str(exec_times))
        vol_to_undefIns[vol]=vol_to_undefIns.get(vol,0)+1
        errType_toAppCrashCount["undefIns"]=errType_toAppCrashCount.get("undefIns",0)+int(crashFound)
        errType_toSystemCrashCount["undefIns"]=errType_toSystemCrashCount.get("undefIns",0)+int(system_crash)
        uniqueRecordsThatEncounteredErrType[doc["_id"]]=1
        
    if "unhandled" in doc["err_messages"]:
        system_crash = doc["system_crash"]
        exec_times=[]
        crashFound=False
        for workload in doc["workloads"]:
            exec_times.append(float(workload["exec_time"]))
            if workload["crash"]==True:
                crashFound=True
        #print("unhandled"+" "+str(doc["_id"])+" "+str(doc["core_vol"])+" "+str(system_crash)+" "+str(crashFound)+" "+str(exec_times))    
        vol_to_unhandl[vol]=vol_to_unhandl.get(vol,0)+1
        errType_toAppCrashCount["unhandled"]=errType_toAppCrashCount.get("unhandled",0)+int(crashFound)
        errType_toSystemCrashCount["unhandled"]=errType_toSystemCrashCount.get("unhandled",0)+int(system_crash)
        uniqueRecordsThatEncounteredErrType[doc["_id"]]=1
        #print("UNHANDLED MESSAGE ENCOUNTERED IN DOC "+str(doc))
       
    #print(doc["err_messages"])'''
    
    
    vol_to_HeiErrorCount[vol]=vol_to_HeiErrorCount.get(vol,0)+toAdd


print("\nvol heiErrors")
keys= sorted(vol_to_HeiErrorCount.keys())
for key in keys:
    print(str(key)+" "+str(vol_to_HeiErrorCount[key]))
'''    
print("\nvol undefIns")
keys= sorted(vol_to_undefIns.keys())
for key in keys:
    print(str(key)+" "+str(vol_to_undefIns[key]))
    
print("\nvol tainted")
keys= sorted(vol_to_tainted.keys())
for key in keys:
    print(str(key)+" "+str(vol_to_tainted[key]))

print("\nvol unhandled")
keys= sorted(vol_to_unhandl.keys())
for key in keys:
    print(str(key)+" "+str(vol_to_unhandl[key]))

print("\nerrType appCrashCount systemCrashCount")
for errType in errTypes:
    print(str(errType)+" "+str(errType_toAppCrashCount.get(errType,0))+" "+str(errType_toSystemCrashCount.get(errType,0)))

print("\n unique experiments that suffered some error other than HEI "+str(len(uniqueRecordsThatEncounteredErrType.keys())))
    
#print("\nerrType systemCrashCount")
#for errType in errType_toAppCrashCount.keys():
#    print(str(errType)+" "+str(errType_toAppCrashCount[errType]))    

#result=mongoHandler._coll.find({"system_crash":True})
#print(str(result))
'''