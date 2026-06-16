🖥️ Health Monitoring Script

📌 What this does

This script collects system metrics and checks them against configurable thresholds and required services.
All information is logged within a general log named healthmon.log and any metrics found to be over the
threshold are logged in both a log called alerts.log and syslog. The user also has to option to print to
screen with a <--check> flag.

📌 What this checks

Currently, this script checks the following:
* Disk usage percentage
* Memory usage percentage
* CPU 1-minute load average
* Services:
  *sshd
  *cron

📌 What this returns

Log entries that are generated following the format below:

2026-06-16 14:35:01,123 [INFO] healthmon: MEMORY_USAGE Current: 41.3 Limit: 80

---------------------------------------------------------------------
-------------------------Requirements--------------------------------
This script was developed and tested on Linux Ubuntu ver 26.04.
Modification may be required for other distributions.

Python Version 3.8+

Check version using the following within the terminal:

python3 --version

---------------------------------------------------------------------

System dependencies

The script uses standard Linux tools:

* logging
* json
* sys
* argparse

These are usually already installed.

---------------------------------------------------------------------

Python dependency

* psutil

Installation will be covered later if neccessary

---------------------------------------------------------------------
-----------------------Installation(via git)-------------------------

Recommended Setup using a Virtual Environment

1. Download this repository

    git clone --branch sprint4-healthmon https://github.com/t4styw1tch/sprint_scripts.git

2. Move into the project folder

    cd sprint_scripts
   
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

1. Go to https://github.com/t4styw1tch/sprint_scripts/tree/sprint4-healthmon
2. Click Code
3. Click Download ZIP
4. Extract the folder
5. Open terminal and run the same commands above

---------------------------------------------------------------------
-----------------Creation of Virtual Environment---------------------
1. Using a terminal, navigate to the folder where healthmon.py and config.json are located

2.(Optional) If psutil was installed in a virtual environment, activate the environment

  source venv/bin/activate

---------------------------------------------------------------------
--------------------Configuration Preparation------------------------
Due to potential differences between file systems, some modification of the config.json may
be required to output logs in the desired location.

Within config.json, alter the file path's for both log_file and alert_log as needed.

---------------------------------------------------------------------
----------------------------Execution--------------------------------

Execute the script with one of the following commands based on desired output
   
Will only log system health information:

  python3 healthmon.py config.json

Will both log information as well as print logs to CLI for viewing:

  python3 healthmon.py config.json --check

---------------------------------------------------------------------
---------------------Configuration Modification----------------------

Basic config.json format:
{
    "thresholds": {
        "disk": 80,
        "memory": 90,
        "cpu": 2.0,
        "services": ["sshd", "cron"]
    },
    "log_file": "/home/sprint_scripts/healthmon/healthmon.log",
    "alert_log": "/home/sprint_scripts/healthmon/alerts.log"
}

In order to modify the thresholds for any of these metrics,
simply replace the numbers within corresponding with which metric you want to alter.
The same applies to the services you may wish to monitor, simply add or change the
pre-existing entries within services.

---------------------------------------------------------------------
--------------------Optional- Cron Scheduling------------------------

This script is fully capable of being scheduled via cron using the following example. This
example was successful and based on having created a virtual environment for the dependencies.

*/5 * * * * /home/sprint_scripts/healthmon/venv/bin/python3 /home/sprint_scripts/healthmon/healthmon.py /home/sprint_scripts/healthmon/config.json

---------------------------------------------------------------------
--------------------------How it works-------------------------------

The script uses:

* logging → creation of loggers which can log information based on severity (INFO, WARNING)
* psutil → retrieves system information about disk usage, memory usage, cpu average, and neccessary services
* json → allows for a configurable file to be used to set thresholds, necessary services, and file paths



---------------------------------------------------------------------
-----------------------------Notes-----------------------------------

* Designed only for Linux systems with Syslog service
* Will not work on any Windows OS
* Will require modification if alternative metrics or thresholds are desired


---------------------------------------------------------------------
-----------------------------Ending----------------------------------

When done, use the following command to deactivate the virtual environment:

deactivate
