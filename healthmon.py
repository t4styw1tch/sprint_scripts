#!/usr/bin/python3


#Description



#Jennira Hill - 20260529


#imports
import logging
import json
import psutil
import sys
from logging.handlers import SysLogHandler


#Functions

def main():
    config = load_config()
    system_data = pull_info(config)

def load_config():

    with open(sys.argv[1], "r") as file:
        config = json.load(file)

    return config


def pull_info(config):
    data = {}
    
    disk_usage = psutil.disk_usage('/')
    data["disk"] = disk_usage[3]

    memory_usage = psutil.virtual_memory()
    data["memory"] = memory_usage[2]
    

    cpu_usage = psutil.getloadavg()
    data["cpu"] = cpu_usage[0]
   
    for service in config["thresholds"]["services"]:
        running = any(
            service.lower() in (p.info['name'] or "").lower()
            for p in psutil.process_iter(['name'])
            )
        data[service] = "PASS" if running else "FAIL"
    
    return data

def check_threshhold(system_data, config):
    results = {}

    
    
    




#def get_logs():
 #   logger = logging.getLogger("healthmon")

  #  logger.warning("Disk at 85%")












if __name__ == "__main__":
    main()
