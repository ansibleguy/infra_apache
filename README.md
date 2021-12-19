# Apache2 Role
Ansible Role to deploy one or multiple Apache2 sites on a linux server.

**Tested:**
* Debian 11

## Functionality

* **Package installation**
  * Ansible dependencies (_minimal_)
  * Apache2


* **Configuration**
  * Support for multiple sites/servers
  * Two **config-modes**:
    * serve (_default_)
    * redirect


  * **Default config**:
    * Disabled: <TLS1.2, unsecure ciphers, autoindex, servertokens/-signature, ServerSideIncludes, CGI
    * Security headers: HSTS, X-Frame, Referrer-Policy, Content-Type nosniff, X-Domain-Policy, XXS-Protection
    * Limits to prevent DDoS
    * Logging to syslog
    * Using a Self-Signed certificate
    * Modules: +ssl, headers, rewrite; -autoindex


  * **SSL modes** (_for more info see: [CERT ROLE](https://github.com/ansibleguy/infra_certs)_)
    * **selfsigned** => Generate self-signed ones
    * **ca** => Generate a minimal Certificate Authority and certificate signed by it
    * **letsencrypt** => Uses the LetsEncrypt certbot
    * **existing** => Copy certificate files or use existing ones


  * **Default opt-ins**:
    * restricting methods to POST/GET/HEAD


  * **Default opt-outs**:
    * Include the config file 'site_{{ site_name }}_app.conf' for advanced usage


Options to provide module config will be added in the future!<br>
Also some basic mods will get a pre-config added. (_prefork, evasive_)

## Info

* **Note:** Most of this functionality can be opted in or out using the main defaults file and variables!


* **Note:** this role currently only supports debian-based systems


* **Note:** This role expects that the site's unencrypted 'server' will only redirect to its encrypted connection.


* **Note:** If you want all domain-names to get 'caught' by a site/server you need to add an underline '*' as alias or domain!<br>
This will also be done automatically if no domain is supplied.


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


* **Warning:** If you run a web application you might need to disable the 'Content-Security-Policy' header!


* **Info:** To disable default settings and headers => just set their value to: ''


## Requirements

* Community collection and certificate role: ```ansible-galaxy install -r requirements.yml```


## Usage

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
      path: '/var/www/static'

    ssl:
      mode: 'ca'  # create minimal ca with signed server-certificate

    config:
      KeepAliveTimeout: 10

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
