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
### Instalation
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
  ### Init setup
```bash
$ sudo usermod -a -G incus-admin <user>
$ newgrp incus-admin
```
### Initial configuration
```bash
$ incus admin init
```
 ### Create instance
```bash
$ incus image list images:
$ incus launch images:ubuntu/24.04 <instance name>
$ incus launch images:ubuntu/24.04 <instance name> --network <network>
$incus launch images:ubuntu/noble host1 --storage <pool> --device root,size=40GiB

$ incus launch --vm images:ubuntu/noble/desktop desktop -c limits.memory=3GiB -c limits.cpu=4 --console=vga
$ incus copy <source instance> <dst instance>


```
  ### List instances
 ```bash
$ incus list -c ns4t
$ incus list -c n -f csv
``` 
 ### Exec commands
 ```bash
$ incus exec <instance> -- <command> --force-noninteractive
$ incus exec <instance> -- <command>
```
 ### Global config
 ```bash
$ incus config show
$ incus config set core.http-address :8443
$ incus config set core.dns-address <ip>
$ incus config trust list
$ incus config trust add-certificate <file>
``` 
 
 ### File push
  ```bash
$ incus file push <source path> <instance>/<path>
$ incus file push /etc/hosts foo/etc/hosts
$ incus file push <source file> <instance>/<path> --gid 1001 --uid 1001

``` 
 ### Profiles
 ```bash
$ incus profile list
$ incus profile show default
$ incus profile at
``` 
 ### Network
 #### Managed bridged network
> [!NOTE]
> Incus `managed bridged network` crea una subred para cada máquina virtual, la ip la obtiene de un servidor DHCP que crea para dicho segmento.
---
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

 #### Unmanaged bridged network (using `nmcli` (NetworkManager))
>[!NOTE]
> Incus `unmanaged bridged network` necesita de configuración adicional en el _host_ (crear un bridge). obtiene la IP de la LAN donde se encuentra el _host_
 
* Create bridge
	 ```bash
	 $ nmcli con show
	 $ nmcli connection show --active
	 $ sudo nmcli con add ifname br0 type bridge con-name br0
	 $ sudo nmcli con add type bridge-slave ifname eno1 master br0
	 $ nmcli -f bridge con show br0
	 $ brctl show	 
	 ```
* Disable "Wired connection 1" and turn no br0
	 ```bash
	 $ sudo nmcli con down "Wired connection 1"
	 $ sudo nmcli con up br0  
	 ```
	 - Create a bridge profile
	 ```bash
	 $ incus create profile bridge
	 $ incus profile device add bridge eth0 nic name=eth0 nictype=bridged parent=br0
	 ``` 
* Launch image with bridge profile
	 ```bash
	 $ incus launch images:ubuntu/noble lan --profile default --profile bridge
	 ```
### Macvlan 
>[!NOTE]
> Incus `macvlan network` **NO** requiere de configuración adicional, esta basada en un modulo del kernel de linux _legacy_.  obtiene la IP de la LAN donde se encuentra el _host_ pero la limitación es que las comunicaciónes entre el _host_ y la _VM_ no son posibles.
 
  * Create a `macvlan` profile
	 ```bash
	 $ incus create profile bridge
	 $ incus profile device add bridge eth0 nic name=eth0 nictype=macvlan parent=br0
	 ``` 
* Launch image with `macvlan` profile
	 ```bash
	 $ incus launch images:ubuntu/noble lan --profile default --profile macvlan
	 ```

### Storage
  ```bash
$ incus storage show
$ incus storage info <pool_name>
$ incus storage set <pool_name> size=<new_size>GiB
 ``` 
 ### Custom images 
 #### [Linux based images](https://discussion.scottibyte.com/t/incus-virtual-machine-custom-installation/407)
 ```bash
$ incus init mint --empty --vm
$ incus config device override mint root size=20GiB
$ incus config set mint limits.cpu=4 limits.memory=4GiB
$ incus config device add mint install disk source=<mint.iso> boot.priority=10
$ incus start mint --console=vga
$ incus config device remove mint install
$ incus console mint --type=vga
$ incus publish mint --alias mint22-image
$ incus launch --vm mint22-image mint22 -c limits.memory=4GiB -c limits.cpu=4 -c security.secureboot=false --console=vga

 ```
  #### [Windows based](https://discussion.scottibyte.com/t/super-easy-windows-11-install-in-an-incus-vm/679)
 ```bash
$ wget https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/virtio-win-0.1.271-1/virtio-win-0.1.271.iso
$ incus init win11 --empty --vm
$ incus config device override win11 root size=85GiB
$ incus config set win11 limits.cpu=4 limits.memory=8GiB
$ incus config device add win11 vtpm tpm path=/dev/tpm0
$ incus config device add win11 disk install source=<windows11.iso> io.bus=usb boot.priority=10
$ incus config device add win11 virtio disk source=/home/<user>/Downloads/virtio-win-0.1.271.iso io.bus=usb boot.priority=5
$ incus start win11 --console=vga
$ incus console win11 --type=vga
$ incus config device remove win11 install
$ incus config device remove win11 virtio
$ incus publish win11 --alias win11-image
 ```
### Running Graphical Applications in Incus Containers
* Descargar _X11.profile_
```bash
$ wget -O ~/X11.profile https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/resources/files/X11.profile
```
* Crear un perfil para poder ejecutar aplicaciones gráficas en un contenedor

```bash
$ incus profile create X11 < X11.profile
```
* Lanzar la imagen con el nuevo _profile_
```bash
$ incus launch images:ubuntu/noble/cloud --profile default --profile X11 gui
```



 ### Anexo I. Links
 * [linux containers](https://images.linuxcontainers.org/)
 * [# Running Graphical Applications in Incus Containers](https://regrow.earth/blog/2024-10-29_gui-apps-in-incus-containers/)
 
 