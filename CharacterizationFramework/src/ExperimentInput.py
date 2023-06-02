'''
Created on 12 Φεβ 2019

@author: admin
'''

class ExperimentInput:
    def __init__(self,workloads,platform,online_offline_cores,core_to_freq,repetitions,run_type,start_voltage,end_voltage,vol_inc,inc_wait_time,vmin_component,run_timeout):
        self.workloads=workloads
        self.platform=platform
        self.online_offline_cores=online_offline_cores
        self.core_to_freq=core_to_freq
        self.repetitions=repetitions
        self.run_type=run_type
        self.start_voltage=start_voltage
        self.end_voltage=end_voltage
        self.vol_inc=vol_inc
        self.inc_wait_time=inc_wait_time
        self.vmin_component=vmin_component
        self.run_timeout=run_timeout

    

'''"experiments":[          
        {
            "workloads":[
                {
                    "work_dir":"/home/zhadji01/xg2DiDtViruses/",
                    "cmd_line":"./tester.sh ./64multiplyStack/theVirus theVirus 300 0,1,2,4,6",
                    "toKillName":"theVirus",
                    "conventionName":"theVirus_01246",
                    "cores":[0,1,2,4,6],
                    "originalOutput":null,
                    "type":"singleThread",
                    "runOutput":"/ssd/zhadji01/chf_tmp/6_out",
                    "inputs":"ref",
                    "VM":false,
                    "stdin":null
                }
            ],          
            "platform":2,  "online_offline_cores":[1,1,1,1,1,1,1,1],
            "core_to_freq":[2400,2400,2400,2400,2400,2400,2400,2400],
            "repetitions":1,
            "run_type":"all",
            "start_voltage":900,
            "end_voltage":870,
            "vol_inc":10,
            "inc_wait_time":10, "vmin_component":"CORE","run_timeout":420
        }        
    ]'''