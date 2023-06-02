from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *

mongoHandler = MongoDBhandler()

mongoHandler.setDB("wseDemo")
mongoHandler.setColl("4instancesUncore")
#mongoHandler.setColl("4instances")
#mongoHandler.setDB("juno")
#mongoHandler.setColl("a72_i++133mVvirus")
#.setDB("juno")
#mongoHandler.setColl("a53_specRef")
#mongoHandler.setDB("test")
#mongoHandler.setColl("wse_demo")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})
count=0
#for doc in mongoHandler._coll.find({"system_crash":True}):
for doc in mongoHandler._coll.find():
            count=count+1
            print(str(doc["system_crash"])+" "+str(doc["date"])+" "+str(doc["uncore_vol"])+" "+str(doc["workloads"][0]["exec_time"]))
            #for workload in doc["workloads"]:
            #print(str(workload["exec_time"]))
            #print(str(doc['err_messages']))
        
            '''if workload["sdc"]==True:
                print("SDC " +str(doc["core_vol"])+" "+str(workload["name"])+" EXEC_TIME "+str(workload["exec_time"])+" WORKLOAD "+str(workload["cores"])+" DOC "+str(doc["_id"]))
                #print("SDC " +str(doc["core_vol"])+" "+str(workload["name"])+" "+str(doc))
                #print("EXEC_TIME "+str(workload["exec_time"]))
            if workload["crash"]==True:
                print("APP_CRASH " +str(doc["core_vol"])+" "+str(workload["name"])+" EXEC_TIME "+str(workload["exec_time"])+" WORKLOAD "+str(workload["cores"])+" DOC "+str(doc["_id"]))'''
                #print("APP_CRASH " +str(doc["core_vol"])+" "+str(workload["name"])+" "+str(doc))
                #print("EXEC_TIME "+str(workload["exec_time"])+" "+str(workload["name"]))
            #if workload["crash"]==False and workload["sdc"]==False and doc["system_crash"]==False:
            #    print("PASS " +str(doc["core_vol"])+" "+str(workload["name"])+" EXEC_TIME "+str(workload["exec_time"])+" WORKLOAD "+str(workload["cores"])+" DOC "+str(doc["_id"]))
            #if workload["name"]=="h264ref":
            #    print ("H264 "+str(doc))
            #print("EXEC_TIME "+str(workload["exec_time"])+" "+str(workload["name"]))
        #if doc["system_crash"]==True:
            #print("SYSTEM_CRASH "+str(doc["core_vol"])+" "+str(workload["name"]))
            #print(str(doc))
        
            #print("EXECUTION TIME "+str(doc["workloads"][0]["exec_time"]))
    #print ("ERR "+str(doc["err_messages"]))
                #print("SYSTEM_CRASH "+str(doc["core_vol"])+" "+str(workload["name"])+" "+str(doc))
            #print ("JUST DOC "+str(doc))
    #print (str(doc))
    #if doc["system_crash"]==True:
    #        print(str(doc))
    #print (str(doc))
    #if int(doc["core_vol"])==990:
    #    print(str(doc["workloads"][0]["exec_time"])+" "+str(doc["workloads"][0]["inputs"]))
    #if(doc["workloads"][0]["exec_time"])
print("Record count "+str(count))