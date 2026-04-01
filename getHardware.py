import subprocess
import multiprocessing
from cpuinfo import get_cpu_info
from pynvml import *
import json
import math
data = {
    "CPU_corecount": 0, "CPU_maxclockspeed": 0, "CPU_L3Cachesize": 0,
    "CPU_Threadcount": 0, "CPU_AVX512": False, "CPU_AMX": False,
    "GPU_VRAMcapacity": 0, "GPU_Memspeed": 0, "GPU_Membandwidth": 0,
    "GPU_TensorCore": False, "RAM_capacity": 0, "RAM_speed": 0,
    "RAM_Type": 0, "TotalScore": 0
}
isScoreReady = False

with open('hardware.json', 'r') as f:
    data = json.load(f)


def getCPU():
    cmd = "Get-CimInstance Win32_Processor | Select-Object -ExpandProperty Name"
    output = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.strip()
    return output

def getGPU():
    cmd = "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"
    output = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.strip()
    return output

def getRAM():
    global data

    cmd = "[Math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB)"
    output = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.strip()
    cmd = "Get-CimInstance Win32_PhysicalMemory | Select-Object -ExpandProperty ConfiguredClockSpeed"
    speed = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.split()

    data["RAM_capacity"] = int(output)
    data["RAM_speed"] = int(speed[0])

    return str(output) + " GB @ " + str(speed[0]) + " MT/s"

def getOverallScore():
    score = 0
    score += getCPUScore() * 0.1
    score += getGPUScore() * 0.65
    score += getRAMScore() * 0.25

    return round(score)

def getCPUScore():
    global data

    cmd = "(Get-CimInstance -ClassName Win32_Processor | Measure-Object -Property NumberOfCores -Sum).Sum"
    corecount = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.split()
    data["CPU_corecount"] = int(corecount[0])

    cmd = "(Get-CimInstance -ClassName Win32_Processor | Measure-Object -Property NumberOfLogicalProcessors -Sum).Sum"
    threadcount = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.split()
    data["CPU_Threadcount"] = int(threadcount[0])

    cmd = "(Get-CimInstance Win32_Processor | Select-Object Name, L3CacheSize)"
    cachesize = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.split()
    data["CPU_L3Cachesize"] = int(cachesize[-1])/1000

    cmd = "(Get-CimInstance Win32_Processor).MaxClockSpeed"
    clkspd = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.split()
    data["CPU_maxclockspeed"] = int(clkspd[0]) / 1000

    flags = get_cpu_info().get('flags', [])
    

    data["CPU_AVX512"] = any('avx512' in flag for flag in flags)
    if not data["CPU_AVX512"]:
        data["CPU_AVX512"] = False

    data["CPU_AMX"] = any('amx' in flag for flag in flags)
    if not data["CPU_AMX"]:
        data["CPU_AMX"] = False

    score = 0
    score += min(100, max(0, ((data["CPU_corecount"] / 15) * 100))) * 0.2
    score += min(100, max(0, ((data["CPU_Threadcount"] / data["CPU_corecount"]) * 100))) * 0.03
    score += min(100, max(0, ((data["CPU_L3Cachesize"] / 64) * 100))) * 0.1
    score += min(100, max(0, ((data["CPU_maxclockspeed"] / 3.5) * 100))) * 0.07
    if data["CPU_AMX"]:
        score += 35
    if data["CPU_AVX512"]:
        score += 25
    
    return score

def getGPUScore():
    global data
    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(0)
    mx, mn = nvmlDeviceGetCudaComputeCapability(handle)
    data["GPU_TensorCore"] = mx >= 7

    mem_info = nvmlDeviceGetMemoryInfo(handle)
    data["GPU_VRAMcapacity"] = mem_info.total / 1024**3

    data["GPU_Memspeed"] = nvmlDeviceGetMaxClockInfo(handle, NVML_CLOCK_MEM)
    mult = 4
    if mx >= 9:
        mult = 2
    elif mx == 8:
        mult = 16 if mn >= 6 else 8
    elif mx == 7:
        mult = 8
    
    data["GPU_Membandwidth"] = (nvmlDeviceGetMemoryBusWidth(handle) * mult * data["GPU_Memspeed"]) / (8 * 1000)

    score = 0
    score += min(100, max(0, ((data["GPU_VRAMcapacity"] / 24) * 100))) * 0.5
    score += min(100, max(0, ((data["GPU_Membandwidth"] / 1000) * 100))) * 0.35
    score += min(100, max(0, ((data["GPU_Memspeed"] / 10501) * 100))) * 0.05
    if data["GPU_TensorCore"]:
        score += 10
    return score

def getRAMScore():
    global data
    cmd = "(Get-CimInstance Win32_PhysicalMemory).SMBIOSMemoryType"
    type = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True).stdout.split()
    data["RAM_Type"] = int(type[0])
    score = 0
    score += min(100, max(0, ((data["RAM_capacity"] / 64) * 100))) * 0.5
    score += min(100, max(0, ((data["RAM_speed"] / 6400) * 100))) * 0.4
    score += min(100, max(0, ((data["RAM_Type"]/ 34) * 100))) * 0.1
    return score

def writeScores(root, progressbar, score):
    if not data["TotalScore"]:
        data["TotalScore"] = getOverallScore()
        with open("hardware.json", "w") as file:
            json.dump(data, file, indent=4)
    score.config(text="Score: " + str(data["TotalScore"]))
    root.after(0, progressbar.destroy())

def updateHardware(cpu, gpu, ram, score, root, progress):
    cpu.config(text="CPU: " + getCPU())
    gpu.config(text="GPU: " + getGPU())
    ram.config(text="RAM: " + getRAM())
    writeScores(root, progress, score)

def hexCode(start_rgb, end_rgb, factor):
    smooth_factor = (1 - math.cos(factor * math.pi)) / 2
    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * smooth_factor)
    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * smooth_factor)
    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * smooth_factor)
    return f"#{r:02x}{g:02x}{b:02x}"

def CreateScorebar(canvas, width, height, score):
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    
    half_width = width / 2

    for x in range(width):
        if x < half_width:
            color = hexCode(RED, YELLOW, x / half_width)
        else:
            color = hexCode(YELLOW, GREEN, (x - half_width) / half_width)
        
        canvas.create_line(x, 0, x, height, fill=color)

    offset = -1
    for i in range(3):
        canvas.create_line(score + offset, 0, score + offset, height, fill="black" if score < 900 else "white")
        offset += 1
