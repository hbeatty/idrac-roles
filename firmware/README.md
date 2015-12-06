# idrac/firmware

Ansible role that works with the [iDRAC Ansible module](https://github.com/hbeatty/iDRAC-Ansible-module).

Upgrades firmware. 

Firmware upgrade order:  

1. iDRAC
3. BIOS
4. Diagnostics
5. OS Driver Pack
6. RAID
7. NIC
8. PSU
9. CPLD
10. Other updates

See [GenerateFirmwareVars](https://github.com/hbeatty/iDRAC-Ansible-module/tree/master/docs/GenerateFirmwareVars.md) for a head start on your group_vars/all/firmware.yml file.

## Tasks

### tasks/main.yml

```
- name: Make sure iDrac is ready
  local_action: idrac username={{lom_user}} password={{lom_pass}}
                hostname={{lom_hostname}} name="CheckReadyState"

# This one has to be run seperately because it causes an automatic reset of the 
# iDRAC
- include: idracFirmwareInstall.yml

# Run seperately because of the upgrade order
- include: biosInstall.yml

# Install the other firmware
- include: firmwareUpgrade.yml
```

### tasks/idracFirmwareInstall.yml

```
- name: Install iDRAC firmware
  local_action:
    module: idrac
    username: "{{lom_user}}"
    password: "{{lom_pass}}"
    hostname: "{{lom_hostname}}"
    name: "InstallIdracFirmware"
    firmware:
      "{{firmware[SystemGeneration].idrac}}"

- name: Check iDRAC status after upgrade
  local_action: idrac username={{lom_user}} password={{lom_pass}}
                hostname={{lom_hostname}} command="CheckReadyState"
```

### tasks/biosInstall.yml

```
- name: Install BIOS
  local_action:
    module: idrac
    username: "{{ lom_user }}"
    password: "{{ lom_pass }}"
    hostname: "{{ lom_hostname }}"
    name: "InstallBIOS"
    firmware:
      "{{firmware[SystemGeneration].bios}}"
```

### tasks/firmwareUpgrade.yml

```
- name: Upgrade Firmware
  local_action:
    module: idrac
    username: "{{ lom_user }}"
    password: "{{ lom_pass }}"
    hostname: "{{ lom_hostname }}"
    name: "UpgradeFirmware"
    reboot_type: 1
    firmware: 
      "{{ firmware[SystemGeneration] }}"
  register: result

# Give a pretty output of how the install went
- debug: var=result.result
```

## Variables - defaults/main.yml

```
lom_user: root
lom_pass: pass
```

## Example Playbook

```
- hosts: localhost
  sudo: yes
  tasks:
  - name: Install wsmancli
    yum: name=wsmancli state=present

- hosts: idracs
  gather_facts: False
  sudo: yes

  roles:
  - { role: idrac/facts, tags: [ "idrac-facts", "idrac-alerts", "idrac-firmware", "idrac-storage", "idrac-os-install" ] }
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

## Notes

iDRAC stuck? Try the link below.
http://www.dell.com/support/manuals/us/en/19/Topic/idrac8-with-lc-v2.05.05.05/LC_2.05.05.05_UG-v1/en-us/GUID-8F76747E-86F2-4242-BE3D-8BB5A88A7C0C


