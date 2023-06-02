from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *
from datetime import datetime, timedelta


def datetime_from_millis(millis, epoch=datetime(1970, 1, 1)):
    """Return UTC time that corresponds to milliseconds since Epoch."""
    return epoch + timedelta(seconds=millis)

mongoHandler = MongoDBhandler()

#mongoHandler.setDB("wseDemo")
mongoHandler.setDB("juno")
#mongoHandler.setColl("wse_8_incremental_noSdc_setVolBef_inputs2-5")
mongoHandler.setColl("4instances900mV")
mongoHandler.setColl("a53ganton12VminIdle180s_goodfinal")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})

#vol_to_crashes={}
#date_to_crash=[]


date_to_vol={}
date_to_doc={}
#for doc in mongoHandler._coll.find({"system_crash":True}):
for doc in mongoHandler._coll.find():
    #print("DOC "+str(doc))
    if doc["system_crash"]==True: 
        date=doc["date"]
        #print(str(doc))
        vol=doc["core_vol"]
        #date_to_vol[date]=vol
        #date_to_doc[date]=doc
        date_str=datetime_from_millis(long(date), epoch=datetime(1970, 1, 1))
        date_str=str(date_str).replace(" ","_")
        if vol > 870:
            #print(str(int(str(doc["_id"]),16))+" "+str(date)+" "+date_str+" "+str(vol)+" "+str(doc))
            print(str(date)+" "+date_str+" "+str(vol))
    #if vol==920 and doc["system_crash"]==True:
    #    print("THE high v "+str(doc))
 
#sys.exit()   
'''print("date volCrash")
print("dic len "+str(len(date_to_vol)))
keys= sorted(date_to_vol.keys())
for key in keys:
    date_str=datetime_from_millis(long(key), epoch=datetime(1970, 1, 1))
    #print(str(date_str).replace(" ","_")+" "+str(date_to_vol[key]))
    #print(str(key)+" "+str(date_to_vol[key]))
    vol=date_to_vol[key]
    doc=date_to_doc[key]
    if vol >900:
        date_str=str(date_str).replace(" ","_")
        print(date_str+" "+str(vol)+" "+str(doc))'''
        

#print("\ncrash times")
#for value in crash_times:
    #    print(value)

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

