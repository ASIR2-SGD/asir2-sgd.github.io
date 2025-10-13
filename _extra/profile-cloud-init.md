---
layout: default
title: "Cloud init example"
---

```yaml
config:
  cloud-init.vendor-data: |
    #cloud-config
    package_update: true
    package_upgrade: true
    package_reboot_if_required: true
    packages:
      - pulseaudio-utils
      - mesa-utils
      - aptitude
      - wget 
      - gpg
      - nano
    write_files:
      - path: /etc/profile
        append: true
        content: |
          export DISPLAY=:0
          export PULSE_SERVER=/mnt/pulse.sock
          export WAYLAND_DISPLAY=wayland-1
          export XDG_SESSION_TYPE=wayland
          ln -fs /mnt/X0 /tmp/.X11-unix/X0
          ln -fs /mnt/wayland-0 /run/user/1000/wayland-0    
description: Sets up GPU, Wayland, X11 and PulseAudio
devices:
  intel-igpu:
    gid: "1000"
    type: gpu
    uid: "1000"
  pulse:
    bind: instance
    connect: unix:/tmp/1000-runtime-dir/pulse/native
    gid: "1000"
    listen: unix:/mnt/pulse.sock
    mode: "0700"
    security.gid: "1000"
    security.uid: "1000"
    type: proxy
    uid: "1000"
  wayland:
    bind: instance
    connect: unix:/tmp/1000-runtime-dir/wayland-1
    gid: "1000"
    listen: unix:/mnt/wayland-1
    mode: "0700"
    security.gid: "1000"
    security.uid: "1000"
    type: proxy
    uid: "1000"
  x11:
    bind: instance
    connect: unix:/tmp/.X11-unix/X0
    gid: "1000"
    listen: unix:/mnt/X0
    mode: "0700"
    security.gid: "1000"
    security.uid: "1000"
    type: proxy
    uid: "1000"

```