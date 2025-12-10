# OVS-INCUS

Install OVS
```bash
sudo apt-get install openvswitch-switch
```

Basics
```bash
sudo ovs-vsctl show
ip link show
ip link set dev eth1 up
ip link set ovs-br0 up
```

Create virtual switch and tagged interfaces (if needed)

```bash
sudo ovs-vsctl add-br ovs-br0
sudo ovs-vsctl add-port ovs-br0 eth1 tag=10 -- set interface eth1 type=internal
```

Attach incus container to the switch
```bash
incus launch images:ubuntu/noble --network ovs-br0
incus config device add <instance> eth1 nic nictype=bridged parent=ovs-br0
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