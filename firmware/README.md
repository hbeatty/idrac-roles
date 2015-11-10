# idrac-firmware
Ansible role that works with the [iDRAC Ansible module](https://github.com/hbeatty/iDRAC-Ansible-module). Sets the values for the alerting in the iDRAC.

## Tasks - tasks/main.yml

* Make sure the iDRAC is ready
* Installs new iDRAC firmware
* 

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

