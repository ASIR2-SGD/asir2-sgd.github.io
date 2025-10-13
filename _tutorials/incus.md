---
layout: default
title: "Incus"

---
# Incus 
## Introducción
Incus es un software de gestión de contenedores y máquinas virtuales. Con *incus* puedes gestiónar tus instancias mediante la linea de comandos haciéndolo muy útil para el despliegue de aplicaciónes y máquinas virtuales.

## Virtual machines vs. system containers
![virtual machines vs system containers](https://linuxcontainers.org/incus/docs/main/_images/virtual-machines-vs-system-containers.svg)

## Incus commands
**Instalation**
 ```bash
$ wget -q -O - https://pkgs.zabbly.com/key.asc | gpg --show-keys --fingerprint
$ wget -O /etc/apt/keyrings/zabbly.asc https://pkgs.zabbly.com/key.asc

$ sh -c 'cat <<EOF > /etc/apt/sources.list.d/zabbly-incus-stable.sources
Enabled: yes
Types: deb
URIs: https://pkgs.zabbly.com/incus/stable
Suites: $(. /etc/os-release && echo ${VERSION_CODENAME})
Components: main
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/zabbly.asc

EOF'
 
```
 **Init setup**
 ```bash
$ sudo usermod -a -G incus-admin <user>
$ newgrp incus-admin
```
**Initial configuration**
```bash
$ incus admin init
```
 **Create instance**
```bash
$ incus image list images:
$ incus launch images:ubuntu/24.04 <instance name>
$ incus launch images:ubuntu/24.04 <instance name> --network <network>
$ incus copy <source instance> <dst instance>
```
  **List instances**
 ```bash
$ incus list -c ns4t
$ incus list -c n -f csv
``` 
 **Exec commands**
 ```bash
$ incus exec <instance> -- <command> --force-noninteractive
$ incus exec <instance> -- <command>
```
 **Global config**
 ```bash
$ incus config show
$ incus config set core.http-address :8443
$ incus config set core.dns-address <ip>
$ incus config trust list
$ incus config trust add-certificate <file>
``` 
 
 **File push**
  ```bash
$ incus file push <source path> <instance>/<path>
$ incus file push /etc/hosts foo/etc/hosts
``` 
 **Profiles**
 ```bash
$ incus profile list
$ incus profile show default
``` 
 **Network**
 ```bash
$ incus network list
$ incus network show incusbr0
$ incus network create asirnetwork \
      ipv4.address=<ip/prefix> \
      ipv6.address=none ipv4.nat=true \ 
      ipv4.dhcp.ranges = <ip-first>-<ip-last> \
      ipv4.dhcp.routes=<network>,<next-hop>, 0.0.0.0,<default_gw> 
$ incus network attach <network> <instance>
$ incus network delete <network>

``` 
 
 **Storage**
  ```bash
$ incus storage show
$ incus storage info <pool_name>
$ incus storage set <pool_name> size=<new_size>GiB
 ``` 
 **Anexo I. Links**
 * [linux containers](https://images.linuxcontainers.org/)
 
 