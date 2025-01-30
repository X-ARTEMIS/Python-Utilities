import os
import platform
import psutil
import subprocess
from psutil._common import bytes2human

# Function to get basic system information
def get_system_info():
    system_info = {}
    
    # Operating System Info
    system_info['OS'] = platform.system()
    system_info['OS Version'] = platform.version()
    system_info['Machine'] = platform.machine()
    system_info['Processor'] = platform.processor()
    
    return system_info

# Function to get CPU specs
def get_cpu_info():
    cpu_info = {}
    cpu_info['CPU Cores'] = psutil.cpu_count(logical=False)
    cpu_info['Logical CPUs'] = psutil.cpu_count(logical=True)
    cpu_info['CPU Usage'] = psutil.cpu_percent(interval=1)
    
    return cpu_info

# Function to get RAM specs
def get_ram_info():
    ram_info = {}
    virtual_memory = psutil.virtual_memory()
    ram_info['Total RAM'] = bytes2human(virtual_memory.total)
    ram_info['Used RAM'] = bytes2human(virtual_memory.used)
    ram_info['Free RAM'] = bytes2human(virtual_memory.available)
    ram_info['RAM Usage'] = virtual_memory.percent
    
    return ram_info

# Function to get GPU specs
def get_gpu_info():
    gpu_info = []

    # Try to use nvidia-smi for NVIDIA GPUs (requires NVIDIA drivers to be installed)
    try:
        # Check if nvidia-smi is available
        result = subprocess.check_output("nvidia-smi --query-gpu=name,memory.total,memory.free,memory.used,temperature.gpu --format=csv,noheader,nounits", shell=True)
        result = result.decode('utf-8').strip().split('\n')

        for line in result:
            gpu_details = line.split(', ')
            gpu_info.append({
                'GPU Name': gpu_details[0],
                'GPU Memory Total': bytes2human(int(gpu_details[1]) * 1024 * 1024),  # Convert MB to bytes
                'GPU Memory Free': bytes2human(int(gpu_details[2]) * 1024 * 1024),  # Convert MB to bytes
                'GPU Memory Used': bytes2human(int(gpu_details[3]) * 1024 * 1024),  # Convert MB to bytes
                'GPU Temperature': gpu_details[4] + 'C'
            })

    except subprocess.CalledProcessError as e:
        # If nvidia-smi fails, fallback to other methods (like GPUInfo)
        pass
    
    # If no information is found, attempt to use system-specific commands
    if not gpu_info:
        try:
            # For Windows, use wmic to get GPU details
            if os.name == 'nt':
                result = subprocess.check_output("wmic path win32_videocontroller get caption, adapterram", shell=True)
                result = result.decode('utf-8').strip().split("\n")  # Corrected here
                for line in result[1:]:
                    if line.strip():
                        parts = line.split()
                        gpu_name = parts[1]  # Adjusted index for the correct output
                        gpu_memory = bytes2human(int(parts[0]))  # Convert to human-readable format
                        gpu_info.append({
                            'GPU Name': gpu_name,
                            'GPU Memory': gpu_memory
                        })
        except Exception as e:
            gpu_info.append({'Error': 'Could not retrieve GPU information'})

    if not gpu_info:
        gpu_info.append({'Error': 'No GPU detected'})
    
    return gpu_info

# Main function to display all information
def display_system_specs():
    system_info = get_system_info()
    cpu_info = get_cpu_info()
    ram_info = get_ram_info()
    gpu_info = get_gpu_info()

    print("\nSystem Information:")
    for key, value in system_info.items():
        print(f"{key}: {value}")
    
    print("\nCPU Information:")
    for key, value in cpu_info.items():
        print(f"{key}: {value}")
    
    print("\nRAM Information:")
    for key, value in ram_info.items():
        print(f"{key}: {value}")
    
    print("\nGPU Information:")
    for gpu in gpu_info:
        for key, value in gpu.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    display_system_specs()
