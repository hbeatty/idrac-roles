# idrac/alerts

Ansible role that works with the [iDRAC Ansible module](https://github.com/hbeatty/iDRAC-Ansible-module). Sets the values for the alerting in the iDRAC.

## Tasks - tasks/main.yml

```
- local_action: 
    module: idrac
    username: "{{ lom_user }}"
    password: "{{ lom_pass }}"
    hostname: "{{ lom_hostname }}"
    command: 'SyslogSettings'
    servers: "{{ idrac_syslog_servers }}"
  when: idrac_syslog_servers is defined
  tags:
    - idrac_syslog

- name: Turn on syslog notifications for iDRAC events
  local_action: idrac username={{lom_user}} password={{lom_pass}}
                hostname={{lom_hostname}} command="SetEventFiltersByInstanceIDs"
  when: idrac_syslog_servers is defined
  tags:
    - idrac_syslog
```

## Variables - defaults/main.yml

```
lom_user: root
lom_pass: pass

# iDRAC limitation of 3
idrac_syslog_servers:
    - 10.10.10.10
    - 10.10.10.11
    - 10.10.10.12

# Sets the sylog port to UDP 514 (iDRAC does not support TCP for syslog)
idrac_syslog_port: 514
```

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

- hosts: idracs
  gather_facts: False
  sudo: yes

  roles:
  - { role: idrac/facts, tags: [ "idrac-facts", "idrac-firmware", "idrac-storage", "idrac-os-install", "idrac-alerts" ] }
  - { role: idrac/alerts, tags: "idrac-alerts" }
  - { role: idrac/firmware, tags: "idrac-firmware" }
  - { role: idrac/storage, tags: "idrac-storage" }
  - { role: idrac/os-install, tags: "idrac-os-install" }
```

## Notes

Currently this sets the syslog servers, enables syslog to be sent, and then turns on all of the Event Filters for "Remote System Log".  

The eventual goal will be that you can pick and choose which Notifications to turn on.
