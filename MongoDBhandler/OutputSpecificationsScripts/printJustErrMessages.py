from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *

mongoHandler = MongoDBhandler()

#mongoHandler.setDB("wseDemo")
#mongoHandler.setColl("4instances")
mongoHandler.setDB("spec2006parsec")
mongoHandler.setColl("spec2006parsec")
#mongoHandler.setDB("longTests")
#mongoHandler.setColl("idealNasSpec_withPMDpower")
#mongoHandler.setDB("longTests")
#mongoHandler.setColl("idealAllvirusMappings_withPMDpowerPlus20")

#mongoHandler.setDB("microViruses")
#mongoHandler.setColl("testerScript")

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
   errmessages=str(doc['err_messages'])
   #if "SDC" in errmessages:
   print(str(doc['core_vol'])+" "+str(doc['workloads'][0]['name'])+" "+str(doc['err_messages']).replace("\n"," "))