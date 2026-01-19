description: Sets up GPU, Wayland, X11 and PulseAudio
devices:
  intel-igpu:
    gid: "1000"
    type: gpu
    uid: "1000"
  pulse:
    bind: instance
    connect: unix:/run/user/1000/pulse/native
    gid: "1000"
    listen: unix:/mnt/pulse.sock
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
