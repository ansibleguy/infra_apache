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

* **Note:** Most of this functionality can be opted in or out using the main defaults file and variables!


* **Note:** this role currently only supports debian-based systems


* **Note:** This role expects that the site's unencrypted 'server' will only redirect to its encrypted connection.


* **Note:** If you want all domain-names to get 'caught' by a site/server you need to add a star/wildcard '*' as alias!<br>
BUT: You still have to provide a main domain!


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


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
