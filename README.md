🖥️ System Info Script

📌 What this does

This script collects basic system information from a Linux machine and displays it in different formats.

It shows:

* Hostname
* Operating system
* CPU info
* RAM usage
* Disk usage
* System uptime
* Network info (IP, MAC, netmask, broadcast)

You can output the results as:

* Screen (terminal)
* CSV file
* JSON file

---------------------------------------------------------------------
-------------------------Requirements--------------------------------

Python Version 3.8+

Check version using the following within the terminal:

python3 --version

---------------------------------------------------------------------

System dependencies

The script uses standard Linux tools:

* `ip`
* `df`
* `uptime`

These are usually already installed.

---------------------------------------------------------------------

Python dependency

* psutil

Installation will be covered later if neccessary

---------------------------------------------------------------------
-----------------------Installation(via git)-------------------------

Recommended Setup using a Virtual Environment

1. Download this repository

    git clone https://github.com/t4styw1tch/sprint_scripts/sysinfo.git

2. Move into the project folder

    cd sysinfo
   
3. Create a virtual environment

    python3 -m venv venv

4. Activate it

    source venv/bin/activate

5. Install dependencies inside the environment

    python3 -m pip install psutil

6. (Optional) Confirm install

    python3 -m pip list

---------------------------------------------------------------------
----------------------Installation(via ZIP)--------------------------

1. Go to https://github.com/t4styw1tch/sprint_scripts/sysinfo
2. Click Code
3. Click Download ZIP
4. Extract the folder
5. Open terminal and run the same commands above

---------------------------------------------------------------------
-----------------Operation within Virtual Environment----------------
1. Using a terminal, navigate to the folder where sysinfo.py is located

  cd sysinfo

2.(Optional) If psutil was installed in a virtual environment, activate the environment

  source venv/bin/activate

3. Execute the script with one of the following commands based on desired output

  1. Output via screen

     python3 sysinfo.py screen

  2. Output via CSV file

     python3 sysinfo.py csv

  3. Output via JSON file

     python3 sysinfo.py json
     
---------------------------------------------------------------------
------------------------------Results--------------------------------

Output will be displayed within the terminal or created within the same folder that sysinfo.py exists as either:

output.csv
    or
output.json

Terminal Results will be displayed according to the example below:
######
Hostname: kali
OS(version) and Distribution: Linux6.18.5+kali-amd64
CPU Count: 6
Total RAM: 10.45 GB
Used RAM: 1.07 GB
Free RAM: 9.38 GB
Total Disk Space: 47G
Free Disk Space: 27G
Uptime: up 3 hours 24 minutes
IP Address: 10.0.2.15
MAC Address: 08:00:27:22:a6:61
Netmask: 255.255.255.0
Broadcast: 10.0.2.255
---------------------------------------------------------------------
--------------------------------CSV----------------------------------
CSV file results when opened will follow the same format as found above.

---------------------------------------------------------------------
-------------------------------JSON----------------------------------
Json file results when opened will be displayed according to the example below:

{
    "Hostname": "kali",
    "OS(ver) and Distro": "Linux6.18.5+kali-amd64",
    "CPU Count": 6,
    "RAM": {
        "Total RAM": "10.45 GB",
        "Used RAM": "1.08 GB",
        "Free RAM": "9.37 GB"
    },
    "Disk": {
        "Total Disk Space": "47G",
        "Free Disk Space": "27G"
    },
    "Network": {
        "IP Address": "10.0.2.15",
        "Netmask": "255.255.255.0",
        "Broadcast": "10.0.2.255",
        "MAC Address": "08:00:27:22:a6:61"
    },
    "Uptime": "up 3 hours 17 minutes"
}

---------------------------------------------------------------------
--------------------------How it works-------------------------------

The script uses:

* platform → Hostname and Operating System information
* psutil → CPU cores and RAM information
* subprocess → Executes the following Linux commands (`ip`, `df`, `uptime`)
* re → parsing network data using regex patterns to extract only information relevent to this script


---------------------------------------------------------------------
-----------------------------Notes-----------------------------------

* Designed for Linux systems
* May not work correctly on Windows without changes
* Network info depends on `ip a` output format
* If data is missing, some fields may show error text


---------------------------------------------------------------------
-----------------------------Ending----------------------------------

When done, use the following command to deactivate the virtual environment:

deactivate
