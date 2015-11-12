# idrac/storage
Ansible role that works with the [iDRAC Ansible module](https://github.com/hbeatty/iDRAC-Ansible-module).

Coming Soon.

## Tasks - tasks/main.yml

```
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
    - idrac/storage
```

## Dependencies

* [iDRAC Ansible module](https://github.com/hbeatty/iDRAC-Ansible-module)
* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.

## Notes

