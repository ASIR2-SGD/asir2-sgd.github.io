
**Activar ratón**
```bash
printf "#Enable mouse support\nset -g mouse on\n" | tee ~/.config/byobu/.tmux.con
```

**Window template**
```bash
cat << EOF > ~/.config/byobu/windows.tmux.incus
new-session -A -s incus -n incus ;
new-window -n grafana incus shell grafana ;
new-window -n alloy incus shell alloy ;
new-window -n loki incus shell loki ;
new-window -n mimir incus shell mimir ;
new-window -n multi incus shell grafana ;
split-window incus shell alloy ;
split-window incus shell loki ;
split-window incus shell mimir ;
select-layout tiled ;
select-window -t tiled
EOF
```

```bash
mkdir -p ~/bin
cat << EOF > ~/bin/incus-byobu
#!/bin/bash
BYOBU_WINDOWS=incus byobu
EOF
chmod +x ~/bin/incus-byobu
```