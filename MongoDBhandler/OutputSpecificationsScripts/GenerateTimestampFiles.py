from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *
from numpy.random import sample


mongoHandler = MongoDBhandler()

# 4instancesGUI_horizontal_pmd_soc_power_pfail
# 4instancesGUI_horizontal_pmd_soc_dram_comb_pfail
# 4instancesGUI_horizontal_pmd910_soc870_dram1428_dramrr2783
# 4instancesGUI_horizontal_pmd900_soc870_pmd930_soc920_dram1428_dramrr2783
# 4instancesGUI_horizontal_mix_noreboot_nomdram
#4instancesGUI_horizontal_pmd_900_rest_nominal_1x10

mongoHandler.setDB("wseDemo")                                                   
mongoHandler.setColl("4instancesGUI_horizontal_ucy_safe_1000")  

vol_to_crashes={}
crash_times=[]
count = 0
sets = 100
prev_date = 0
last_crash = True
totalNmV = 0


sample_count = 0
samples = []

samples_pmd = []
samples_soc = []
    

pmd = 970
soc = 940

res = {}

for doc in mongoHandler._coll.find():
    vol=doc["core_vol"]
    uvol=doc["uncore_vol"]
#     if (vol == pmd and uvol == soc):
#         print(doc["date"])
    if "core"+str(vol)+"uncore"+str(uvol) in res:
        res["core"+str(vol)+"uncore"+str(uvol)].append(doc["date"])
    else:
        res["core"+str(vol)+"uncore"+str(uvol)] = []
        res["core"+str(vol)+"uncore"+str(uvol)].append(doc["date"])

print(res)

import sys

for config, timestamps in res.items():
    fpmd = open('C:/Users/admin/Desktop/timestamps/reboots/' + str(config) + '.txt', 'w')
    if config == "core980uncore950":
        count = 0
        for p in timestamps:
            if (count > 0 and count < 101):
                fpmd.write(str(p) + '\n')
            count += 1 
    else:
        for p in timestamps:
            fpmd.write(str(p) + '\n')
    fpmd.close()

