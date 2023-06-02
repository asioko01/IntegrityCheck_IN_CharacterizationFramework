from MongoDBhandler import *
from pip._vendor.html5lib.treewalkers import pprint
from jsonpickle import json
import jsonpickle
from numpy import *

mongoHandler = MongoDBhandler()
#mongoHandler.setDB("xg3")
#mongoHandler.setColl("specAproxe")
#mongoHandler.setColl("nas_32_3_aproxe")
#mongoHandler.setColl("zhadji_virus_vminSanityAproxe1000")
#mongoHandler.setColl("nas_32_3_aproxeMissingLUMGSPUA")
#mongoHandler.setDB("spec2006parsec")
#mongoHandler.setColl("spec2006parsec")
#mongoHandler.setDB("longTests")
#mongoHandler.setColl("realWorkloadUnderVoltPlus10")
#mongoHandler.setDB("xg3")
#mongoHandler.setColl("zhadji_virus_vminSanityAproxe")
#mongoHandler.setColl("nas_32_3_aproxeMissingLUMGSPUA")
#mongoHandler.setColl("zhadji_virus_vminFiftyInsHalfMinutesRun")
#mongoHandler.setColl("nas_32_3_aproxe")
#mongoHandler.setColl("aproxe_virus_vminiplusplusLoop")
#realWorkloadUnderVoltPlus10
#mongoHandler.setColl("zhadji_virus_vminFiftyInsThreeMinutesRun")
#mongoHandler.setColl("aproxe_virus_vminFiftyInsThreeMinutesRun")
#mongoHandler.setColl("aproxe_virus_vminFiftyIns")

  #"mongoCol":"test",
   #   "mongoDB":"StressDaemon
#mongoHandler.setColl("idealNasSpec_withPMDpower")
#mongoHandler.setColl("nominalAndUndervoltNasSpec_withPMDpower")
#mongoHandler.setDB("longTests")
#mongoHandler.setColl("idealNasSpecXg3_withPMDpower")
#mongoHandler.setColl("xg3EmvirusCharWorstCaseTopologyInstances")
#mongoHandler.setColl("idealAllvirusMappings_withPMDpowerPlus20")
#mongoDB="longTests"
#mongoCol="idealAllvirusMappings"
#mongoHandler.setDB("worstCaseExploration")
#mongoHandler.setColl("worstCaseExploration")
#  "mongoCol":"idealAllvirusMappings_withPMDpower",
#      "mongoDB":"longTests"
#mongoHandler.setDB("longTests")
#mongoHandler.setColl("NotIdealPlus10")
#mongoHandler.setColl("idealAllvirusMappings_withPMDpower")
#mongoHandler.setDB("longTests")
#mongoHandler.setColl("idealAllvirusMappings_withPMDpower")

#mongoHandler.setDB("microViruses")
#mongoHandler.setColl("L1I")
                                     
#mongoHandler.setDB("wseDemo")
#mongoHandler.setColl("4instances900mV")
#mongoHandler.setDB("xg3")
#mongoHandler.setColl("nas_32_3")


#mongoHandler.setDB("wseDemo")
#mongoHandler.setColl("4instances")
#mongoHandler.setDB("juno")
#mongoHandler.setColl("a72_i++133mVvirus")
mongoHandler.setDB("juno")
#mongoHandler.setColl("a53_specRef")
#mongoHandler.setColl("a53aproxeGood_100")
#mongoHandler.setColl("a53aproxeGood88s")
#mongoHandler.setColl("a53aproxe100")
#mongoHandler.setColl("a53aproxe_950_100")
#mongoHandler.setColl("a53_spec_aproxe")
##mongoHandler.setColl("a53aproxeGood_200exps")
#mongoHandler.setColl("a53aproxeGood_3_4_5")
#mongoHandler.setColl("a53aproxeGood_singleCoresNoGating")
mongoHandler.setColl("a53iminusminus_singleCoresNoGating")
#mongoHandler.setColl("a53aproxeGood_singleCoresNoGating_10msmyinterrupt")
#mongoHandler.setColl("a53aproxeGood_singleCoresNoGating_selfLoop")
mongoHandler.setColl("a53ganton12VminIdle180s_goodfinal")
#mongoHandler.setColl("deletethis4")
mongoHandler.setColl("a53aproxeGood_Virus26s_georgia_vmin")
#mongoHandler.setColl("a53aproxeGood_VirusCrashTime920_georgia")
#mongoHandler.setColl("a53aproxeGood_VirusCrashTime920Part2_georgia")
#mongoHandler.setColl("a53aproxeGood_VirusCrashTime920_multiplier19_georgia")
#mongoHandler.setColl("InterruptsNominalIdle30sA53ganton12500exp")
mongoHandler.setColl("a53aproxeGood_VirusCrashTime900_multiplier19_georgia")
mongoHandler.setColl("a53_georgia_VirusCrashTime900_multiplier19")
mongoHandler.setColl("a53Virus_3s_Validation_ganton12")
mongoHandler.setColl("a53_georgia_VirusCrashTime900_multiplier19_SubmitFramework")
mongoHandler.setColl("a53_georgia_VirusCrashTime900_multiplier19_SubmitFramework_FrameworkInterruptsRateTo5")
mongoHandler.setColl("a53_georgia_VirusCrashTime900_multiplier19_SubmitFrameworkPart2")
mongoHandler.setColl("a53_georgia_VirusCrashTime900_multiplier19_SubmitFrameworkInterval1")
mongoHandler.setColl("a72_georgia_Vmin_multiplier24")
#mongoHandler.setColl("a72_georgia_CrashTime_multiplier24")
mongoHandler.setColl("junoA53Ganton12VirusdidtVmin")
mongoHandler.setColl("a53aproxeGood_Virus26s_georgia_vmin")
mongoHandler.setColl("junoA53Ganton12VirusdidtVminPowerGateOff")
#mongoHandler.setColl("a53_georgia_VirusCrashTime895_multiplier19_SubmitFrameworkInterval2TimeOut3SSHCrash")
#mongoHandler.setColl("a53_georgia_VirusCrashTime890_multiplier19_SubmitFrameworkInterval2TimeOut3SSHCrash")
mongoHandler.setColl("a53_georgia_VirusCrashTime900_multiplier19_SubmitFrameworkInterval2TimeOut3SSHCrashPowerGateOff")
mongoHandler.setColl("a53_georgia_VirusCrashTime900_multiplier19_SubmitFrameworkInterval2TimeOut3PowerGateOff")
mongoHandler.setColl("a53_georgia_VirusCrashTime900_multiplier19_SubmitFrameworkInterval5TimeOut5PowerGateOff")
mongoHandler.setColl("a53CrashTimedidtVirus13s1000V_1000Exp_ganton12_FrameworkValidation")
mongoHandler.setColl("a53CrashTimedidtVirus13s900V_1000Exp_ganton12_FrameworkValidation")
mongoHandler.setColl("a53CrashTimedidtVirus26s900V_1000Exp_ganton12_FrameworkValidation")
#a53CrashTimedidtVirus13s900V_1000Exp_ganton12_FrameworkValidation
#mongoHandler.setColl("a53CrashTimedidtVirusInfinite900V_1000Exp_ganton12_FrameworkValidation")

mongoHandler.setColl("a53_georgia_VirusCrashTime900_multiplier19_SubmitFrameworkInterval5TimeOut5PowerGateOffDiagnostics")
mongoHandler.setColl("asioko01a53_virus")
mongoHandler.setColl("asioko01a53_virus_10_repetitions_f1")
#mongoHandler.setColl("asioko01a53_virus_10_repetitions_4")
#mongoHandler.setColl("asioko01a53_virus_10_repetitions_7")
#mongoHandler.setColl("asioko01a53_virus_10_repetitions_f1")
#mongoHandler.setColl("asioko01a53_virus_10_repetitions_6")
#a53CrashTimedidtVirus26s900V_1000Exp_ganton12_FrameworkValidation
#a53_georgia_VirusCrashTime900_multiplier19_SubmitFramework_shufflecorecheck
#mongoHandler.setColl("a53_georgia_VirusCrashTime900_multiplier19_SubmitFramework_rev#ersedExecution")
#mongoHandler.setColl("delethis")
#a53_georgia_VirusCrashTime900_multiplier19_SubmitFramework
#mongoHandler.setColl("a53aproxeGood_VirusCrashTime925Part2_georgia")
#mongoHandler.setColl("a53aproxeGood_Virus26s_georgia_getInterrupts")
#mongoHandler.setColl("a53aproxeGood_VirusCrashTime925_georgia")
#InterruptsNominalIdle30sA53ganton12100exp
#mongoHandler.setColl("a53ganton12VminIdle30s_goodfinal")
#mongoHandler.setColl("a53ganton12VminIdle890V30s_goodfinalgood")
#mongoHandler.setColl("a53ganton12VminIdle30s_goodfinal")
#mongoHandler.setColl("a53aproxeGood_singleCoresNoGating_3vs0")
#mongoHandler.setColl("a53aproxeGood_singleCoresNoGating_3vs1")
#mongoHandler.setColl("a53aproxeGood_singleCoresNoGating_idle")
#mongoHandler.setColl("a53aproxeGood_singleCoresNoGating_3")
#mongoHandler.setColl("a53aproxeGood_singleCoresNoGating_4")
#mongoHandler.setColl("a53aproxeGood_200exps")
#mongoHandler.setColl("a53aproxeGood_singleCoresNoGating_selfLoop_1core")#mongoHandler.setColl("a53aproxeGood_testingsdc")
#mongoHandler.setDB("test")
#mongoHandler.setColl("wse_demo")
#for doc in mongoHandler._coll.find({"system_crash":True}):
#    print(doc)

#mongoHandler.insertDoc({"testValue":1})

#for doc in mongoHandler._coll.find({"system_crash":True}):
count=0
count2=0
voltTime={}
for doc in mongoHandler._coll.find():
        count2=count2+1
        #if doc["workloads"][0]["name"]!="theVirus_2":
        #    continue
        #print(str(doc))
        for workload in doc["workloads"]:
        
            if workload["sdc"]==True:
                print("SDC " +str(doc["core_vol"])+" "+str(workload["name"])+" EXEC_TIME "+str(workload["exec_time"])+" WORKLOAD "+str(workload["cores"])+" DOC "+str(doc["_id"]))
                #print("SDC " +str(doc["core_vol"])+" "+str(workload["exec_time"]))
                '''
                if(str(doc["core_vol"]) in voltTime):
                    voltTime[str(doc["core_vol"])].append(str(workload["exec_time"]))
                else:
                    voltTime[str(doc["core_vol"])]=[]
                    voltTime[str(doc["core_vol"])].append(str(workload["exec_time"]))
                 '''   
            if workload["crash"]==True:
                print("APP_CRASH " +str(doc["core_vol"])+" "+str(workload["name"])+" EXEC_TIME "+str(workload["exec_time"])+" WORKLOAD "+str(workload["cores"])+" DOC "+str(doc["_id"]))
                '''
                if(str(doc["core_vol"]) in voltTime):
                    voltTime[str(doc["core_vol"])].append(str(workload["exec_time"]))
                else:
                    voltTime[str(doc["core_vol"])]=[]
                    voltTime[str(doc["core_vol"])].append(str(workload["exec_time"])) 
                '''               
            
            if workload["crash"]==False and (workload["sdc"]==False or workload["sdc"] is None) and doc["system_crash"]==False and (workload["bitFlip"]==False or workload["bitFlip"] is None):
                print("PASS " +str(doc["core_vol"])+" "+str(workload["name"])+" EXEC_TIME "+str(workload["exec_time"])+" WORKLOAD "+str(workload["cores"])+" DOC "+str(doc["_id"]))#+" "+str(doc["power"][0]["min_max_avg"])+" "+str(len(doc["power"][0]["values"])))
                count=count+1

            if workload["bitFlip"]==True:
                print("Bitflip " +str(doc["core_vol"])+" "+str(workload["name"])+" EXEC_TIME "+str(workload["exec_time"])+" WORKLOAD "+str(workload["cores"])+" DOC "+str(doc["_id"]))


        if doc["system_crash"]==True:
            #print("SYSTEM_CRASH "+str(doc["core_vol"])+" "+str(workload["name"])+" "+str(workload["cores"])+" "+str(doc["workloads"][0]["exec_time"]))
            print("SYSTEM_CRASH "+str(doc["core_vol"])+" "+str(doc["workloads"][0]["exec_time"]))
            
            '''
            if(str(doc["core_vol"]) in voltTime):
                voltTime[str(doc["core_vol"])].append(str(workload["exec_time"]))
            else:
                voltTime[str(doc["core_vol"])]=[]
                voltTime[str(doc["core_vol"])].append(str(workload["exec_time"]))
            '''
#for i in voltTime:
    #print(i+"    "+str(voltTime[i]).replace('[','').replace(']','').replace("\'",''))
print(str(count)+" "+str(count2))
   