#!/usr/bin/python3


#Description
#This python Script is a simple network reconnaissance tool that combines port-scanning and IP geolocation
#lookup. Upon scan completion, the results will be both displayed within the terminal and saved to a csv file.
#Two command line arguments are neccessary to function and must be provided in the following order: IP address
#followed by an output file name.

#The scans ran will be a TCP-port scan with a range between ports 22-443 using Nmap and an external query to a
#geolocation API.


#Jennira Hill - 20260522


#imports
import nmap
import requests
import sys
import csv
import ipaddress


#Constants
PORT_START = 22
PORT_END = 443



#Functions

def main():
    """This main function makes all calls to other functions and handles the majority of errors possible within
        each function. Scan errors returned as None and handled within writer functions"""
    
    if len(sys.argv) != 3:
        print("Incorrect input. ex: python3 netrecon.py <target_ip> <output_file>")
        sys.exit(1)
            
    target_ip = sys.argv[1]
    output_file = sys.argv[2]
    #Error Handler - Invalid IP
    try:
        ipaddress.ip_address(target_ip)
    except ValueError:
        sys.exit("Invalid IP address format")
    #Error Handler - Port Scan
    try:
        scan_results = port_scanner(target_ip)
    except Exception as error:
        print(f"Port Scan error: {error} | Ensure IP is correct, reachable, and NMAP is fuctioning correctly")
        scan_results = None
    #Error Handler - Geolocation Scan
    try:
        geo_info = geolocation_scanner(target_ip)
    except Exception as error:
        print(f"Geolocation Scan error: {error} | Ensure http://ip-api.com is reachable")
        geo_info = None

    csv_writer(scan_results, geo_info, output_file)
    screen_writer(scan_results, geo_info)
        

#Scanner functions
def port_scanner(target_ip):
    """Uses Nmap library to perform TCP scan of port range defined within 'Constants'.
       Returns results as [scanner_data]"""
    
    scanner_data = {}
    
    scanner = nmap.PortScanner()

    result = scanner.scan(target_ip,
                (f"{PORT_START}-{PORT_END}"),
                arguments='-sT -Pn'
                )

    
    tcp = result.get('scan', {}) \
            .get(target_ip, {}) \
            .get('tcp', {}) 

    if not tcp:
        print("No TCP results found")
        return

    for port, data in tcp.items():
        state = data.get('state', 'unknown')
        service = data.get('name', 'unknown')

        scanner_data[port] = {
            "state": state,
            "service": service
            }

    return scanner_data


def geolocation_scanner(target_ip):
    """Uses requests library to retrieve geolocation information about the target IP from externally hosted API.
    Returns results as [geolocation_data]"""
    
    url = f"http://ip-api.com/json/{target_ip}"

    geo_scanner = requests.get(url)
    
    geo_scan = geo_scanner.json()
    
    geolocation_data = {
        "country": geo_scan.get("country", "Unknown"),
        "region": geo_scan.get("region", "Unknown"),
        "city": geo_scan.get("city", "Unknown"),
        "isp": geo_scan.get("isp", "Unknown")
        }
    return geolocation_data
    
#Writer Functions
def csv_writer(scanner_data, geolocation_data, output_file):
    """Accepts data from scanner functions, creates csv file named based off argument, and populates it with
        retrieved information. If error occurred, received information is handled as None."""
    
    with open(output_file, 'w', newline = '')as file:
        writer = csv.writer(file)

        writer.writerow(["=== Geolocation Data ==="])

        if geolocation_data is None:
            writer.writerow(["Geolocation data unavailable"])

        else:    
            writer.writerow(["Country", geolocation_data["country"]])
            writer.writerow(["Region", geolocation_data["region"]])
            writer.writerow(["City", geolocation_data["city"]])
            writer.writerow(["ISP", geolocation_data["isp"]])
            writer.writerow(["=== Port Scan Data ==="])


        if scanner_data is None:
            writer.writerow(["Port data unavailable"])

        else:
            writer.writerow(["Port", "State", "Service"])
            for port, info in scanner_data.items():
            
                writer.writerow([
                    port,
                    info["state"],
                    info["service"]
                    ])
            
def screen_writer(scanner_data, geolocation_data):
    """Accepts data from scanner functions and formats it for readability before printing to terminal.
    If error occurred, received information is handled as None."""

    print("=== Geolocation Data ===")
    if geolocation_data is None:
        print("Geolocation data unavailable")

    else:    
        print(f"Country: {geolocation_data['country']}")
        print(f"Region: {geolocation_data['region']}")
        print(f"City: {geolocation_data['city']}")
        print(f"ISP: {geolocation_data['isp']}")
        print("=== Port Scan Data ===")
    if scanner_data is None:
        print("Port data unavailable")

    else:    
        for port, info in scanner_data.items():
            print(
                f"Port: {port} | "
                f"State: {info['state']} | "
                f"Service: {info['service']}"
                )

        
if __name__ == "__main__":
    main()
