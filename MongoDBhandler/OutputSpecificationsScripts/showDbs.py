from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *

#mongoHandler = MongoDBhandler("151.80.40.138","27017","zach","uniserver2017")

#print(str(mongoHandler._client.database_names()))
#mongoHandler = MongoDBhandler()
#mongoHandler.


import pymongo
from pymongo import MongoClient

#client = MongoClient('mongodb://zach:uniserver2017@151.80.40.138')
'''client = MongoClient('151.80.40.138',27017)
db = client['test']
db.authenticate('zach','uniserver2017')
print(client.database_names())
# Get the sampleDB database
db = client.sampleDB'''

client = MongoClient('127.0.0.1',27017)
db = client['test']
db.authenticate('zach','uniserver2017')
print(client.database_names())
# Get the sampleDB database
db = client.sampleDB

#mongoHandler.setDB("wseDemo")
#mongoHandler.setColl("wse_8_incremental_noSdc_setVolBef_inputs2-5")
#mongoHandler.setColl("4instances")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})

#for doc in mongoHandler._coll.find({"system_crash":True}):

