'''
Created on 17 Μαΐ 2017

@author: admin
'''

from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle

mongoHandler = MongoDBhandler()

mongoHandler.setDB("juno")
mongoHandler.setColl("various")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})

for doc in mongoHandler._coll.find(): #{"system_crash":True}
    #print(str(doc["core_vol"]))
    print (str(doc))
#result=mongoHandler._coll.find({"system_crash":True})
#print(str(result))