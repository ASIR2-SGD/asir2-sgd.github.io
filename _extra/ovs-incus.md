# OVS-INCUS

## Launch incus container
```bash
incus launch images:ubuntu/noble firewall
incus exec firewall -- bash -c 'apt-get update && apt-get -y install  aptitude wget bash-completion gpg nano xsel vim' 
```

## Install OVS
```bash
sudo apt-get install openvswitch-switch
```

## Install incus
```bash
incus exec firewall -- wget -O /etc/apt/keyrings/zabbly.asc https://pkgs.zabbly.com/key.asc
incus exec firewall -- sh -c 'cat <<EOF > /etc/apt/sources.list.d/zabbly-incus-stable.sources
Enabled: yes
Types: deb
URIs: https://pkgs.zabbly.com/incus/stable
Suites: $(. /etc/os-release && echo ${VERSION_CODENAME})
Components: main
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/zabbly.asc

EOF'
incus exec firewall -- apt-get update
incus exec firewall -- apt-get -y install incus
```

## Set up incus remote server
```bash
$server incus config set core.https_address :8443
$server incus config trust add host
$server incus config trust list

$client incus remote add firewall 10.149.165.138
$client incus config device add c1-net eth1 nic network=incusbr0

$client incus remote list
$client incus remote switch <remote-name>
```

## Instalar openwrt
```
## OVS Basics
```bash
sudo ovs-vsctl show
ip link show
ip link set dev eth1 up
ip link set ovs-br0 up
```

## Create virtual switch and tagged interfaces (if needed)

```bash
sudo ovs-vsctl add-br ovs-br0
sudo ovs-vsctl del-br ovs-br0
sudo ovs-vsctl add-port ovs-br0 eth1 tag=10 -- set interface eth1 type=internal
sudo ovs-vsctl del-port ovs-br0 eth0
```

## Attach incus container to the switch
```bash
incus launch images:ubuntu/noble --network ovs-br0
incus config device add <instance> eth0 nic nictype=bridged parent=lan1
incus config device add <instance> eth2 nic name=wan nictype=bridged parent=ovs-br0
incus config device delete <instance> eth0
```
>[!NOTE]
>If access to OVS switch network from host is needed. A static route must be placed to one of the virtual switch ports `sudo ip route add 172.21.1.0/24  dev ovs-br0`


>[!NOTE]
>If seting up OpenWrt, add static ip to LAN interface and enable DHCP on that interface.


# Links
* [Understanding Oven Virtual Switch](https://medium.com/@ozcankasal/understanding-open-vswitch-part-1-fd75e32794e4)
* [Playing with OVN Part I](https://humanz.moe/posts/playing-with-ovn-v1/)
* [Using Open Virtual Network Layer-3 Switch Replacement](https://github.com/jcpowermac/homelab-ovn?tab=readme-ov-file)
* [Skydive Network analyzer](https://github.com/skydive-project/skydive)