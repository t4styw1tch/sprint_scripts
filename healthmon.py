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
    config_data = load_config()
    system_data = pull_info(config_data)
    check_threshold(system_data, config_data)
 #   print(config_data)
  #  print(system_data)
    

def load_config():

    with open(sys.argv[1], "r") as file:
        config_data = json.load(file)

    return config_data


def pull_info(config_data):
    system_data = {}
    
    system_data["disk_usage"] = psutil.disk_usage('/').percent
    

    system_data["memory_usage"] = psutil.virtual_memory().percent
    

    system_data["cpu_load_avg"] = psutil.getloadavg()[0]
   
    for service in config_data["thresholds"]["services"]:
        running = any(
            service.lower() in (p.info['name'] or "").lower()
            for p in psutil.process_iter(['name'])
            )
        system_data[service] = "PASS" if running else "FAIL"
    
    return system_data

def check_threshold(system_data, config_data):

    logger = logging.getLogger("healthmon")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propogate = False


    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    
    health_handler = logging.FileHandler(config_data["log_file"])
    health_handler.setLevel(logging.INFO)
    health_handler.setFormatter(formatter)

    alert_handler = logging.FileHandler(config_data["alert_log"])
    alert_handler.setLevel(logging.WARNING)
    alert_handler.setFormatter(formatter)

    #sys_handler = SysLogHandler(

    logger.addHandler(health_handler)
    logger.addHandler(alert_handler)
    
    
    for metric, limit in config_data["thresholds"].items():

        if metric == "services":
            continue

        value = system_data[metric]

        if value >= limit:
            logger.warning(
                f"{metric.upper()} threshold exceeded! "
                f"Current: {value} Limit: {limit}"
            )

        else:
            logger.info(
                f"{metric.upper()} Current: {value} Limit: {limit}"
            )
            
            










if __name__ == "__main__":
    main()
