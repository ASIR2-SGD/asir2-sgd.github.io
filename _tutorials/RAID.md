---
layout: default
title: Redundancia de datos y volúmenes lógicos
---
# Redundancia de datos (RAID)

## Contexto
Los ordenadores trabajan con datos, y estos son almacenados en forma de ficheros. Que dichos ficheros sean almacenadas y accedidos de forma segura es, por tanto, una de nuestras tareas más importantes como adminitradores de un sistema informático y en ello influye la política de almacenamiento adoptada.

En esta práctica se trabajará sobre la política de almacenamiento redundante que aporta una capa más en la seguridad de la información al coste de disponer de más dispositivos de almacenamiento.

## Objetivos
* Entender que es un RAID y los diferentes niveles de seguridad.
* Crear y configurar un RAID en *linux* mediante comandos
* Comprobar y verificar mediante un entorno de pruebas que el RAID funciona como es esperado.
* Automatizar la actividad.
* Implementar un RAID haciendo uso de ZFS
## Pasos previos

### Creación y manejo de volúmenes en incus VM
Para trabajar con dispositivos de bloques es necesario crear una máquina virtual en incus, esta a diferencia de los contenedores de sistema dispone de su propio kernel, pero desde el punto de vista del usuario la interfaz de comandos es la misma.
```bash
incus$ incus launch images:ubuntu/24.04 raid --vm
incus$ incus exec raid -- bash -c 'apt-get update && apt-get -y install  aptitude wget bash-completion gpg nano xsel vim mdadm lvm2'
```

Incus almacena los datos en _pools_ divididos en _volúmenes_ de diferentes tipos. Por defecto incus crea un pool denominado _default_. Podemos hacer uso de este pool para crear nuestros volumenes que simularán los discos de nuestro RAID.

Los siguientes comandos crean y eliminan volúmenes en el pool _defatult_
```bash
incus$ incus storage volume list <pool>
incus$ incus storage volume create <pool> disk_a size=10MiB --type=block
incus$ incus storage volume delete <pool> disk_a
incus$ incus storage volume list <pool> -c tnc

```

Una vez creado el volumen, lo asociamos a una instancia
```bash
incus$ incus storage volume attach <pool> disk_a <instance>
incus$ incus storage volume detach <pool> disk_a <instance>
```

Podemos ver los dispositivos de bloques que tiene nuestra instancia con el comando ```lsblk```

## Actividad

Crea una instancia de **máquina virtual** denominada _lvm_ y añadele seis volúmenes de 10MiB.

TODO: crea un esquema de LVM

## Evaluable
* Entrega el _taskfile_ denominado _taskfile_lvm.yml_ que cree la instancia _lvm_ y configure los discos según el esquema indicado en clase. Añande las tareas de clean y destroy.
* Entrega el taskfile denominado _taskfile_rad.yml_ que cree la instancia _raid_ y configure un raid como se indica en clase.
* Verifica y comprueba que el RAID funciona como es esperado. Prueba a quitar un disco y ver el comportamiento del RAID
* Investiga y aprende el uso del sistema de ficheros ZFS que incorpora características de RAID.
* Entrega un taskfile denominado taskfile_zfs.yml que cree una instancia _zfs_ siguiendo el mismo esquema que en el apartado anterior pero haciendo uso del sistema de ficheros _zfs_
* **EXTRA**: Investiga y  expande tus conocimientos instalando en una VM limpia creada en incus el S.O TrueNAS, un S.O específico con interfaz gráfica web para la creación de un NAS.

