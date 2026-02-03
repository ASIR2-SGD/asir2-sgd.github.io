---
layout: default
title: "OpenSense"

---
# OpenSense

## VM Install
```bash


$incus profile create opensense << EOF
config:
  limits.cpu: "2"
  limits.memory: 4GiB
  raw.qemu: |
    -cpu host
  raw.qemu.conf: |
   [device "dev-qemu_rng"]
  security.secureboot: "false"
devices: 
  eth0:
    name: lan
    nictype: bridged
    parent: ovs-br0
    type: nic
  eth1:
    name: wan
    network: incusbr0
    type: nic
EOF
$incus create opensense --vm --empty -d root,size=40GiB --profile opensense

$incus config device add opensense iso disk     source=~/Downloads/OPNsense-xx.x-vga-amd64.img   boot.priority=10

$incus start opensense --console vga #default password opnsense
incus config device remove opensense iso


```

Configurar opensense desde consola, habilitando servidor dhcp en lan

```bash
incus launch images:ubuntu/noble lan1 --network ovs-br0
```