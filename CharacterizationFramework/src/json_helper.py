'''
Created on 30 ÎœÎ±Ï� 2017

@author: Sugar
'''

import json
import jsonpickle
from JSONoutputObjectDefinitions import *


def __assignDefaultInputs__(outObject):
    #outObject.platform="xgene2"
    outObject.board="UCY"
    outObject.chip="normal"
    outObject.total_dram_size=8
    
    dim_id1=dim_id()
    dim_id1.manufacturer="crucial"
    dim_id1.size=8
    dim_id1.model="CT102472BA1886D"
    dim_id1.part_number=""
    dim_ids=[]
    dim_ids.append(dim_id1)

    outObject.dim_ids=dim_ids

def generateDefaultInputs(out_file_name): #function for writting down an expOut object with some default inputs.. The output file can be automatically unboxed into a expOut object with importDefaultInputs funtion
    
    out_file=open(out_file_name,'w')
    
    outObject= expOut()
    __assignDefaultInputs__(outObject)
    frozen=jsonpickle.encode(outObject)
    
    out_file.write(frozen)

#def generateInputFile(out_file_name): #function for generating an expOut object that at the same time will bb used for input to the characterization framework.. The output file can be automatically unboxed into a expOut object with importInput funtion
    
#    out_file=open(out_file_name,'w')
    
#    outObject= expOut()
#    __assignDefaultInputs__(outObject)
#    outObject.w
#    frozen=jsonpickle.encode(outObject)
    
#    out_file.write(frozen)
    

def importInput(input_file):
    with open(input_file) as default_inputs:
        json_string=default_inputs.read().replace('\n',' ')
        #out=json.load(default_inputs)
    out=jsonpickle.decode(json_string)
    return out
    #for dim_id in out.dim_ids:
    #   print(dim_id.model)
    #print(out.dim_ids[0],)

def returnJsonAsString(json_obj):
    return(jsonpickle.encode(json_obj,unpicklable=False))

def __testJsonOutput__():
    with open("files/test") as f:
        lines = f.read().splitlines()
    
    
    jsonArray=[]
    print("[")
    for line in lines:
        #print("original line is " +line)
        newObject= expOut()
        newObject.board="UCY"
        newObject.chip="normal"
        cores=str(line).split(" ")[1]
        frequency=str(line).split(" ")[2]
        for core in str(cores).split(","):
            newObject.core_to_freq.append(int(frequency))
        newObject.core_vol=int(str(line).split(" ")[5])
        newObject.os_version="4.3.0-3.06.21+uniserver.161005.aarch64"
        newObject.soc_freq=2400
        newObject.soc_vol=980
        newObject.system_crash=True
        benchmark=str(str(line).split(" ")[7])#.split[1]
        workload_ins=workload()
        workload_ins.name=benchmark
        workload_ins.cores=cores.replace(","," ")
        workload_ins.inputs="native"
        newObject.workloads.append(workload_ins)
        frozen=jsonpickle.encode(newObject)
        print(frozen+",")
        #jsonArray.append(frozen)
    print("]")
    #frozen=jsonpickle.encode(jsonArray,unpicklable=False)
    #print(frozen)
    
#generateDefaultInputs("C:/Users/zhadji01/workspace/CharacterizationFramework/inputs/xg2_normal_1dim.json");
#importInput("C:/Users/zhadji01/workspace/CharacterizationFramework/inputs/xg2_normal_1dim.json")