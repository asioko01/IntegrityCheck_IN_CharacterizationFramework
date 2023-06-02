from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *

mongoHandler = MongoDBhandler()

#"mongoCol":"Nominal",
#      "mongoDB":"longTestsCorrect"

mongoHandler.setDB("longTests")
mongoHandler.setColl("idealNasSpec_withPMDpower")

mongoHandler.dropColl()
#mongoHandler.setDB("wseDemo")
#mongoHandler.setColl("wse_8_incremental_noSdc_setVolBef_inputs2-5")
#mongoHandler.setColl("4instances")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})

#for doc in mongoHandler._coll.find({"system_crash":True}):

