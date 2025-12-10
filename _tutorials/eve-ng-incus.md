# Eve-NG over Incus VM

```bash
$ incus create eve-ng --empty --vm -c limits.cpu=2 -c limits.memory=4GiB -d root,size=20GiB
$ incus config device add eve-ng install disk source=<eve-ng.iso> boot.priority=10
$ incus start eve-ng --console=vga
$ incus config device remove eve-ngt install
$ incus console mint --type=vga
$ incus launch --vm mint22-image mint22 -c limits.memory=4GiB -c limits.cpu=4 -c security.secureboot=false --console=vga
```