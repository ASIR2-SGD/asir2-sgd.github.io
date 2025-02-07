# Práctica Firewall.
## Configuración de un cortafuegos basado en iptables

## Contexto
Los cortafuegos se utilizan con frecuencia para evitar que otros  usuarios de Internet no autorizados tengan acceso a las redes privadas  conectadas a Internet. Estos suelen actuar como un organismo de  inspección que verifica las conexiones que se establecen entre una red y un equipo local. Un cortafuegos regula, por lo tanto, la comunicación  entre ambos para proteger el ordenador contra programas maliciosos u  otros peligros de Internet.

## Links
* [iptables-essentials](https://www.digitalocean.com/community/tutorials/iptables-essentials-common-firewall-rules-and-commands)
* [iptables, un manual sencillo](https://fp.josedomingo.org/seguridadgs/u03/iptables.html)

## Objetivos
* Virtualizar el escenario necesario para llevar a cabo la práctica
* Conocer el funcionamiento de un cortafuegos basado en tablas y cadenas
* Crear las reglas en iptables
* Ser capaz de configurar el cortafuegos según las especificaciones del problema

## Desarrollo

### Preapración del escenario virtual del escenario

Instalamos el paquete _iptables-persistent_
```bash
vagrant@fw sudo apt install iptables-persistent
```

Eliminamos la puerta de enlace del interfaz eth0 (nat) para evitar confusiones durante la práctica

```bash
vagrant@lan sudo route del default gw 10.0.2.2
vagrant@fw sudo route del default gw 10.0.2.2
vagrant@dmz sudo route del default gw 10.0.2.2
```
Añadimos las puertas de enlace necesarias para la práctica.

```bash
vagrant@lan:$ sudo route add default gw 10.0.82.1
vagrant@dmz:$ sudo route add default gw 10.0.200.1
vagrant@fw:$ sudo route add default gw 192.168.82.100
```
Estos cambios no añaden la ruta por defecto de forma permanente y se borra en cada reinicio. Deberemos añadirla en un nuevo fichero de netplan, ya que vagrant modifica le fichero _50-vagrant.yaml_ en cada reinicio
```bash
vagrant@lan:$ sudo vi /etc/netplan/60-routes.yaml
```

```bash
---
network:
  version: 2
  renderer: networkd
  ethernets:
    eth1:
      routes:
      - to: default
        via: 10.0.82.1

```

Ejecutamos _netplan try_ para verificar la sintaxis
```bash
vagrant@lan:$ sudo netplan try
```

Realizamos la misma operación en la máquina _dmz_ y la máquina _ldap_ modificando la puerta de enlace.


Activamos enrutamiento en el _firewall_
De forma temporal mediante el comando
```bash
sysctl -w net.ipv4.ip_forward=1
```
Hacemos el cambio persistente editando el fichero _/etc/sysctl.conf_ y descomenta la linea 28

```bash
vagrant@fw:$ sudo vi /etc/sysctl.conf
28 net.ipv4.ip_forward=1
```
Reiniciar el servicio _systemd-sysctl_
```bash
sudo systemctl restart systemd-sysctl.service 
```
Probamos conectividad

```bash
vagrant@lan:$ ping 10.0.82.1
vagrant@lan:$ ping 10.0.82.200
vagrant@lan:$ ping 10.0.200.100
vagrant@lan:$ ping 192.168.82.100
vagrant@lan:$ ping yahoo.es
```


Para navegar en la internet, necesitamos utilizar una ip pública, para ello activaremosa traducción de direcciones privadas a públicas (NAT) en el cortafuegos
```
iptables -t nat -A POSTROUTING -o eth3 -j MASQUERADE
```

### Arquitectura IP-Tables

![iptables chains](https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/img/iptables-in-linux.webp)
![iptables-chains](https://miro.medium.com/v2/resize:fit:720/format:webp/1*Vs4XnYTCI4fXYuGl2V3xfw.png)

## Firewall
- [ ] Permitir el tráfico desde el interfaz loopback
- [ ] No se permitirá ninguna conexión entrante al cortafuegos exceptuando ssh desde nuestro ordenador anfitrión y el ordenador del profesor 192.168.82.100
- [ ] 
- [ ] DS
- [ ] D
- [ ] SD
- [ ] SD
- [ ] 
TODO: Desarrollar las reglas
TODO: Realizar diagrama de red


## Anexo I. Comados IP-Tables
1. Lista la tabla filter(por defecto)
	```bash
	iptables -L
	```
2. Lista la cadena INPUT de la tabla filter
	```bash
	iptables -t filter -L INPUT
	```
3. Lista la tabla nat
	```bash
	iptables -t nat -L
	```
4. Aplica la política por defetco DROP a la cadena INPUT de la tabla _filter_
	```bash
	iptables -t filter -P INPUT DROP
	```
5. Borra(flush) las reglas de la cadena FORWARD de la tabla filter(por defecto)
	```bash
	iptables -F FORWARD
	```
6. NAT Maquerade
	```bash
	iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
	```

7. sd
	```bash
	iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
	```
8. ds
	```bash
	iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
	```
9. s
	```bash
	iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
	```
10. sd
	```bash
	iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
	```
11. sd
	```bash
	iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
	```
12. sd
	```bash
	iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
	```



>[!NOTE]
> A realizar por el alumno

>[!TIP]
>dsd

>[!IMPORTANT]
>dsd

>[!WARNING]
>kjkñl


>[!CAUTION]
>kjkñl
