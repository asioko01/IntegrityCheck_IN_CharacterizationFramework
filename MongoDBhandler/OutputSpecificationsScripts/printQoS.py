from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *

mongoHandler = MongoDBhandler()

mongoHandler.setDB("longTests")
mongoHandler.setColl("Nominal")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})

#for doc in mongoHandler._coll.find({"system_crash":True}):
for doc in mongoHandler._coll.find():
    for workload in doc["workloads"]:
        if workload["quality_metric"] is not None:
            print(str(workload["quality_metric"]["value"]))