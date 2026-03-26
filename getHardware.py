import subprocess
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
    global CPU_corecount, CPU_L3Cachesize, CPU_Threadcount, CPU_AVX512, CPU_AMX
    cmd = "wmic cpu get NumberOfCores"
    output = subprocess.check_output(cmd, shell=True, creationflags=0x08000000).decode().strip().split()
    CPU_corecount = int(output[1])

    cmd = "wmic cpu get NumberOfLogicalProcessors"
    output = subprocess.check_output(cmd, shell=True, creationflags=0x08000000).decode().strip().split()
    CPU_Threadcount = int(output[1])

    
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

getCPUScore()


