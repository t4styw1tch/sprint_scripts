#!/usr/bin/python3
#------------
#Description
#------------
#This script is used to gather data about a local system and will output the hostname,
#OS info, CPU, memory disk, IP address, MAC adress, and uptime. Output is determinable by the user in either
#terminal, CSV, or JSON format

#Jennira Hill - 20260501: Initial Version


#--------
#imports
#--------
import subprocess
import platform
import re
import psutil
import csv
import sys
import json

#---------------------------------
#Error Handler- Missing Arguement
#---------------------------------
if len(sys.argv) != 2:
    print("Missing Arguement... ex: python3 sysinfo.py [screen|csv|json]")
    sys.exit(1)
    
#-----------
#Paramaters
#-----------
    
#Constants
valid_formats = ["screen", "csv", "json"]

#Variables
output_format = sys.argv[1].lower()

#------------------------------ 
#Error Handler- Invalid Format
#------------------------------
if sys.argv[1].lower() not in valid_formats:
    print(f"Invalid output format: {sys.argv[1]}")
    print(f"Valid options: screen, csv, json")
    sys.exit(1)
    
#---------------------------------
#Informationg Gathering Functions
#---------------------------------
def get_os_info():
    """Uses platform library to retrieve Operating System information. Returns results as [os_info]"""
    
    os_info = platform.system() + platform.release()

    return os_info
    
def get_hostname():
    """Uses platform library to retrieve Hostname of current system. Returns results as [hostname]"""
    
    hostname = platform.node()

    return hostname

def get_uptime():
    """Uses subprocess library to execute "uptime -p" command to discover time that system has been running since boot and removes unneccessary returned values. Return results as [uptime]"""
    """Handles Errors and returns message"""
    
    try:
        raw_uptime = subprocess.run(
            ["uptime", "-p"],
            capture_output = True,
            text = True
            )
        uptime = raw_uptime.stdout.strip()
        uptime = uptime.replace(",","")

        return uptime

    #Error Handlers
    except subprocess.CalledProcessError:
        return "Unable to retrieve uptime"
    except FileNotFoundError:
        return "uptime command not found"
    
def get_network_info():
    """Uses subprocess library to execute "ip a" command to discover system networking information, filters results using regex for ip, cidr, broadcast, and mac. Returns results as dict and applied to [network_info]"""
    """Handles Errors and returns message"""
    try:
        result = subprocess.run(
            ["ip", "a"],
            capture_output=True,
            text=True,
            check=True
        )

        ip_address = None
        netmask = None
        broadcast = None
        mac_address = None

        for line in result.stdout.splitlines():

            if "inet " in line and "127.0.0.1" not in line:
                ip_match = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)", line)
                cidr_match = re.search(r"/(\d+)", line)

                if ip_match:
                    ip_address = ip_match.group(1)

                if cidr_match:
                    cidr = int(cidr_match.group(1))
                    mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
                    netmask = ".".join(str((mask >> (8 * i)) & 0xff) for i in reversed(range(4)))

            if "brd" in line:
                bcast_match = re.search(r"brd\s+(\d+\.\d+\.\d+\.\d+)", line)
                if bcast_match:
                    broadcast = bcast_match.group(1)

            if "link/ether" in line:
                mac_match = re.search(r"link/ether\s+([0-9a-fA-F:]{17})", line)
                if mac_match:
                    mac_address = mac_match.group(1)
                    
        #Error Handlers
        if not ip_address:
            ip_address = ("Error retrieving data")
        if not mac_address:
            mac_address = ("Error retrieving data")
                

        return {
            "ip": ip_address,
            "netmask": netmask,
            "broadcast": broadcast,
            "mac": mac_address
            }
    
    #Error Handlers
    except subprocess.CalledProcessError:
        return "Unable to retrieve network information"
    except FileNotFoundError:
        return "'ip' command not found"

def get_CPU_info():
    """Uses psutil library to discover CPU core count of system. Returns results as [cpu_info]"""
    
    CPU_count = psutil.cpu_count()
    cpu_info = (CPU_count)

    return cpu_info

def get_RAM_info():
    """Uses psutil library to discover RAM information: Total, used, free. Formats results in Gigabytes and returns as [ram_info]"""
    
    virtual_memory = psutil.virtual_memory()
    total_RAM = virtual_memory.total / (1024 ** 3)
    used_RAM = virtual_memory.used / (1024 ** 3)
    free_RAM = virtual_memory.available / (1024 ** 3)
    
    ram_total = (f"{total_RAM:.2f} GB")
    ram_used = (f"{used_RAM:.2f} GB")
    ram_free = (f"{free_RAM:.2f} GB")
    ram_info = (ram_total, ram_used, ram_free)

    return ram_info

def get_disk_info():
    """Uses subprocess library to execute "df -BG /" command to determine disk information of the root partition. Processes results given and returns as [disk_info]"""
    try:
        result = subprocess.run(
            ["df", "-BG", "/"],
            capture_output = True,
            text = True
            )
        raw_disk_info = result.stdout.splitlines()[1]
        raw_disk_info = raw_disk_info.split()
        disk_info = (raw_disk_info[1], raw_disk_info[3])

        return disk_info
    except Exception:
        return (None, None)
    
#-----------------
#Output Functions
#-----------------
def screen_print(hostname, os_info, uptime,
                 network_info, cpu_info, ram_info, disk_info):
    """Collects and formats information gathered before printing to terminal"""
    
    print(f"Hostname: {hostname}")
    print(f"OS(version) and Distribution: {os_info}")
    print(f"CPU Count: {cpu_info}")
    print(f"Total RAM: {ram_info[0]}")
    print(f"Used RAM: {ram_info[1]}")
    print(f"Free RAM: {ram_info[2]}")
    print(f"Total Disk Space: {disk_info[0]}")
    print(f"Free Disk Space: {disk_info[1]}")
    print(f"Uptime: {uptime}")
    print(f"IP Address: {network_info["ip"]}")
    print(f"MAC Address: {network_info["mac"]}")
    print(f"Netmask: {network_info["netmask"]}")
    print(f"Broadcast: {network_info["broadcast"]}")

def write_csv(hostname, os_info, uptime,
                 network_info, cpu_info, ram_info, disk_info):
    """Attempts creation of csv file, formats information gathered, and writes information to file"""
    
    try:
        with open("output.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            
            writer.writerow(["Hostname: " + hostname])
            writer.writerow(["OS(ver) and Distro: " + os_info])
            writer.writerow(["CPU Count: " + str(cpu_info)])
            writer.writerow(["Total RAM: " + (ram_info[0])])
            writer.writerow(["Used RAM: " + (ram_info[1])])
            writer.writerow(["Free RAM: " + (ram_info[2])])
            writer.writerow(["Total Disk Space: " + (disk_info[0])])
            writer.writerow(["Free Disk Space: " + (disk_info[1])])
            writer.writerow(["Uptime: " + uptime])
            writer.writerow(["IP Address: " + (network_info["ip"])])
            writer.writerow(["MAC Address: " + (network_info["mac"])])
            writer.writerow(["Netmask: " + (network_info["netmask"])])
            writer.writerow(["Broadcast: " + (network_info["broadcast"])])
            
    #Error Handler        
    except Exception as e:
        print(f"Error writing CSV: {e}")

def write_json(hostname, os_info, uptime,
               network_info, cpu_info, ram_info, disk_info):
    """First formats and stores information in nested dicts within [system_data], attempts to create json file, then dumps [system_data] into file"""

    try:
        # Store data in a dictionary
        system_data = {
            "Hostname": hostname,
            "OS(ver) and Distro": os_info,
            "CPU Count": cpu_info,

            "RAM": {
                "Total RAM": ram_info[0],
                "Used RAM": ram_info[1],
                "Free RAM": ram_info[2]
            },

            "Disk": {
                "Total Disk Space": disk_info[0],
                "Free Disk Space": disk_info[1]
            },

            "Network": {
                "IP Address": network_info["ip"],
                "Netmask": network_info["netmask"],
                "Broadcast": network_info["broadcast"],
                "MAC Address": network_info["mac"]
            },

            "Uptime": uptime
        }

        # Write dictionary to JSON file
        with open("output.json", "w") as json_file:
            json.dump(system_data, json_file, indent=4)

    except Exception as e:
        print(f"Error writing JSON: {e}")                  
            
#--------------
#Main Function
#--------------
def main():
    """Orchestrates Information Gathering functions by using them to write variables to be referenced by output functions"""
    hostname = get_hostname()
    os_info = get_os_info()
    uptime = get_uptime()
    network_info = get_network_info()
    ram_info = get_RAM_info()
    disk_info = get_disk_info()
    cpu_info = get_CPU_info()
    if output_format == "screen":
        screen_print(hostname, os_info, uptime,
            network_info, cpu_info, ram_info, disk_info)
    elif output_format == "csv":
        write_csv(hostname, os_info, uptime,
            network_info, cpu_info, ram_info, disk_info)
    elif output_format == "json":
        write_json(hostname, os_info, uptime,
            network_info, cpu_info, ram_info, disk_info)

            


if __name__=='__main__':
    main()



