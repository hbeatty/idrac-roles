# idrac-roles

Roles for the [iDRAC Ansible Module](https://github.com/hbeatty/iDRAC-Ansible-module)

[Local](local/README.md)  
[Facts](facts/README.md)  
[Alerts](alerts/README.md)  
[Firmware](firmware/README.md)  
[Storage](storage/README.md)  
[OS Install](os-install/README.md)  

## Setup

1. [Generate a firmware.yml](https://github.com/hbeatty/iDRAC-Ansible-module/tree/master/docs/GenerateFirmwareVars.md)
  * This will create a <hostname>.firmware.yml for each host. You can then combine them into one and place it in your group_vars/all folder.
2. All of these roles assume you have lom_hostname set for each of the hosts you want to manage.

All of these roles use the same variables. I recommend putting them in your inventory file or a group_vars file. The variables that are needed for a specific role have been put in defaults/main.yml and then commented out.

## Variables

```
lom_user: root
lom_pass: pass
drac_default_pass: calvin

share_user: idrac
share_pass: idrac
share_ip: 10.10.10.10
share_name: public
share_type: cifs
local_samba_path: /var/samba
local_firmware_path: "{{ local_samba_path }}/firmware"

# From the perspective of the iDRAC
remote_share_path: firmware

idrac_syslog_servers:
  - 10.10.10.10
  - 10.10.10.11
  - 10.10.10.12

# Set the destination (from the perspective of the iDRAC) UDP port.
# The iDRAC is set to 514 by default. However, if someone has manually changed
# it and this is not set the task will not change it back to UDP 514.
idrac_syslog_port: 514

# Disable remote syslog for the iDRAC (defaults to true). Only needed if you
# want to turn it off
#idrac_syslog_enabled: false
```

## Dependencies

* [iDRAC Ansible module](https://github.com/hbeatty/iDRAC-Ansible-module)
* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.
