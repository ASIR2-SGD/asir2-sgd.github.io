---
layout: default
title: Redundancia de datos y volúmenes lógicos
---
# Gestor de Volúmenes lógicos (LVM)

## Contexto
Nuestras necesidades de almacenamiento cambian dependiendo del momento, en muchos casos debemos aumentar el tamaño de nuestro almacenamiento empleando el menor tiempo posible. Para ello necesitamos un esquema de almacenamiento flexible. LVM es una capa de abstracción que permite gestionar el almacenamiento de manera más flexible que el particionado tradicional. Divide el espacio en tres componentes: Volúmenes Físicos (PV), que son las unidades de almacenamiento subyacentes; Grupos de Volúmenes (VG), que agrupan los PV en un "disco virtual"; y Volúmenes Lógicos que son las particiones que el sistema operativo utiliza. Sus principales ventajas incluyen la capacidad de redimensionar volúmenes dinámicamente sin parar el sistema
## Objetivos
* Comprender el sistema de volúmentes lógicos de *linux*
* Crear y configurar un LVM mediante comandos.
* Automatizar la tarea
## Pasos previos

### Creación y manejo de volúmenes en incus VM
Para trabajar con dispositivos de bloques es necesario crear una **máquina virtual** en incus, esta a diferencia de los contenedores de sistema dispone de su propio kernel, pero desde el punto de vista del usuario la interfaz de comandos es la misma.
```bash
incus$ incus launch images:ubuntu/24.04 lvm --vm
incus$ incus exec lvm -- bash -c 'apt-get update && apt-get -y install  aptitude wget bash-completion gpg nano xsel vim bats git lvm2'
```

Incus almacena los datos (imágenes,máquinas virutales, contenedores y custom) en _pools_ divididos en _volúmenes_ de diferentes tipos. Por defecto incus crea un pool denominado _default_. Podemos hacer uso de este pool para crear nuestros volumenes que simularán los discos de nuestro RAID.

Para crear los dispositivos de bloques (discos) utilizaremos los siguientes comandos en incus
```bash
incus$ incus storage volume list <pool>
incus$ incus storage volume create <pool> disk_a size=10MiB --type=block
incus$ incus storage volume delete <pool> disk_a
incus$ incus storage volume list <pool> -c tnc

```

| TYPE   | NAME   |
| ------ | ------ |
| custom | disk_b |
| custom | disk_c |
| custom | disk_d |
| custom | disk_e |
| custom | disk_f |
| custom | disk_g |

Una vez creado el volumen, lo asociamos a una instancia
```bash
incus$ incus storage volume attach <pool> disk_a <instance>
incus$ incus storage volume detach <pool> disk_a <instance>
```

Podemos ver los dispositivos de bloques que tiene nuestra instancia con el comando ```lsblk```

## Actividad

Crea una instancia de **máquina virtual** denominada _lvm_ y añadele tres volúmenes de 20MiB y 2 volúmentes de 10MiB

```bash
##lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda      8:0    0   10G  0 disk 
├─sda1   8:1    0  100M  0 part /boot/efi
└─sda2   8:2    0  9.9G  0 part /
sdb      8:16   0   10M  0 disk 
sdc      8:32   0   10M  0 disk 
sdd      8:48   0   10M  0 disk 
sde      8:64   0   10M  0 disk 
```

Vamos a simular que los dispositivos son de diferente naturaleza física y unos son discos duros magnéticos HDD y otros SSD.

| Device | Type |
| ---------- | -------- |
| /dev/sdb | HDD |
| /dev/sdc | HDD |
| /dev/sdd | HDD |
| /dev/sde | SSD |
| /dev/sdf | SSD |

Utilizaremos los dispositivos SSD para las aplicaciones que requieran acceso más rápido al sistema de almacenamiento.
Utiliza _lvm_ para crear el siguiente esquema de almacenamiento.

![lvm schema]({% link /resources/img/lvm.png %})



## Evaluable
* Entrega el _taskfile_ denominado _taskfile.yml_ que cree la instancia _lvm_ y configure los discos según el esquema indicado en clase. 
* El fichero `Taskfile` entregado debe tener como mínimo las siguienes tareas:
* __init__: creación y aprovisionamiento de la instancia denominada _acl_
* __destroy__: destrucción de la instancia _acl_
* __build__: construye la práctica (estrucutra de ficheros y directorios necesarios, usuarios, grupos, permisos)
* __clean__: Elimina todo lo creado en la tarea _build_
* __test__: Ejecuta los tests.
* 
## Anexo I. Comandos LVM
Se enumeran a continuación los comandos relacionados con la creción, eliminación y visualización de los volúmenes físicos, grupo de volúmenes y volúmenes lógicos.

**Volúmenes lógicos**
```bash
pvcreate /dev/sdX /dev/sdX
pvremove /dev/sdX
pvdisplay /dev/sdX
pvscan
pvs
```

```bash
root@lvm:~# pvs
  PV         VG Fmt  Attr PSize  PFree 
  /dev/sdb      lvm2 ---  10.00m 10.00m
  /dev/sdc      lvm2 ---  10.00m 10.00m
  /dev/sdd      lvm2 ---  10.00m 10.00m
  /dev/sde      lvm2 ---  10.00m 10.00m

```

**Grupo de volúmenes**
Cuando se utilizan volúmenes físicos para crear un grupo de volumen, sl espacio de disco se divide en extensiones de 4MB de forma predeterminada. El valor de la extensión es la cantidad mínima por la cual el volumen lógico puede ser incrementado o reducido. 

Si el valor predeterminado no es el deseado, el tamaño de la extensión puede ser especificado con la opción `-s` del comando `vgcreate`

```bash
vgcreate -s <PE_size> <volumen group> /dev/sdX /dev/sdX
vgreduce <volumen group> <phisical volume>
vgextend <volumen group> <phisical volume>
vgremove <volumen group>
vgdisplay <volumn group>
vgs
```

**Volúmenes lógicos**
```bash
lvcreate -L 10G -n <name> <volumen group>
lvcreate -l 20%VG -n <name> <volumen group>
lvcreate -l 100%FREE -n <name> <volumen group>
lvextend -l +10%VG <path logical volume> #/dev/volumen_group/logical_volumen
lvs
```

**Crea y monta sistema de archivos**

```bash
mkfs.ext4 /dev/volume_group/logical_volume
mount /dev/volume_group/logical_volume <local_mount_point>

```
Edita el fichero _/etc/fstab_ para hacer el punto de montaje permanente.

**Implementación RAID de LVM**
```bash
lvcreate --type raid1 -m 1 -L 1G -n raid1 my_vg
#three stripes + 1 parity
lvcreate --type raid5 -i 3 -L 1G -n raid5 my_vg 
#three stripes + 2 parity
lvcreate --type raid6 -i 3 -L 1G -n raid6 my_vg
```
## Anexo II. Referencias
* [An Introduction to LVM Concepts, Terminology, and Operations](https://www.digitalocean.com/community/tutorials/an-introduction-to-lvm-concepts-terminology-and-operations)
* [5.4.16. RAID Logical Volumes](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/)
* [5.4.3. Creating Mirrored Volumes](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/logical_volume_manager_administration/mirror_create)
