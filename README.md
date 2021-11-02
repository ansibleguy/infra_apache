# Apache2 Ansible Role
Ansible role to install apache2 sites on the target server.

**Tested:**
* Debian 11

## Functionality

* Package installation
  * Ansible dependencies (_minimal_)
  * Apache2
* Configuration
  * 
  * Default opt-in:
    * 
  * Default opt-outs:
    * 
  * Default config:
    * 

## Info

* **Note:** Most of this functionality can be opted in or out using the main defaults file and variables!


* **Note:** this role currently only supports debian-based systems

## Requirements

* Community collection: ```ansible-galaxy install -r requirements.yml```


## Usage
Run the playbook:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml
```

You need to define your instances by configuring the 'mariadb' dictionary!

```yaml
apache

```

There are also some useful **tags** available:
* base => only configure basics; sites will not be touched
* sites
* config => configuration (base and instances)
* certs
