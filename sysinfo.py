#!/usr/bin/python3
#Description: This script is used to gather data about a local system and will output the hostname,
#OS info, CPU, memory disk, IP address, MAC adress, and uptime. Output is determinable by the user in either
#bash, CSV, or JSON format

#Jennira Hill - 20260501: Initial Version

#imports
import os
import subprocess
import platform
import re
import psutil
import csv
import sys
import json

#Constants

#Variables
output_format = sys.argv[1]
 

#Functions
def get_os_info():
    os_info = platform.system() + platform.release()

    return os_info
    
def get_hostname():
    hostname = platform.node()

    return hostname

def get_uptime():
    raw_uptime = subprocess.run(
        ["uptime", "-p"],
        capture_output = True,
        text = True
        )
    uptime = raw_uptime.stdout.strip()
    uptime = uptime.replace(",","")

    return uptime

def get_network_info():
    raw_ip_addr = subprocess.run(
        ["ifconfig", "-a"],
        capture_output = True,
        text = True
        )
    ip_addr = re.search(
        r"inet\s+(\d+\.\d+\.\d+\.\d+).*?netmask\s+(\d+\.\d+\.\d+\.\d+).*?broadcast\s+(\d+\.\d+\.\d+\.\d+)",
        raw_ip_addr.stdout
        )
    ip_address = (ip_addr.group(1))
    netmask = (ip_addr.group(2))
    broadcast = (ip_addr.group(3))
    network_info = (ip_address, netmask, broadcast)

    return network_info
    
def get_MAC_address():
    raw_mac_addr = subprocess.run(
        ["ifconfig", "-a"],
         capture_output = True,
         text = True
         )
    mac_addr = re.search(
        r"\s(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}",
        raw_mac_addr.stdout
        )
    mac_address = (mac_addr.group(0))

    return mac_address

def get_CPU_info():
    CPU_count = psutil.cpu_count()
    cpu_info = (CPU_count)

    return cpu_info

def get_RAM_info():
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
    result = subprocess.run(
        ["df", "-BG", "/"],
        capture_output = True,
        text = True
        )
    raw_disk_info = result.stdout.splitlines()[1]
    raw_disk_info = raw_disk_info.split()
    disk_info = (raw_disk_info[1], raw_disk_info[3])

    return disk_info

def screen_print(hostname, os_info, uptime,
                 network_info, mac_address,
                 cpu_info, ram_info, disk_info):
    print(f"Hostname: {hostname}")
    print(f"OS(version) and Distribution: {os_info}")
    print(f"CPU Count: {cpu_info}")
    print(f"Total RAM: {ram_info[0]}")
    print(f"Used RAM: {ram_info[1]}")
    print(f"Free RAM: {ram_info[2]}")
    print(f"Total Disk Space: {disk_info[0]}")
    print(f"Free Disk Space: {disk_info[1]}")
    print(f"Uptime: {uptime}")
    print(f"IP Address: {network_info[0]}")
    print(f"MAC Address: {mac_address}")
    print(f"Netmask: {network_info[1]}")
    print(f"Broadcast: {network_info[2]}")

def write_csv(hostname, os_info, uptime,
                 network_info, mac_address,
                 cpu_info, ram_info, disk_info):
    try:
        with open("output", "w", newline="") as csv_file:
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
            writer.writerow(["IP Address: " + (network_info[0])])
            writer.writerow(["MAC Address:" + mac_address])
            writer.writerow(["Netmask: " + (network_info[1])])
            writer.writerow(["Broadcast: " + (network_info[2])])
    except Exception:
        traceback.print_exc()

def write_json(hostname, os_info, uptime,
               network_info, mac_address,
               cpu_info, ram_info, disk_info):

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
                "IP Address": network_info[0],
                "Netmask": network_info[1],
                "Broadcast": network_info[2],
                "MAC Address": mac_address
            },

            "Uptime": uptime
        }

        # Write dictionary to JSON file
        with open("output.json", "w") as json_file:
            json.dump(system_data, json_file, indent=4)

    except Exception as e:
        print(f"Error writing JSON: {e}")                  
            

        
def main():
    hostname = get_hostname()
    os_info = get_os_info()
    uptime = get_uptime()
    network_info = get_network_info()
    mac_address = get_MAC_address()
    ram_info = get_RAM_info()
    disk_info = get_disk_info()
    cpu_info = get_CPU_info()
    try:
        if output_format == "screen":
            screen_print(hostname, os_info, uptime,
                 network_info, mac_address,
                 cpu_info, ram_info, disk_info)
        if output_format == "csv":
            write_csv(hostname, os_info, uptime,
                 network_info, mac_address,
                 cpu_info, ram_info, disk_info)
        if output_format == "json":
            write_json(hostname, os_info, uptime,
               network_info, mac_address,
               cpu_info, ram_info, disk_info)
            
    except Exception:
        traceback.print_exc()
            


if __name__=='__main__':
    main()



