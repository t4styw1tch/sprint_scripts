# sprint_scripts
ICO Spring 2026 SEC444

#Project 1 - Log Parser

This python script is designed to be used within a Linux system to read through and extract data from log files.

##Description

In its current form, this script allows you to quickly analyze auth.log files for specific parameters such as failures specifically 
with sshd connections. When ran, the script will create a csv file with the desired output to be read or used for further anaylsis.
This script is executable from within a Linux terminal and requires multiple arguements to set parameters within the script.

##Getting Started

###Dependencies

Python3 with standard library
*RE
*sys
*csv

Linux OS
*Current script tested

###Installing
Within Linux terminal, use this command to clone the repo.
*git clone https://github.com/t4styw1tch/sprint_scripts.git

###OPTIONAL- In Progress

###Execution
1. Navigate to the sprint_scripts directory
2. Copy any auth.log file that you wish to analyze into this directory
3. To run this script, use the following command and replace any <content> with your paramenters
     python3 logparser.py <input_file> <filter_1> <filter_2> <output_file.csv>

#Author
T4styw1tch - Jen

#Version History
*0.1
  Initial Release
