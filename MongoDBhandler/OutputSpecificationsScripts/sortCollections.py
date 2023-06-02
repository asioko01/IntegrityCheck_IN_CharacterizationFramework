from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *


mongoHandler = MongoDBhandler()

mongoHandler.setDB("wseDemo")                                                   #4instances910mV_test2#4instances910mV_ramdiskInputfile_900secDelay_reboot_20x10exp#4instances910mV_ramdiskInputfile_900secDelay_rebootAll
mongoHandler.setColl("4instances_horizontal_core910mVUncore870mV")  #4instances910mV_ramdiskInputfile_firstCrash1r#4instances_Core910mV_Uncore870mV_ramdiskInputfile#4instances910mV_ramdiskInputfile_120secDelay_firstCrash1
#mongoHandler.setColl("wse_8_incremental_noSdc_setVolBef_inputs2-5")900mV_ramdiskNo_warmupDelay120s_warmupNominalRunYes_rebootOnInitYes_rebootAll
#mongoHandler.setColl("4instances")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})

vol_to_crashes={}
crash_times=[]
count = 0
sets = 100
prev_date = 0

import pymongo
client = pymongo.MongoClient("localhost", 27017, maxPoolSize=50)
d = dict( (db, [collection for collection in client[db].collection_names()])
         for db in client.database_names())

d = d['wseDemo']
col_dates_names = []

for c in d:
    mongoHandler.setColl(c)
    col_dates_names.append([c, mongoHandler._coll.find()[0]['date']])

col_dates_names.sort(key=lambda x:x[1])

for elem in col_dates_names:
    print(elem[0])

#print(json.dumps(d))
#print(col_dates_names)
      

