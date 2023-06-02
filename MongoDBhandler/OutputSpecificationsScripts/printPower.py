from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *

mongoHandler = MongoDBhandler()
mongoHandler.setDB("spec2006parsec")
mongoHandler.setColl("spec2006parsec")
#mongoHandler.setDB("Xg2EmViruses")
#mongoHandler.setColl("test")
#mongoHandler.setDB("xg3")
#mongoHandler.setColl("nas_32_3_uncore_32MB")
#mongoHandler.setDB("longTests")
#mongoHandler.setColl("Nominal")
#mongoHandler.setDB("longTests")
#mongoHandler.setColl("nominalNasSpec_withPMDpower")

#mongoHandler.setDB("wseDemo")
#mongoHandler.setColl("wse_8_incremental_noSdc_setVolBef_inputs2-5")
#mongoHandler.setColl("4instances")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})

#for doc in mongoHandler._coll.find({"system_crash":True}):
for doc in mongoHandler._coll.find():
    if doc["workloads"][0]["name"]=="tonto":
        print(str(doc["power"]))
    #if (doc["system_crash"])==False:
    #    print(str(doc["uncore_vol"])+" "+str(doc["power"])+" "+str(doc["system_crash"])+" "+str(doc["date"]))