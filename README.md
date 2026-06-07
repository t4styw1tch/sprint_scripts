🖥️ Network Reconnaisaance Script

📌 What this does

This script accepts an IP address and an output file name before performing a TCP port scan using Nmap to discover any open ports along with using an external API to collect geolocational 
data about the IP. After the information is collected, the script will create and populate a CSV file with the information as well as print the information to the terminal screen.

It shows:

* Country
* Region
* City
* Internet Service Provider
* Open port information
  * Port number
  * Service association

Output results as:

* Screen (terminal)
* CSV file

---------------------------------------------------------------------
--------------------------DISCLAIMER---------------------------------

As a legal disclaimer and general knowledge:
Unauthorized network scanning, port scanning, or security testing of systems you do not own or have explicit permission to test may be illegal and could result in criminal prosecution
under the Computer Fraud and Abuse Act (CFAA) or other equivalent laws in other jurisdictions.

As a tool:
The full functionality of this tool is only viable if a publically available IP address is used. Limited or no geographic information may be retrieved from private IP addresses. This tool
also only retrieves open port information and will not provide information about any closed ports.

---------------------------------------------------------------------
-------------------------Requirements--------------------------------

Python Version 3.8+

  *Check version using the following within the terminal:

  *python3 --version

Nmap 7.8+

  *Check version using the following within the terminal:

  *nmap --version

---------------------------------------------------------------------

Python libraries

Native
* sys
* csv
* ipaddress

Requires installation
* nmap
* requests

Installation will be covered later if neccessary

---------------------------------------------------------------------
-----------------------Installation(via git)-------------------------

Recommended Setup using a Virtual Environment

1. Download this repository

git clone --branch sprint3-netrecon https://github.com/t4styw1tch/sprint_scripts.git

2. Move into the project folder

    cd sprint_scripts
   
3. (Optional) Create a virtual environment

    python3 -m venv venv

4. (Optional) Activate it

    source venv/bin/activate

5. Install dependencies

    pip install -r requirements.txt

7. (Optional) Confirm install

    python3 -m pip list

---------------------------------------------------------------------
----------------------Installation(via ZIP)--------------------------

1. Go to https://github.com/t4styw1tch/sprint_scripts/tree/sprint3-netrecon
2. Click Code
3. Click Download ZIP
4. Extract the folder
5. Open terminal and run the same commands above

---------------------------------------------------------------------
-----------------Operation within Virtual Environment----------------
1. Using a terminal, navigate to the folder where netrecon.py is located

  cd sprint_scripts

2.(Optional) If python dependencies were installed in a virtual environment, activate the environment

  source venv/bin/activate

3. Execute the script using a public IP address and desired output file name

  python3 netrecon.py <Ip address> <output file name>
     
---------------------------------------------------------------------
------------------------------Results--------------------------------

Output will be displayed within the terminal or created within the same folder that netrecon.py exists.


Terminal Results will be displayed according to the example below:
######
=== Geolocation Data ===
Country: <United States>
Region: <WA>
City: <Seattle>
ISP: Comcast Cable Communications
=== Port Scan Data ===
Port: <###> | State: open | Service: <##########>

---------------------------------------------------------------------
--------------------------------CSV----------------------------------
CSV file results when opened will follow the same format as found above.


---------------------------------------------------------------------
--------------------------How it works-------------------------------

The script uses:

* nmap → Runs a TCP Port scan and retrieves only open port information
* requests → Reaches out to an external API and retrieves geolocational data about the IP address


---------------------------------------------------------------------
-----------------------------Notes-----------------------------------

* Designed for Linux systems
* May not work correctly on Windows without changes
* If data is missing, some fields may show error text


---------------------------------------------------------------------
-----------------------------Ending----------------------------------

When done, use the following command to deactivate the virtual environment:

deactivate
