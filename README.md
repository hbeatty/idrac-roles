# idrac-roles
Roles for the iDRAC Ansible Module

[Facts](facts/README.md)  
[Alerts](alerts/README.md)  
[Firmware](firmware/README.md)  
[Storage](storage/README.md)  
[OS Install](os-install/README.md)  

## Setup

* Copy firmware.yml to your group_vars/all folder

All of these roles used the same variables. I recommend putting them in your inventory file or a group_vars file. The variables that are needed for a specific role have been put in defaults/main.yml and then commented out.

## Variables

```
share_user: idrac
share_pass: idrac
share_ip: 10.10.10.10
share_name: public
share_type: cifs
local_samba_path: /var/samba
local_firmware_path: "{{ local_samba_path }}/firmware"

# From the perspective of the iDRAC
remote_share_path=firmware
```
