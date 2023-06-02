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
from InputGenerator import activeCoresToTopology


def generateOnlySingleAndPMDs(total_cores,total_pmds,coresPerPMD):
    activeCoresToTopology=[]
    instances=Topology.getOnlyCoreAndPMDs(total_cores)
    for instance in instances:
        topology = Topology.returnTopology(instance, total_pmds, total_cores, coresPerPMD)
        toAdd = (instance,topology)
        activeCoresToTopology.append(toAdd)
    return activeCoresToTopology


def getAllpossibleTopologies(totalPmds,totalCores,coresPerPMD):
    topologies=[]
    for activeCores in range(1,totalCores+1):
            maxfpmds=activeCores//coresPerPMD
            for fpmds in range(0,maxfpmds+1):
                hpmds=activeCores-(coresPerPMD*fpmds)
                if((hpmds+fpmds)>totalPmds):
                    continue
                else: 
                    topologies.append(Topology(totalPmds,totalCores,coresPerPMD,fpmds,hpmds))
    return topologies
            
                
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
targetHostName="10.16.20.162"
targetSSHusername="root"
targetSSHpassword="root"
    
sysLogParsingScript="/home/root_desktop/chf_scripts/printErrorsWithinTimestamps"
helperScriptSetup="/home/root_desktop/chf_scripts/chf_helper_freq_taskset.sh"

workloadStatusOutput="/home/root_desktop/chf_scripts/chf_tmp/workload_status"
serialPort="COM1"
mongoDB="longTests"
mongoCol="realWorkloadUnderVolt"
measurePowerScript = "/home/root_desktop/chf_scripts/chf_measure_power.sh"
platform=4
online_offline_cores=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
repetitions=1
run_type="all"
vol_inc=10
inc_wait_time=10
vmin_component="CORE"
nominalVol=830


spec2017workloadNames=[]
spec2017workloadNames.append("perlbench_r")
spec2017workloadNames.append("mcf_r")
spec2017workloadNames.append("cactuBSSN_r")
spec2017workloadNames.append("namd_r")
spec2017workloadNames.append("parest_r")
spec2017workloadNames.append("povray_r")
spec2017workloadNames.append("lbm_r")
spec2017workloadNames.append("omnetpp_r")
spec2017workloadNames.append("wrf_r")
spec2017workloadNames.append("xalancbmk_r")
spec2017workloadNames.append("x264_r")
spec2017workloadNames.append("cam4_r")
spec2017workloadNames.append("deepsjeng_r")
spec2017workloadNames.append("imagick_r")
spec2017workloadNames.append("leela_r")
spec2017workloadNames.append("nab_r")
spec2017workloadNames.append("exchange2_r")
spec2017workloadNames.append("fotonik3d_r")
spec2017workloadNames.append("roms_r")
spec2017workloadNames.append("xz_r")

nasWorkloadNames=[]
nasWorkloadNames.append("bt.C.x")
nasWorkloadNames.append("cg.C.x")
#nasWorkloadNames.append("dc.B.x")
nasWorkloadNames.append("ep.C.x")
nasWorkloadNames.append("lu.C.x")
nasWorkloadNames.append("sp.C.x")
nasWorkloadNames.append("ua.C.x")

totalPmds=16
totalCores=32
coresPerPMD=2


knownTopologies = getAllpossibleTopologies(totalPmds, totalCores, coresPerPMD)
knownTopologies=[]

knownTopToVoltage = {}
knownInstancesToVoltage={}
with open('./xg3TopologyResults') as f:
    lines = f.readlines()
f.close()

for line in lines:
    tokens=line.strip().replace("fp"," ").replace("hp","").split(" ")
    fps=int(tokens[0])
    hps=int(tokens[1])
    newTopology=Topology(totalPmds,totalCores,coresPerPMD,fps,hps)
    knownTopToVoltage[newTopology]=int(tokens[3])+10
    knownTopologies.append(newTopology)

with open('./core_vmin.txt') as f:
    lines = f.readlines()
f.close()

core=0
for line in lines:
    vmin=int(line)+30
    knownInstancesToVoltage[tuple([core])]=vmin
    core=core+1

with open('./pmds_vmin.txt') as f:
    lines = f.readlines()
f.close()

core=0
for line in lines:
    vmin=int(line)+30
    knownInstancesToVoltage[tuple([core,core+1])]=vmin
    core=core+2

##end of ideal voltages
run_timeout=7200
helperScriptWorkload="/home/root_desktop/chf_scripts/chf_helper_spec2017_nas.sh"
#helperScriptWorkload="/home/zhadji01/chf_helper_virus.sh"

workSlotsToGenerate=350
maxWorkloadsPerSlot=1
randWorkloadChoiceMin=0
randWorkloadChoiceMax=1

rand = Random()
rand.seed(2)

#activeCoresToTopology = None
#activeCoresToTopology = generateAllInstances(totalCores,totalPmds,coresPerPMD)
#activeCoresToTopology= generateOnlySingleAndPMDs(totalCores,totalPmds,coresPerPMD)
currentCombination=0
doAllMappings=False
doOnlyCoresAndPMDs=False

jsonFileName="xg3SpecNas.json"
#END OF VARIABLES

generalInput = GeneralInput(targetHostName,targetSSHusername,targetSSHpassword,sysLogParsingScript,helperScriptSetup,helperScriptWorkload,workloadStatusOutput,serialPort,mongoDB,mongoCol,measurePowerScript)
experiments=[]

for slotID in range(workSlotsToGenerate):
    
    #choose num of cores and workloads
    numOfCores = rand.randint(1,totalCores)
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
    elif doOnlyCoresAndPMDs:
        activeCores,chosenTopology = activeCoresToTopology[currentCombination]
        currentCombination=currentCombination+1
    else:
        activeCores,chosenTopology = topologyInstanceGenerator(numOfCores)
    
   
    #set frequencies
    core_to_freq=[]
    for core in range(totalCores):
        core_to_freq.append(375)
        
    for core in activeCores:
        core_to_freq[core]=3000
        if core % 2 == 0:
            core_to_freq[core+1]=3000
        else:
            core_to_freq[core-1]=3000
    
    workloads=[]
    workloadName = None
    workloadCategory = None
    choice = rand.randint(randWorkloadChoiceMin, randWorkloadChoiceMax)
    if choice==0:
        workloadName=rand.choice(spec2017workloadNames)
        workloadCategory="SPEC2017"
        workloads.append(Workload.SPEC2017rateWorkloadGeneratorXG3(workloadName, workloadName, activeCores, "/home/root_desktop/chf_scripts/chf_tmp/0_out", "", ""))
    elif choice==1:
        workloadName=rand.choice(nasWorkloadNames)
        workloadCategory="NAS"
        workloads.append(Workload.NASworkloadGeneratorXG3(workloadName, workloadName, activeCores, "/home/root_desktop/chf_scripts/chf_tmp/0_out", "", ""))
    elif choice==2: #virus
        workloads.append(Workload.dIdTvirusWorkloadGeneratorXG3(activeCores))
                         
    startVol = knownTopToVoltage[chosenTopology]
    if chosenTopology.__eq__(Topology(totalPmds,totalCores,coresPerPMD,1,0)) or chosenTopology.__eq__(Topology(totalPmds,totalCores,coresPerPMD,0,1)):
        tmpvol = knownInstancesToVoltage[tuple(activeCores)]
        startVol = tmpvol
    endVol = startVol    
    experiment = ExperimentInput(workloads,platform,online_offline_cores,core_to_freq,repetitions,run_type,startVol,endVol,vol_inc,inc_wait_time,vmin_component,run_timeout)
    experiments.append(experiment)
    
out_file = open(jsonFileName,'w')    
inputTop = InputTop(generalInput,experiments)
frozen = jsonpickle.encode(inputTop,unpicklable=False)
out_file.write(frozen)
