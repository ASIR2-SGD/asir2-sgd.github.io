---
layout: default
title: "OpenWrt"

---
# OpenWrt
## Setup en un contenedor incus

* Crea red _LAN_ (192.168.82.0/24)
```bash
$ incus network create LAN \
	 ipv4.address=192.168.82.1/24 \
	 ipv6.address=none ipv4.nat=true \
	 ipv4.dhcp.ranges=192.168.82.150-192.168.82.220
```

```bash
$ incus launch images:openwrt/24.10 openwrt 

$ incus config device add openwrt eth1 nic network=LAN
$ incus config device add openwrt eth1 nic name=eth1 nictype=bridged parent=ovs-br0
$ incus config device add openwrt eth1 nic name=eth1 nictype=macvlan parent=eth1 
```

>[!WARNING]
>Es posible que no podamos acceder mediante Luci o SSH a OpenWrt puesto que por defecto OpenWrt previene el acceso al UI desde el interfaz WAN.
>Una posible solución es la de borrar de forma temporal las reglas del cortafuegos para acceder y luego reestablecerlas. [tutorial](https://discuss.linuxcontainers.org/t/openwrt-getting-started-question/22205)


 ```bash
$ incus exec openwrt -- ash -c 'cat << EOF >> /etc/config/network 
config interface 'lan'
        option ifname eth1
        option proto dhcp
EOF
'
 ```

Ejemplo _/etc/config/network_
```bash
config interface 'loopback'
    option ifname 'lo'
    option proto 'static'
    option ipaddr '127.0.0.1'
    option netmask '255.0.0.0'

config interface 'wan'
    option ifname 'eth0'
    option proto 'dhcp'

config interface 'wan6'
    option ifname 'eth0'
    option proto 'dhcpv6'


config interface 'LAN'
    option proto 'static'
    option device 'eth1'
    option ipaddr '172.21.1.1'
    option netmask '255.255.255.0'
```

