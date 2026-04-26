#!/usr/bin/env python3
#This .py file is a simple log parser tha generates a csv file for easier viewing within a Linux system.
#Jennira Hill - 20260422: Initial Version

#imports
import sys, csv, re, os

#Error Processing if the incorrect number of arguements was passed to script.
if len(sys.argv) != 5:
    print("Usage: logparser.py <input_file> <filter_1> <filter_2> <output_file.csv>")
    sys.exit(1)
     
#variables
input_file = sys.argv[1]
filter_1 = sys.argv[2].lower()
filter_2 = sys.argv[3].lower()
output_file = sys.argv[4]

#constants

#Lists and Dicts
log_output = []
hits = {}

#Error Processing if the file cannot be found.
if not os.path.isfile(input_file):
    print(f"Error: '{input_file}' not found.")
    sys.exit(1)
    
def main():
    extract_data(input_file, filter_1, filter_2, log_output, hits)
    write_csv(log_output, output_file)


def extract_data(input_file, filter_1, filter_2, log_output, hits):
    """
    Opens input_file variable and only extracts data from lines with filter variables.
    Data is extracted line by line as dicts and then compiled into a list.
    Extracted data is timestamp, ip, username, and port. NOTE: Invalid user is stored as invalid user.
    """
    #Created within try statement for Error catching and Processing.
    try:
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
                    if "invalid user" in line.lower():
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
    #The following are Error Processors for the following conditions: File not found, incorrect permissions to use specified file, and any unexpected errors.
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied for '{input_file}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error reading file: {e}")
        sys.exit(1)
    return log_output



def write_csv(log_output, output_file):
    """Takes log_output variable and creates a csv file based on data and is titled with output_file variable."""
    
    with open(output_file, "w", newline="") as csv_file:
        #Creates columns based around current datapoints extracted in reader function.
        writer = csv.DictWriter(csv_file, fieldnames=["timestamp", "ip", "username", "port"])

        writer.writeheader()
        writer.writerows(log_output)





if __name__=='__main__':
    main()
