import subprocess
import multiprocessing
from cpuinfo import get_cpu_info
CPU_corecount = 0
CPU_maxclockspeed = 0
CPU_L3Cachesize = 0
CPU_Threadcount = 0
CPU_AVX512 = False
CPU_AMX = False

GPU_VRAMcapacity = 0
GPU_Memspeed = 0
GPU_Membandwidth = 0
GPU_TFLOPcount = 0
GPU_TensorCorecount = 0

RAM_capacity = 0
RAM_speed = 0
RAM_Type = ""

def getCPU():
    

    cmd = "Get-CimInstance Win32_Processor | Select-Object -ExpandProperty Name"
    output = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.strip()
    return output

def getGPU():
    cmd = "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"
    output = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.strip()
    return output

def getRAM():
    cmd = "[Math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB)"
    output = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.strip()
    cmd = "Get-CimInstance Win32_PhysicalMemory | Select-Object -ExpandProperty ConfiguredClockSpeed"
    speed = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.split()
    return str(output) + " GB @ " + str(speed[0]) + " MT/s"

def getOverallScore():
    pass

def getCPUScore():
    global CPU_corecount, CPU_L3Cachesize, CPU_Threadcount, CPU_maxclockspeed, CPU_AVX512, CPU_AMX

    cmd = "(Get-CimInstance -ClassName Win32_Processor | Measure-Object -Property NumberOfCores -Sum).Sum"
    corecount = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.split()
    CPU_corecount = int(corecount[0])

    cmd = "(Get-CimInstance -ClassName Win32_Processor | Measure-Object -Property NumberOfLogicalProcessors -Sum).Sum"
    threadcount = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.split()
    CPU_Threadcount = int(threadcount[0])

    cmd = "(Get-CimInstance Win32_Processor | Select-Object Name, L3CacheSize)"
    cachesize = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.split()
    CPU_L3Cachesize = int(cachesize[-1])/1000

    cmd = "(Get-CimInstance Win32_Processor).MaxClockSpeed"
    clkspd = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.split()
    CPU_maxclockspeed = int(clkspd[0]) / 1000

    flags = get_cpu_info().get('flags', [])
    

    CPU_AVX512 = any('avx512' in flag for flag in flags)

    CPU_AMX = any('amx' in flag for flag in flags)

    score = 0
    score += min(100, max(0, ((CPU_corecount / 15) * 100))) * 0.2
    score += min(100, max(0, ((CPU_Threadcount / CPU_corecount) * 100))) * 0.03
    score += min(100, max(0, ((CPU_L3Cachesize / 64) * 100))) * 0.1
    score += min(100, max(0, ((CPU_maxclockspeed / 3.5) * 100))) * 0.07
    if CPU_AMX:
        score += 35
    if CPU_AVX512:
        score += 25
    
    return score
    
    
def updateHardware(cpu, gpu, ram):
    cpu.config(text="CPU: " + getCPU())
    gpu.config(text="GPU: " + getGPU())
    ram.config(text="RAM: " + getRAM())

def getGPUScore():
    pass

def getRAMScore():
    pass

def writeScores():
    pass

print(getCPUScore())


