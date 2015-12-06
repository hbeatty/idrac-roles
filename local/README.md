# idrac/local
Ansible role that works with the [iDRAC Ansible module](https://github.com/hbeatty/iDRAC-Ansible-module).

* Installs wsmancli
* Used for downloading firmware if you are installing from a samba share.

Could probably be used for installing from NFS share but, I haven't tested. Would be interested in any updates.

This should give you an idea of how you could set things up for installing the firmware.

## Setup

* Create a lookup_plugins folder in your main Ansible tree
* Copy recursive.py from the lookup_plugins folder

## Tasks - tasks/main.yml

```
- name: Create local samba dir
  file: path={{local_samba_path}} state=directory

- name: Create firmware dir
  file: path={{local_firmware_path}} state=directory

# this uses an extra var in the firmware.yml file called 'download' see GenerateFirmwareVars for creating firmware.yml
- name: Download firmware from Dell
  get_url: url={{ item.value.download }}
    dest={{local_firmware_path}}/{{ item.value.download | basename }}
  when: item.value.download is defined
  with_recursive:
   - { name: dict, args: firmware }
   - { name: dict, args: "{{item.value}}" }

- name: Install WSMAN
  yum: name=wsmancli state=present
```

## Variables - defaults/main.yml

```
lom_user: root
lom_pass: pass

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

## Example Playbook

```
- hosts: localhost
  sudo: yes
  
  roles:
    - { role: idrac/local, tags: "idrac-local" }

- hosts: idracs
  gather_facts: False
  sudo: yes

  roles:
    - { role: idrac/facts, tags: [ "idrac-facts", "idrac-alerts", "idrac-firmware", "idrac-storage", "idrac-iso" ] }
    - { role: idrac/alerts, tags: "idrac-alerts" }
    - { role: idrac/firmware, tags: "idrac-firmware" }
    - { role: idrac/storage, tags: "idrac-storage" }
    - { role: idrac/os-install, tags: "idrac-os-install" }
```

## Dependencies

* [iDRAC Ansible module](https://github.com/hbeatty/iDRAC-Ansible-module)
* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.

