#!/usr/bin/python3


#Description
#This python script is a system health monitor that accepts a formatted json configuration
#file. That file explicitly defines the thresholds for disk usage, memory usage, average
#CPU load, and services meant to be running.

#When the script is ran, all metrics and services
#are logged into a file called healthmon.log created according to the config.json file path.

#Metrics that surpass their threshold and/or services that are not running will be logged in
#both the systems syslog and a file called alerts.log that is created according to the
#config.json file path.



#Jennira Hill - 20260529


#imports
import logging
import json
import psutil
import sys
import argparse
from logging.handlers import SysLogHandler


#Functions

def main():
    """Main orchestrator for the script. Creates dicts from info pulled from the json file
        for thresholds and from info collected via psutil for live metrics."""
    
    args = parse_arguments()
    config_data = load_config(args.config)

    if args.check:
        config_data["cli"] = "true"
        
    system_data = pull_info(config_data)
    logger = create_logger(config_data)
    check_threshold(system_data, config_data, logger)

def parse_arguments():
    """This function enables the use of the --check flag to be able to print to CLI if
        desired. Will also catch errors in input."""
        
    parser = argparse.ArgumentParser()

    parser.add_argument("config", help="Path to json config file")

    parser.add_argument("--check", action="store_true", help="Enables CLI summary")

    return parser.parse_args()

def load_config(config_file):
    """Accepts CLI argument as json configuration file and processes errors related to the
        json file should they occur. Thresholds assigned to dict called config_data."""

    try:
        with open(config_file, "r") as file:
            config_data = json.load(file)

        return config_data
        
    except FileNotFoundError:
        print(f"Error: Config file '{config_file}' not found.")
        sys.exit(1)
        
    except json.JSONDecodeError:
        print("Error: Config file contains invalid JSON.")
        sys.exit(1)

def pull_info(config_data):
    """Creates dict named system_data prior to gathering system metrics using psutil. Any
        metric alterations would go here."""
    
    system_data = {}
    
    system_data["disk_usage"] = psutil.disk_usage('/').percent
    

    system_data["memory_usage"] = psutil.virtual_memory().percent
    

    system_data["cpu_load_avg"] = psutil.getloadavg()[0]
   
    for service in config_data["services"]:
        running = any(
            service.lower() in (p.info['name'] or "").lower()
            for p in psutil.process_iter(['name'])
            )
        system_data[service] = "PASS" if running else "FAIL"
    
    return system_data

def create_logger(config_data):
    
    """This function creates the logger and the 3 handlers required by the script. INFO level
        logging sent to healthmon.log, WARNING level logging sent to alerts.log and syslog.
        If --check flag was included, INFO level logging also sent to CLI."""

    logger = logging.getLogger("healthmon")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False


    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    
    
    health_handler = logging.FileHandler(config_data["log_file"])
    health_handler.setLevel(logging.INFO)
    health_handler.setFormatter(formatter)

    alert_handler = logging.FileHandler(config_data["alert_log"])
    alert_handler.setLevel(logging.WARNING)
    alert_handler.setFormatter(formatter)

    syslog_handler = SysLogHandler(address=config_data["syslog"])
    syslog_handler.setLevel(logging.WARNING)
    syslog_handler.setFormatter(formatter)

    if config_data.get("cli") == "true":
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    
    logger.addHandler(health_handler)
    logger.addHandler(alert_handler)
    logger.addHandler(syslog_handler)


    return logger

def check_threshold(system_data, config_data, logger):
    
    """This function compares the thresholds/metrics gathered. All metrics logged in
        healthmon.log for successful script validation. Metrics beyond threshold
        logged in alerts.log and syslog."""
    
    for metric, limit in config_data["thresholds"].items():

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

    for service in config_data["services"]:

        status = system_data[service]

        if status == "PASS":
            logger.info(f"Service {service} is running.")

        else:
            logger.warning(f"Service {service} is NOT running.")
            

if __name__ == "__main__":
    main()









if __name__ == "__main__":
    main()
