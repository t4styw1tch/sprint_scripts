#!/usr/bin/python3
#This .py file is a simple log parser tha generates a csv file for easier viewing within a Linux system
#Jennira Hill - 20260422: Initial Version

#imports
import sys, csv, re

#variables
input_file = sys.argv[1]
filter_1 = sys.argv[2].lower()
filter_2 = sys.argv[3].lower()
output_file = sys.argv[4]

#constants

#Lists and Dicts
log_output = []
hits = {}

def extract_data(input_file, filter_1, filter_2):
    """
    Opens input_file variable and only extracts data from lines with filter variables.
    Data is extracted line by line as dicts and then compiled into a list.
    Extracted data is timestamp, ip, username, and port. NOTE: Invalid user is stored as invalid user.
    """
    
    with open(input_file) as file:
        for line in file:
            #First checks if line contains filter words before continuing with regex analysis.
            line_lower = line.lower()
            if filter_1 in line_lower and filter_2 in line_lower:
                print(line.strip())
                #Regex groups: 1-timestamp, 2-username, 3-ip address, 4- port.
                match = re.search(r"([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}).*?for (\w+).*?from (\d+\.\d+\.\d+\.\d+) port (\d+)", line)
                #Catchline in case regex matches not found to prevent breaking script.
                if not match:
                    continue
                #Organized specifically for order of information according to Sprint 1, unneccessary for future.
                timestamp = match.group(1)
                ip = match.group(3)
                username = match.group(2)
                port = match.group(4)

                #Catchline specifically for invalid user. Future requirements on capturing invalid user's username
                #will go here.
                if "invalid user" in line:
                    username = "invalid user"
                #Data saved to a dict for possible script alterations in the future. 
                hits = {
                    "timestamp": timestamp,
                    "ip": ip,
                    "username": username,
                    "port": port
                    }
                #Dicts saved to list and then returned for follow-on functions.
                log_output.append(hits)
    return log_output
                    
def write_csv(log_output, output_file):
    """Takes log_output variable and creates a csv file based on data and is titled with output_file variable."""
    
    with open(output_file, "w", newline="") as csv_file:
        #Creates columns based around current datapoints extracted in reader function.
        writer = csv.DictWriter(csv_file, fieldnames=["timestamp", "ip", "username", "port"])

        writer.writeheader()
        writer.writerows(log_output)


def main():
    extract_data(input_file, filter_1, filter_2)
    write_csv(log_output, output_file)





if __name__=='__main__':
    main()
