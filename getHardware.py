import subprocess
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
    cmd = "wmic COmputerSystem get TotalPhysicalMemory"
    output = subprocess.check_output(cmd, shell=True, creationflags=0x08000000).decode().strip().split()
    output = int(output[1]) / 1073741824
    output = int(output + 0.5) if output >= 0 else int(output - 0.5)
    return str(output) + " GB"



