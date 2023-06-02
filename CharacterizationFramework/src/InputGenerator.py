'''
Created on 12 Φεβ 2019

@author: admin
'''
import jsonpickle
from InputTop import InputTop
from GeneralInput import GeneralInput
from ExperimentInput import ExperimentInput
from Workload import Workload
from Topology import Topology
from random import Random

def returnRandomTopologyInstance():
    chosenTopology = rand.choice(knownTopologies)
    activeCores = chosenTopology.randomPickCores(rand)
    return activeCores,chosenTopology

def topologyInstanceGenerator(numOfCores):
    ##choose topology
    chosenTopology = None
    canditateTopologies = []
    for top in knownTopologies:
        if top.activeCores() == numOfCores:
            canditateTopologies.append(top)
    chosenTopology = rand.choice(canditateTopologies)
    activeCores = chosenTopology.randomPickCores(rand)
    return activeCores,chosenTopology

def generateAllInstances(total_cores,total_pmds,coresPerPMD):
    activeCoresToTopology=[]
    instances=Topology.getAllInstancesStatic(total_cores, total_pmds, coresPerPMD)
    for instance in instances:
        topology = Topology.returnTopology(instance, total_pmds, total_cores, coresPerPMD)
        toAdd = (instance,topology)
        activeCoresToTopology.append(toAdd)
    return activeCoresToTopology
#def getAllTopol

#TODO
'''
test chf_helper_spec2017_nas script
'''
#end of TODO

##VARIABLES
targetHostName="10.16.20.161"
targetSSHusername="root"
targetSSHpassword="root"
    
sysLogParsingScript="/home/zhadji01/printErrorsWithinTimestamps"
helperScriptSetup="/home/zhadji01/chf_helper_freq_taskset.sh"

workloadStatusOutput="/ssd/zhadji01/chf_tmp/workload_status"
serialPort="COM1"
mongoDB="longTests"
mongoCol="idealNasSpec_withPMDpower"
measurePowerScript = "/home/zhadji01/chf_measure_power.sh"
platform=2
online_offline_cores=[1,1,1,1,1,1,1,1]
repetitions=1
run_type="all"
vol_inc=10
inc_wait_time=10
vmin_component="CORE"


spec2017workloadNames=[]
#spec2017workloadNames.append("perlbench_r")
#spec2017workloadNames.append("mcf_r")
#spec2017workloadNames.append("cactuBSSN_r")
spec2017workloadNames.append("namd_r")
#spec2017workloadNames.append("parest_r")
#spec2017workloadNames.append("povray_r")
#spec2017workloadNames.append("lbm_r")
#spec2017workloadNames.append("omnetpp_r")
#spec2017workloadNames.append("wrf_r")
#spec2017workloadNames.append("xalancbmk_r")
spec2017workloadNames.append("x264_r")
#spec2017workloadNames.append("cam4_r")
spec2017workloadNames.append("deepsjeng_r")
spec2017workloadNames.append("imagick_r")
spec2017workloadNames.append("leela_r")
spec2017workloadNames.append("nab_r")
#spec2017workloadNames.append("exchange2_r")
#spec2017workloadNames.append("fotonik3d_r")
#spec2017workloadNames.append("roms_r")
spec2017workloadNames.append("xz_r")

nasWorkloadNames=[]
#nasWorkloadNames.append("bt.C.x")
nasWorkloadNames.append("cg.C.x")
#nasWorkloadNames.append("dc.B.x")
nasWorkloadNames.append("ep.C.x")
nasWorkloadNames.append("lu.C.x")
nasWorkloadNames.append("sp.C.x")
nasWorkloadNames.append("ua.C.x")

totalPmds=4
totalCores=8
coresPerPMD=2


knownTopologies = []
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,1,0))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,0,1))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,0,2))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,0,3))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,1,1))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,0,4))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,2,0))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,1,2))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,2,1))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,1,3))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,3,0))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,2,2))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,3,1))
knownTopologies.append(Topology(totalPmds,totalCores,coresPerPMD,4,0))

knownTopToVoltage = {}
knownInstancesToVoltage={}

'''
#nominal
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,0)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,1)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,2)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,3)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,1)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,4)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,2,0)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,2)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,2,1)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,3)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,3,0)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,2,2)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,3,1)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,4,0)]=980

knownInstancesToVoltage[list(0)]=980
knownInstancesToVoltage[list(1)]=980
knownInstancesToVoltage[list(2)]=980
knownInstancesToVoltage[list(3)]=980
knownInstancesToVoltage[list(4)]=980
knownInstancesToVoltage[list(5)]=980
knownInstancesToVoltage[list(6)]=980
knownInstancesToVoltage[list(7)]=980
knownInstancesToVoltage[list(0,1)]=980
knownInstancesToVoltage[list(2,3)]=980
knownInstancesToVoltage[list(4,5)]=980
knownInstancesToVoltage[list(6,7)]=980
#end of not nominal
'''

#not ideal voltages
'''
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,0)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,1)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,2)]=890
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,3)]=900
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,1)]=900
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,4)]=910
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,2,0)]=910
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,2)]=910
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,2,1)]=920
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,3)]=910
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,3,0)]=920
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,2,2)]=920
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,3,1)]=930
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,4,0)]=940

knownInstancesToVoltage[tuple([0])]=890
knownInstancesToVoltage[tuple([1])]=890
knownInstancesToVoltage[tuple([2])]=890
knownInstancesToVoltage[tuple([3])]=880
knownInstancesToVoltage[tuple([4])]=890
knownInstancesToVoltage[tuple([5])]=890
knownInstancesToVoltage[tuple([6])]=880
knownInstancesToVoltage[tuple([7])]=880
knownInstancesToVoltage[tuple([0,1])]=890
knownInstancesToVoltage[tuple([2,3])]=900
knownInstancesToVoltage[tuple([4,5])]=890
knownInstancesToVoltage[tuple([6,7])]=890
##end of not ideal voltages
'''

'''
#not ideal voltages +10
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,0)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,1)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,2)]=900
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,3)]=910
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,1)]=910
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,4)]=920
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,2,0)]=920
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,2)]=920
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,2,1)]=930
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,3)]=920
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,3,0)]=930
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,2,2)]=930
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,3,1)]=940
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,4,0)]=950

knownInstancesToVoltage[tuple([0])]=900
knownInstancesToVoltage[tuple([1])]=900
knownInstancesToVoltage[tuple([2])]=900
knownInstancesToVoltage[tuple([3])]=890
knownInstancesToVoltage[tuple([4])]=900
knownInstancesToVoltage[tuple([5])]=900
knownInstancesToVoltage[tuple([6])]=890
knownInstancesToVoltage[tuple([7])]=890
knownInstancesToVoltage[tuple([0,1])]=900
knownInstancesToVoltage[tuple([2,3])]=910
knownInstancesToVoltage[tuple([4,5])]=900
knownInstancesToVoltage[tuple([6,7])]=900
##end of not ideal voltages +10
'''


#ideal voltages
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,0)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,1)]=980
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,2)]=910
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,3)]=920
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,1)]=920
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,0,4)]=930
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,2,0)]=930
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,2)]=930
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,2,1)]=950
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,1,3)]=940
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,3,0)]=940
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,2,2)]=950
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,3,1)]=950
knownTopToVoltage[Topology(totalPmds,totalCores,coresPerPMD,4,0)]=970

knownInstancesToVoltage[tuple([0])]=900
knownInstancesToVoltage[tuple([1])]=910
knownInstancesToVoltage[tuple([2])]=900
knownInstancesToVoltage[tuple([3])]=900
knownInstancesToVoltage[tuple([4])]=900
knownInstancesToVoltage[tuple([5])]=900
knownInstancesToVoltage[tuple([6])]=910
knownInstancesToVoltage[tuple([7])]=910
knownInstancesToVoltage[tuple([0,1])]=910
knownInstancesToVoltage[tuple([2,3])]=910
knownInstancesToVoltage[tuple([4,5])]=910
knownInstancesToVoltage[tuple([6,7])]=910

##end of ideal voltages
run_timeout=7200
helperScriptWorkload="/home/zhadji01/chf_helper_spec2017_nas.sh"
#helperScriptWorkload="/home/zhadji01/chf_helper_virus.sh"

workSlotsToGenerate=200
maxWorkloadsPerSlot=1
randWorkloadChoiceMin=0
randWorkloadChoiceMax=1

rand = Random()
rand.seed(3)


activeCoresToTopology = generateAllInstances(totalCores,totalPmds,coresPerPMD)
currentCombination=0
doAllMappings=False
oneNomOneUnderVolt=True
nominalVol=980

jsonFileName="Seastemp.json"
#END OF VARIABLES

generalInput = GeneralInput(targetHostName,targetSSHusername,targetSSHpassword,sysLogParsingScript,helperScriptSetup,helperScriptWorkload,workloadStatusOutput,serialPort,mongoDB,mongoCol,measurePowerScript)
experiments=[]

for slotID in range(workSlotsToGenerate):
    
    #choose num of cores and workloads
    numOfCores = rand.randint(1,totalCores) #needed for topology instance generator function
    numOfWorkloads = 1
    if numOfCores > 1:
        numOfWorkloads = rand.randint(1,maxWorkloadsPerSlot)  ##TODO need an extension here for different number of workloads
    
    activeCores=None
    chosenTopology=None
   
    ##topology instance generator
    if doAllMappings:
        #the below is for testing all possible topology instances
        activeCores,chosenTopology = activeCoresToTopology[currentCombination] 
        currentCombination=currentCombination+1
    else:
        #activeCores,chosenTopology = topologyInstanceGenerator(numOfCores)
        activeCores,chosenTopology=returnRandomTopologyInstance()
    
   
    #set frequencies
    core_to_freq=[]
    for core in range(totalCores):
        core_to_freq.append(300)
        
    for core in activeCores:
        core_to_freq[core]=2400
        if core % 2 == 0:
            core_to_freq[core+1]=2400
        else:
            core_to_freq[core-1]=2400
    
    workloads=[]
    workloadName = None
    workloadCategory = None
    choice = rand.randint(randWorkloadChoiceMin, randWorkloadChoiceMax)
    if (choice==1 and len(activeCores)<4):
        choice=0
    if choice==0:
        workloadName=rand.choice(spec2017workloadNames)
        workloadCategory="SPEC2017"
        workloads.append(Workload.SPEC2017rateWorkloadGenerator(workloadName, workloadName, activeCores, "/ssd/zhadji01/chf_tmp/0_out", "", ""))
    elif choice==1:
        workloadName=rand.choice(nasWorkloadNames)
        workloadCategory="NAS"
        workloads.append(Workload.NASworkloadGenerator(workloadName, workloadName, activeCores, "/ssd/zhadji01/chf_tmp/0_out", "", ""))
    elif choice==2: #virus
        workloads.append(Workload.dIdTvirusWorkloadGenerator(activeCores))
                         
    startVol = knownTopToVoltage[chosenTopology]
    if chosenTopology.__eq__(Topology(totalPmds,totalCores,coresPerPMD,1,0)) or chosenTopology.__eq__(Topology(totalPmds,totalCores,coresPerPMD,0,1)):
        tmpvol = knownInstancesToVoltage[tuple(activeCores)]
        startVol = tmpvol
    endVol = startVol    
                                                                                                 
    experiment = ExperimentInput(workloads,platform,online_offline_cores,core_to_freq,repetitions,run_type,startVol,endVol,vol_inc,inc_wait_time,vmin_component,run_timeout)
    experiments.append(experiment)
    if oneNomOneUnderVolt:
        experiment = ExperimentInput(workloads,platform,online_offline_cores,core_to_freq,repetitions,run_type,nominalVol,nominalVol,vol_inc,inc_wait_time,vmin_component,run_timeout)
        experiments.append(experiment)
        
out_file = open(jsonFileName,'w')    
inputTop = InputTop(generalInput,experiments)
frozen = jsonpickle.encode(inputTop,unpicklable=False)
out_file.write(frozen)
