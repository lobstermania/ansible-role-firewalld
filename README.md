ansible-role-firewalld
=========

Ansible role to configure firewalld zones.


Role Variables
--------------

Remove default services from the public zone:

- firewalld_remove_default_public_services: False

Default services are defined in `vars/main.yml`.

Install any additional rules:

```

firewalld_zones:
  - zone: myzone
    services:
      - https
      - http
    interfaces:
      - eth1
  - zone: myzone_2
    ports:
      - 1234-1237/tcp
    src:
      - 12.13.14.15/24

```

Note:

- An interface can only be a member of a single zone
- In order for a zone to become active, it must have either an interface or a source
- A list of available services can be found from `firewall-cmd --get-services`

Dependencies
------------

N/A

Example Playbook
----------------

```
    - hosts: servers
      become: true
      gather_facts: true
      roles:
         - { role: firewalld, tags: firewalld }
```

Author Information
------------------

@lobstermania
