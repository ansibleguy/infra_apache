[![Apache2](https://www.apache.org/logos/res/httpd/default.png)](https://httpd.apache.org/)

# Ansible Role - Apache2 Webserver

Ansible Role to deploy one or multiple Apache2 sites on a linux server.

<a href='https://ko-fi.com/ansible0guy' target='_blank'><img height='35' style='border:0px;height:46px;' src='https://az743702.vo.msecnd.net/cdn/kofi3.png?v=0' border='0' alt='Buy me a coffee' />

[![Molecule Test Status](https://badges.ansibleguy.net/infra_apache.molecule.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/molecule.sh.j2)
[![YamlLint Test Status](https://badges.ansibleguy.net/infra_apache.yamllint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/yamllint.sh.j2)
[![PyLint Test Status](https://badges.ansibleguy.net/infra_apache.pylint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/pylint.sh.j2)
[![Ansible-Lint Test Status](https://badges.ansibleguy.net/infra_apache.ansiblelint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/ansiblelint.sh.j2)
[![Ansible Galaxy](https://badges.ansibleguy.net/galaxy.badge.svg)](https://galaxy.ansible.com/ui/standalone/roles/ansibleguy/infra_apache)

Molecule Logs: [Short](https://badges.ansibleguy.net/log/molecule_infra_apache_test_short.log), [Full](https://badges.ansibleguy.net/log/molecule_infra_apache_test.log)

**Tested:**
* Debian 11

## Install

```bash
# latest
ansible-galaxy role install git+https://github.com/ansibleguy/infra_apache

# from galaxy
ansible-galaxy install ansibleguy.infra_apache

# or to custom role-path
ansible-galaxy install ansibleguy.infra_apache --roles-path ./roles

# install dependencies
ansible-galaxy install -r requirements.yml
```

## Functionality

* **Package installation**
  * Ansible dependencies (_minimal_)
  * Apache2


* **Configuration**
  * Support for multiple sites/servers
  * Two **config-modes**:
    * serve (_default_)
    * redirect
  * Support for specific configurations using the 'config' and 'config_additions' parameters


  * **Default config**:
    * Disabled: <TLS1.2, unsecure ciphers, autoindex, servertokens/-signature, ServerSideIncludes, CGI
    * Security headers: HSTS, X-Frame, Referrer-Policy, Content-Type nosniff, X-Domain-Policy, XXS-Protection
    * Limits to prevent DDoS
    * Using a Self-Signed certificate
    * Modules: +ssl, +http2, headers, rewrite; -autoindex
    * HTTP2 enabled with fallback to HTTP1.1
    * IPv6 support disabled (*at least one ipv6 address MUST EXIST*)


  * **SSL modes** (_for more info see: [CERT ROLE](https://github.com/ansibleguy/infra_certs)_)
    * **selfsigned** => Generate self-signed ones
    * **ca** => Generate a minimal Certificate Authority and certificate signed by it
    * **letsencrypt** => Uses the LetsEncrypt certbot
    * **existing** => Copy certificate files or use existing ones


  * **Default opt-ins**:
    * restricting methods to POST/GET/HEAD
    * status-page listener on localhost
    * Logging to syslog
    * http2


  * **Default opt-outs**:
    * Include the config file 'sites-available/site_{{ site_name }}_app.conf' for advanced usage


Options to provide module config will be added in the future!<br>
Also some basic mods will get a pre-config added. (_prefork, evasive_)

## Info

* **Note:** Most of the role's functionality can be opted in or out.

  For all available options - see the default-config located in the main/site defaults-file!


* **Note:** this role currently only supports debian-based systems


* **Note:** This role expects that the site's unencrypted 'server' will only redirect to its encrypted connection.


* **Note:** If you want any requested domain to get handled by a site/server you need to add a **wildcard** '*' as alias!<br>

   BUT: You still have to provide a main domain!


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


* **Info:** To disable default settings and headers => just set their value to: ''


* **Info:** For LetsEncrypt renewal to work, you must allow outgoing connections to:

  80/tcp, 443/tcp+udp to acme-v02.api.letsencrypt.org, staging-v02.api.letsencrypt.org (_debug mode_) and r3.o.lencr.org


## Usage

You want a simple Ansible GUI? Check-out my [Ansible WebUI](https://github.com/ansibleguy/webui)

### Config

Define the apache dictionary as needed!

```yaml
apache:
  headers:
    mySuperCustom: 'headerContent'

  modules:
    present: ['evasive', 'ssl', 'headers', 'rewrite']

  guys_statics:
    mode: 'serve'
    domain: 'static.guy.net'
    serve:
      path: '/var/www/site_guys_statics'

    ssl:
      mode: 'ca'  # create minimal ca with signed server-certificate

    config:  # add settings as key-value pairs
      KeepAliveTimeout: 10
    config_additions:   # add a list of custom lines of config
      - 'location = / { return 301 /kitty.jpg; }'

  git_stuff:
    mode: 'redirect'
    domain: 'ansibleguy.net'
    aliases: ['www.ansibleguy.net']
    redirect:
      target: 'https://github.com/ansibleguy'

    ssl:
      mode: 'letsencrypt'

    letsencrypt:
      email: 'apache@template.ansibleguy.net'

    security:
      restrict_methods: false
```

### Execution

Run the playbook:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml
```

There are also some useful **tags** available:
* base => only configure basics; sites will not be touched
* sites
* config => configuration (base and instances)
* certs

To debug errors - you can set the 'debug' variable at runtime:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml -e debug=yes
```
