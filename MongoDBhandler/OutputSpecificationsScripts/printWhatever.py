from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *

mongoHandler = MongoDBhandler()

#mongoHandler.setDB("wseDemo")
#mongoHandler.setColl("4instances900mV")
#mongoHandler.setDB("xg3")
#mongoHandler.setColl("nas_32_3_uncore_32MB")
#mongoHandler.setDB("xg2Spec2017")
#mongoHandler.setColl("8rate")

mongoHandler.setDB("xg3")
mongoHandler.setColl("aproxe01_virus_vmin")

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
    if doc["core_vol"]==880 and doc["workloads"][0]["name"]=="theVirus_4":
        print(str(doc))