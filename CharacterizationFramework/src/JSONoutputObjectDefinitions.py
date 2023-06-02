'''
Created on 30 ÎœÎ±Ï� 2017

@author: Sugar
'''
import jsonpickle

class expOut (object):
    def __init__(self):
        self.date=None #long
        self.slimpro_rev=None#float
        self.tianocore_rev=None#float
        self.os_version=None
        self.platform=None
        self.board=None
        self.chip=None
        self.dim_ids=None #dim_id object array
        self.total_dram_size=None #int
        self.core_to_freq=None #array of integers in MHz
        self.core_vol=None #one integer value in mV
        self.uncore_freq=None #integer in MHz
        self.uncore_vol=None #integer in mV
        self.dram_freq=None #integer in MHz
        self.dram_vol=None #integer in mV
        self.dram_refresh=None #integer in ms
        self.workload_num=None #integer
        self.workloads=None # array of workload object
        self.system_crash=None #boolean
        self.err_messages=None #intact error messages thrown by system
        self.pmd_errors=None  #array of pmd_error object
        self.pmd_l2_errors=None  # array pmd_l2_errors object
        self.l3_errors=None #array of l3_error object
        self.mcu_errors=None  #array of mcu_error objects
        self.pcie_errors=None # array of pci_error objects
        self.sata_errors=None #array of sata_error objects
        self.soc_overtemp=None #int
        self.pmd_vrd_hot=None #int
        self.dimm_vrd_hot=None #int
        self.soc_vrd_hot=None #int
        self.temperature=None #array of temperature objects
        self.power=None #array of power objects
        self.EM=None # array of freq,amp pairs
        
class dim_id (object):
    def __init__(self):
        self.manufacturer=None 
        self.size=None #int
        self.model=None 
        self.part_number=None 

class workload (object):
    def __init__(self):
        self.name=None 
        self.language=None 
        self.compiler_version=None 
        self.compiler_flags=None 
        self.type=None #singleThread or multiThread
        self.inputs=None 
        self.cores=None #array of int []
        self.phases=None #array of phase objects
        self.exec_time=None #float exec time or time error happenned
        self.sdc=None #boolean
        self.crash=None #boolean
        self.quality_metric=None #quality metric object
        self.VM=None #boolean
        self.exitCode=None #integer

        #asioko01
        self.bitFlip=None
        
class pmd_error(object):
    def __init__(self):
        self.type=None 
        self.cpu=None  #array of int cores
        self.time=None  #float How many seconds after workload start the error was recorded

class pmd_l2_error(object):
    def __init__(self):
        self.severity=None
        self.cpu=None # cpu that causes the error
        self.type=None
        self.ErrAction=None
        self.ErrGrp=None #int 
        self.ErrWay=None #int
        self.ErrSyn=None #int
        self.rtos=None
        self.time=None #float How many seconds after workload start the error was recorded        
        
        
        
class l3_error(object):
    def __init__(self):
        self.type=None
        self.ErrGrp=None #int 
        self.ErrWay=None #int
        self.ErrSet=None #int
        self.ErrSyn=None #int
        self.ErrBank=None #int
        self.time=None #float How many seconds after workload start the error was recorded 
        self.data_tag=None
        
class mcu_error(object):
    def __init__(self):
        self.dimid=None #int
        self.type=None
        self.rank_error=None#int
        self.bank_error=None#int
        self.row_error=None#int
        self.column_error=None#int
        self.time=None #float How many seconds after workload start the error was recorded 
        
class pcie_error(object):
    def __init__(self):
        self.id=None #int
        self.type=None
        self.time=None#float
        self.function=None #int
        self.device=None #int
        
class sata_error(object):
    def __init__(self):
        self.controller=None #int
        self.port=None #int
        self.type=None
        self.time=None#float
                
class temperature(object):
    def __init__(self):
        self.type=None
        self.min_max_avg=None #array of int
        self.values=[] #array of samples
        self.timestep=None #timestep between samples in seconds
        
class power(object):
    def __init__(self):
        self.type=None
        self.min_max_avg=None #array of int
        self.values=[] #array of samples
        self.timestep=None #timestep between samples in seconds
        
class quality_metric(object):
    def __init__(self):
        self.type=None #string
        self.value=None #float

class phase (object):
    def __init__(self):
        self.perf_count=None # array of perf_counter object
        
class perf_counter(object):
    def __init__(self):
        self.raw_event_id=None #cycles or raw_event_counter
        self.count=None #integer counter value
        self.cores=None #array of integer core ids
    