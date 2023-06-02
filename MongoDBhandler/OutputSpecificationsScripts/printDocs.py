from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *

mongoHandler = MongoDBhandler()

#mongoHandler.setDB("longTests")
#mongoHandler.setColl("Nominal")

#mongoHandler.setDB("longTests")
#mongoHandler.setColl("idealNasSpec_withPMDpower")

mongoHandler.setDB("spec2006parsec")
mongoHandler.setColl("spec2006parsec")

#mongoHandler.setDB("worstCaseExploration")
#mongoHandler.setColl("worstCaseExploration")

#mongoHandler.setDB("xg2Spec2017")
#mongoHandler.setColl("8rate")

#mongoHandler.setDB("wseDemo")
#mongoHandler.setColl("4instances")
#mongoHandler.setDB("juno")
#mongoHandler.setColl("a72_i++133mVvirus")
#mongoHandler.setDB("juno")
#mongoHandler.setColl("a53_specRef")
#mongoHandler.setDB("test")
#mongoHandler.setColl("wse_demo")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})

#for doc in mongoHandler._coll.find({"system_crash":True}):
for doc in mongoHandler._coll.find():
    if doc["workloads"][0]["name"]=="tonto":
        print(str(doc))
        
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