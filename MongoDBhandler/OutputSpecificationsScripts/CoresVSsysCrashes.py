from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *
from numpy.random import sample


mongoHandler = MongoDBhandler()

# 4instancesGUI_horizontal_pmd_soc_sep
# 4instancesGUI_horizontal_pmd_soc_sep_exept980
# 4instancesGUI_horizontal_soc_and_pmd_930_920
# 4instancesGUI_horizontal_pmd_soc_dram_comb
# 4instancesGUI_horizontal_pmd_soc_dram_comb_only_pmd920_soc890_880
# 4instancesGUI_horizontal_highpfail_2
# 4instancesGUI_horizontal_pmd_soc_power_pfail
# 4instancesGUI_horizontal_pmd_soc_dram_comb_pfail
# 4instancesGUI_horizontal_pmd910_soc870_dram1428_dramrr2783
# 4instancesGUI_horizontal_pmd900_soc870_pmd930_soc920_dram1428_dramrr2783      # SDC 1511206319 1511205303 1511204659 1511203061 1511201782
# 4instancesGUI_horizontal_mix_noreboot_nomdram 
# 4instancesGUI_horizontal_mix_noreboot_nomdram2                                # SDC? 1511217364 
# 4instancesGUI_horizontal_pmd_reboot
# 4instancesGUI_horizontal_pmd910_5x5
# 4instancesGUI_horizontal_pmd900_10x2_test
# =======================================================
# 4instancesGUI_horizontal_pmd_reboot
# 4instancesGUI_horizontal_pmd_reboot_2
# 4instancesGUI_horizontal_pmd_reboot_2_missing
# 4instancesGUI_horizontal_pmd_reboot_rest
# 4instancesGUI_horizontal_pmd_reboot_rest2
#4instancesGUI_horizontal_ucy_safe_1000
#4instancesGUI_horizontal_idle_10_10_920_880
#"4instancesGUI_horizontal_pmd910_s100r2_lower_pmd_soc_vol_gradually_removebias4

mongoHandler.setDB("xg3")                                                   #4instances910mV_test2#4instances910mV_ramdiskInputfile_900secDelay_reboot_20x10exp#4instances910mV_ramdiskInputfile_900secDelay_rebootAll
mongoHandler.setColl("aproxe01_virus_vmin_zachvirus")  #4instances910mV_ramdiskInputfile_firstCrash1r#4instances_Core910mV_Uncore870mV_ramdiskInputfile#4instances910mV_ramdiskInputfile_120secDelay_firstCrash1
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
last_crash = True
totalNmV = 0


sample_count = 0
samples = []

samples_pmd = []
samples_soc = []
    

pmd = 980
soc = 950
NmV = 980

count_NmV = 0
#for doc in mongoHandler._coll.find({"system_crash":True}):
print("vol\tuvol\texect\tpmin\tpmax\tpavg\tqos\tacrash\tscrash") 
# START OF A big loop going through all entries in the database
for doc in mongoHandler._coll.find():
#     if (count % sets == 0):
#         print(" \t \t \t \t \t \tFalse\tFalse\tINIT")  
    toAdd=0
    
    if doc["system_crash"]==True: #and int(doc["workloads"][0]["inputs"])==4:
        
        toAdd=1
        crash_times.append(doc["workloads"][0]["exec_time"])
        #print(str(doc))
    
    power = doc["power"][0]["min_max_avg"]
    if (power == None):
        power = [None, None, None]
    elif (len(power) == 1):
        power = [power[0], power[0], power[0]]
    if (doc["workloads"][0]["quality_metric"] == None):
        qos = None
    else:
        qos = doc["workloads"][0]["quality_metric"]["value"]
    
    exec_time = doc["workloads"][0]["exec_time"]
    system_crash = doc["system_crash"]
    
    application_crash = False
    for workload in doc["workloads"]:
        if workload["crash"]==True and int(doc["workloads"][0]["inputs"])!=5:  
            application_crash = True
    
    vol=doc["core_vol"]
    uvol=doc["uncore_vol"]
    vol_to_crashes[vol]=vol_to_crashes.get(vol,0)+toAdd
    
    
    if not (vol == 980 and uvol == 950):
        count = count + 1
    if vol == 930:
        totalNmV = totalNmV + 1

    # FOR SIMPLICITY WORK BELOW THIS LINE

#     if (vol == pmd and uvol == soc):
#         if sample_count < 101:
#             if not (doc['power'][0]['min_max_avg'] == None):
#                 for p in doc['power'][0]['min_max_avg'][:-3]:
#                         samples_pmd.append(p)
#             if not (doc['power'][1]['min_max_avg'] == None):
#                 for p in doc['power'][1]['min_max_avg'][:-3]:
#                     if not p == None:
#                         samples_soc.append(p)
#             print(doc['power'][0]['min_max_avg'])
#             print(doc['power'][1]['min_max_avg'])
#             print(str(vol) + "\t" + str(uvol) + "\t" + str(exec_time) + "\t" + str(power[-3]) + "\t" + str(power[-2]) + "\t" + str(power[-1]) + "\t" + str(qos) + "\t" + str(application_crash) + "\t" + str(system_crash))
#         sample_count = sample_count + 1
# #     if (doc["date"] == 1510560040):
    print(str(vol) + "\t" + str(uvol) + "\t" + str(exec_time) + "\t" + str(power[-3]) + "\t" + str(power[-2]) + "\t" + str(power[-1]) + "\t" + str(qos) + "\t" + str(application_crash) + "\t" + str(system_crash))

#     if (vol == pmd and uvol == soc):
#     if doc["date"] == 1511217314:
#         print(str(vol) + "\t" + str(uvol) + "\t" + str(exec_time) + "\t" + str(power[-3]) + "\t" + str(power[-2]) + "\t" + str(power[-1]) + "\t" + str(qos) + "\t" + str(application_crash) + "\t" + str(system_crash))
# 
#     print(doc["date"])

    NmV = 890
    if (vol == NmV):
        count_NmV += 1

# END OF A big loop going through all entries in the database

print("count " + str(NmV) + ": " + str(count_NmV))

#         if (doc["date"] == 1511):
#             print(str(vol) + "\t" + str(uvol) + "\t" + str(exec_time) + "\t" + str(power[-3]) + "\t" + str(power[-2]) + "\t" + str(power[-1]) + "\t" + str(qos) + "\t" + str(application_crash) + "\t" + str(system_crash))

#     if application_crash or system_crash:
#         print(doc["date"])

# import sys
#  
# fpmd = open('C:/Users/admin/Desktop/power_results_15_11_2017/pmd' + str(pmd) + '_soc' + str(soc) + '_pmd_power.txt', 'w')
# sample_count = 0
# print('PMD')
# for p in samples_pmd:
# #     print(p)
#     fpmd.write(str(p) + '\n')
#     sample_count = sample_count + 1
# fpmd.close()
#  
# print('Sample Count PMD')
# print(sample_count)
#  
# fsoc = open('C:/Users/admin/Desktop/power_results_15_11_2017/pmd' + str(pmd) + '_soc' + str(soc) + '_soc_power.txt', 'w')
# sample_count = 0
# print('SoC')
# for p in samples_soc:
# #     print(p)
#     fsoc.write(str(p) + '\n')
#     sample_count = sample_count + 1
# fsoc.close()
#  
# print('Sample Count SoC')
# print(sample_count)

  
#     if (vol == pmd and uvol == soc):
#         if sample_count > 0 and sample_count < 101:
#             samples.append(exec_time)
#         sample_count = sample_count + 1
#         
# print(samples)
# import numpy
# arr = numpy.array(samples)
# print(len(samples))
# print(numpy.mean(arr, axis=0))
# print(numpy.std(arr, axis=0))
    #if vol==920 and doc["system_crash"]==True:
    #    print("THE high v "+str(doc))
    
    #print(doc)
    #if (vol == 900):
#     print("vol: " + str(vol) + "\texectime: " + str(exec_time) + "\tpmin: " + str(power[0]) + "\tpmax: " + str(power[1]) + "\tpavg: " + str(power[2]) + "\tqos: " + str(qos))
#     if (not (vol == 980 and uvol == 950)):
#         if not((system_crash or application_crash) and last_crash):
#             #print(str(doc) + " ABC")
#             print(str(vol) + "\t" + str(uvol) + "\t" + str(exec_time) + "\t" + str(power[0]) + "\t" + str(power[1]) + "\t" + str(power[2]) + "\t" + str(qos) + "\t" + str(application_crash) + "\t" + str(system_crash))

#     if (uvol > 934 and uvol < 945):
#         print(str(vol) + "\t" + str(uvol) + "\t" + str(exec_time) + "\t" + str(power[0]) + "\t" + str(power[1]) + "\t" + str(power[2]) + "\t" + str(qos) + "\t" + str(application_crash) + "\t" + str(system_crash))

#     if not (vol == 980 and uvol == 980):
#         print("time difference: " + str(doc["date"] - prev_date))
#         prev_date = doc["date"]
        #print(doc)
#     if (application_crash or system_crash):
#         print(doc)
#     if (count == 10):
#         print(doc)
#     if (count == 1 or count == 2):
#         print("######### " + str(count) + " #########")
#         print(doc)
    
#     if system_crash or application_crash:
#         last_crash = True
#     else:
#         last_crash = False
    

print ("total experiments")
print(count)    

print("vol crashes")
keys= sorted(vol_to_crashes.keys())
for key in keys:
    print(str(key)+" "+str(vol_to_crashes[key]))

print("\ncrash times")
for value in crash_times:
    print(value)

print("\ntotal n mv")
print(totalNmV)

print(sorted(crash_times))

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

