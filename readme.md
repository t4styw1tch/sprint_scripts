# HealthMon Server Ansible Deployment

## Overview

HealthMon is a lightweight Python-based system monitoring tool deployed and managed using Ansible. It monitors system health metrics using `psutil` and runs automatically on a schedule via a cron job.

This project demonstrates infrastructure automation, configuration management, and Linux system administration using Ansible.

---

## Features

* Automated deployment using Ansible
* Standardized hardening of a new system
* Python virtual environment isolation
* Dependency management via `requirements.txt`
* Scheduled execution using cron (every 5 minutes)
* Config-driven monitoring via `config.json`
* Runs under a dedicated non-root automation user

---

## Project Structure

```
ansible/
├── deploy.yml
├── inventory.ini
├── configure.yml
└── files/
    └── healthmon/
        ├── healthmon.py
        ├── config.json
        └── requirements.txt
```

---

## Requirements

On the Ansible control node:

* Ansible 2.9+
* SSH access to target hosts

On target hosts:

* Python 3
* sudo privileges for initial setup

---
##### WARNING ####
Before progressing, eunsure that you are able to access to the target device via SSH keys.

DISCLAIMER: The creation of an password-less user belonging to the sudo group is BAD PRACTICE and
        in its current state, the configure.yml playbook should be either edited to make the created
        user secure or have plans to secure the user.


## Ansible setup

Before running either of these playbooks, you must make modifications to the inventory.ini file for your specific environment.
Specifically, ensure you change the IP addresses for both servers to match the IP address of the desired target(s).
Also ensure that the filepath for "ansible_ssh_private_key_file" is correct.

---
## System Configuration

Run the playbook:

```bash
ansible-playbook -i inventory.ini configure.yml
```

This will:

1. Update OS and ensure rsyslog is installed and running
2. Create an SSH directory
3. Create a user "automation_user" which will later become the owner of the healthmon script
4. Disable SSH root login
5. Disable SSH password authentication
6. Set SSH protocol to more secure protocol
7. Set timezone to Pacific Daylight Time (PDT)

## Deployment

Run the playbook:

```bash
ansible-playbook -i inventory.ini deploy.yml
```

This will:

1. Install required system packages (Python, pip, venv)
2. Create `/opt/healthmon`
3. Copy application files to the target host
4. Create a Python virtual environment
5. Install dependencies from `requirements.txt`
6. Configure a cron job to run HealthMon automatically

---

## Scheduled Execution

The cron job runs every 5 minutes:

```cron
*/5 * * * * /opt/healthmon/venv/bin/python /opt/healthmon/healthmon.py /opt/healthmon/config.json
```

---

## Configuration

The `config.json` file controls monitoring thresholds and behavior.

Example:

```json
{
  "cpu_threshold": 80,
  "memory_threshold": 75,
  "disk_threshold": 85
}
```

---

## Idempotency

The playbook is idempotent:

* Re-running it will not duplicate configuration
* Files are only updated if changed
* Cron job is only created once
* Virtual environment is only created if missing

---

## Security Considerations

* Runs under non-root user where possible
* Configuration file permissions can be restricted (`0644` or stricter)
* Virtual environment isolates Python dependencies

