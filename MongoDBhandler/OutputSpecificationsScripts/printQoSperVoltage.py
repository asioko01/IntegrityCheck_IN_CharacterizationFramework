from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *

mongoHandler = MongoDBhandler()

mongoHandler.setDB("wseDemo")
mongoHandler.setColl("4instances")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})

#for doc in mongoHandler._coll.find({"system_crash":True}):
corevolToQos={}
corevolToCount={}

for doc in mongoHandler._coll.find():
    for corevol in range (980,870,-10):
        if corevol==doc['core_vol']:
            if doc ['system_crash']==True:
                continue
            for workload in doc["workloads"]:
                qos=0
                if workload ["quality_metric"] is not None:
                    qos=workload["quality_metric"]["value"];
                else:
                    continue;
                corevolToQos[corevol]=corevolToQos.get(corevol,0)+qos
                corevolToCount[corevol]=corevolToCount.get(corevol,0)+1

for corevol in range (980,870,-10):
    sum=corevolToQos.get(corevol,0);
    count=corevolToCount.get(corevol,1);
    avg=sum/count
    print(str(corevol)+" "+str(avg))
    '''for workload in doc["workloads"]:
        if workload["quality_metric"] is not None:
            print(str(workload["quality_metric"]["value"]))'''