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
    

    cmd = "wmic cpu get name"
    output = subprocess.check_output(cmd, shell=True, creationflags=0x08000000).decode().strip().split()
    output = " ".join(output[1:])
    return output

def getGPU():
    cmd = "wmic path win32_VideoController get name"
    output = subprocess.check_output(cmd, shell=True, creationflags=0x08000000).decode().strip().split()
    output = " ".join(output[1:])
    return output

def getRAM():
    cmd = "wmic ComputerSystem get TotalPhysicalMemory"
    output = subprocess.check_output(cmd, shell=True, creationflags=0x08000000).decode().strip().split()
    output = int(output[1]) / 1073741824
    output = int(output + 0.5) if output >= 0 else int(output - 0.5)
    cmd = "wmic memorychip get speed"
    speed = subprocess.check_output(cmd, shell=True, creationflags=0x08000000).decode().strip().split()
    return str(output) + " GB @ " + str(speed[2]) + " MT/s"

def getOverallScore():
    pass

def getCPUScore():
    pass

def getGPUScore():
    pass

def getRAMScore():
    pass

def writeScores():
    pass


