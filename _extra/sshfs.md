---
layout: default
title: "sshfs config mount"
---
[Tutorial](https://www.digitalocean.com/community/tutorials/how-to-use-sshfs-to-mount-remote-file-systems-over-ssh)

# SERVER
```bash
incus launch images:ubuntu/noble sshfs --network enp5s0
incus exec sshfs -- bash -c 'apt-get install aptitude openssh-server wget vim nano git bash-completion tree' 
incus exec sshfs -- su -l ubuntu -c 'mkdir -p ~/gpg/{aguilar,arnedo,lucas,...}'
```

# CLIENTS
```bash
incus exec c1 -- bash -c 'apt-get install aptitude sshfs wget vim nano git bash-completion'
```
## Genera clave y copia en servidor
```bash
incus exec c1 -- bash -c 'apt-get install aptitude sshfs wget vim nano git bash-completion'

incus exec c1 -- bash -c 'ssh-keygen -t rsa -b 4096 -C "your_email@example.com"'
#incus exec c1 -- bash -c 'ssh-copy-id ubuntu@ip"'
incus exec c1 -- bash -c 'scp .ssh/id_rsa.pub ubuntu@ip:'
incus exec c1 -- bash -c 'ssh ubuntu@ip "cat id_rsa.pub >> .ssh/authorized_keys"'
incus exec c1 -- bash -c 'ssh ubuntu@ip "rm id_rsa.pub"'
incus exec c1 -- bash -c 'apt-get install aptitude sshfs wget vim nano git bash-completion'
```
## Conecta con el servidor mediante comando sshfs 
```bash
incus exec c1 -- bash -c 'mkdir -p ~/gpg'
incus exec c1 -- bash -c 'sed  -i -e "s/#\(user_allow_other\)/\1/" /etc/fuse.conf'
incus exec c1 -- bash -c 'sshfs -o allow_other,default_permissions ubuntu@ip:/home/ubuntu/gpg ~/gpg'
```

## Cambios permanentes mediante systemd mount
```bash
#incus exec c1 -- bash -c 'echo -e ip:/home/ubuntu/gpg\t\t~/gpgnfs	ro,defaults 0 0" >> /etc/fstab
```

```bash
incus exec c1 -- bash -c 'cat > /etc/systemd/system/home-ubuntu-gpg.mount << EOF
[Unit]
Description=SSHFS mount for remote data
After=network-online.target
Wants=network-online.target
Before=remote-fs.target

[Mount]
What=ubuntuy@ip:/home/ubuntu/gpg
Where=/home/ubuntu/gpg
Type=fuse.sshfs
Options=allow_other,default_permissions,compression=yes,cache=yes,auto_cache,reconnect,IdentityFile=/home/ubuntu/.ssh/id_rsa

[Install]
WantedBy=multi-user.target
EOF
'
```
```bash
incus exec c1 -- bash -c 'systemctl enable home-ubuntu-gpg.mount'
incus exec c1 -- bash -c 'systemctl start  home-ubuntu-gpg.mount'
incus exec c1 -- bash -c 'systemctl restart  home-ubuntu-gpg.mount'
```