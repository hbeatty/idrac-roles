# idrac/facts
Ansible role that works with the [iDRAC Ansible module](https://github.com/hbeatty/iDRAC-Ansible-module).

Gets some system information and will reset the root password.

## Tasks - tasks/main.yml

* Get System Inventory (ignore_errors)
* Reset Default Password (if Get System Inventory Failed)
* Get Firmware Info

## Variables - defaults/main.yml

```
lom_user: root
lom_pass: pass
drac_default_pass: calvin
```

## Handlers - handlers/main.yml

* Get System Inventory

## Dependencies

* [iDRAC Ansible module](https://github.com/hbeatty/iDRAC-Ansible-module)
* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.

## Example Playbook

```
- hosts: localhost
  sudo: yes
  tasks:
  - name: Install wsmancli
    yum: name=wsmancli state=present

- hosts: localhost
  sudo: yes

  roles:
  - { role: idrac/lcoal, tags: "idrac-local" }

- hosts: idracs
  gather_facts: False
  sudo: yes

  roles:
  - { role: idrac/facts, tags: [ "idrac-facts", "idrac-firmware", "idrac-storage", "idrac-os-install", "idrac-alerts" ] }
  - { role: idrac/alerts, tags: "idrac-alerts" }
  - { role: idrac/firmware, tags: "idrac-firmware" }
  - { role: idrac/storage, tags: "idrac-storage" }
  - { role: idrac/os-install, tags: "idrac-os-install" }

