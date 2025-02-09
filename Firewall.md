# Práctica Firewall.
## Configuración de un cortafuegos basado en iptables

## Contexto
Los cortafuegos se utilizan con frecuencia para evitar que otros  usuarios de Internet no autorizados tengan acceso a las redes privadas  conectadas a Internet. Estos suelen actuar como un organismo de  inspección que verifica las conexiones que se establecen entre una red y un equipo local. Un cortafuegos regula, por lo tanto, la comunicación  entre ambos para proteger el ordenador contra programas maliciosos u  otros peligros de Internet.

## Links
* [iptables-essentials](https://www.digitalocean.com/community/tutorials/iptables-essentials-common-firewall-rules-and-commands)
* [How To Implement a Basic Firewall Template with Iptables on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-implement-a-basic-firewall-template-with-iptables-on-ubuntu-20-04)
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

>[!NOTE]
> El alumno deberá implementar el resto de reglas según se detalla en el siguiente apartado y se muTCP es un protocolo basado en conexión, por lo que una conexión ESTABLISHED esta bien definida. UDP es un protocolo no orientado a conexión, por lo que ESTABLISHED hace referencia a tráfico que ha tenido una respuesta y viceversa.

### Firewall - Reglas
![network_diagram](https://github.com/ASIR2-SGD/asir2-sgd.github.io/blob/main/img/network_diagram.png?raw=true)
- [ ] Permitir el tráfico desde el interfaz loopback
- [ ] No se permite el trafico entrante (dirigido a) ni saliente (generado por) del cortafuegos, exceptuando el tráfico _ssh_ proveniente desde nuestr ordenador anfitrión y el ordenador del profesor 192.168.82.101
- [ ] No se permite el tráfico de la red _dmz_ a la red _lan_ exceptuando el tráfico _ldap_ dirigido a al servidor _ldap_.
- [ ] No se permite el tráfico saliente (generado por) de la red _dmz_ exceptuando el mencionado en el apartado anterior
- [ ] Se permite el tráfico al exterior (wan) generando en la red _lan_, exceptuando el tráfico proveniente del servidor _ldap_
- [ ] Se permite el tráfico http/s del exterior dirigido a la _dmz_
- [ ] Las peticiones provenientes del exterior al puerto 80/443 (http/s) serán redirigidas al servidor web de la _dmz_

>[!CAUTION]
>La conexión _ssh_ al _fw_ se realiza desde una ip de la red 10.0.2.0/24. Utiliza el comando _netstat -atunp_ para conocer la ip exacta y permitir estas conexiónes únicamente desde esa ip.

>[!Tip]
>Se metódico y cuidadoso a la hora de establecer las reglas. Crea un fichero (script) bien documentado con a medida que vas añadiendolas. Comprueba el efecto de cada una y ejecuta los _tests_ de regresión para verificar que las reglas añadidas no rompen el estado anterior.

>[!Tip]
>Si en algún momento deseas que tu máquina tenga acceso a internet, puedes hacerlo de forma temporal agregando la linea ```route add default gw 10.0.2.2``` . Recuerda eliminarla finalizado el uso de internet para no alterar el funcionamiento de la práctica. Usa el comando ```route del default gw 10.0.2.2```

### Redireccionamiento de puertos y apache2 ldap authentication.

En nuestra zona DMZ ubicaremos un servidor web, en el cual ciertas páginas estarán protegidas y únicamente se permitira el acceso a los usuarios autenticados. La autenticación se llevara a cabo mediante el servidor _ldap_ que hay en la _lan_, alcanzable a través de las reglas del firewall.
Para llevara a cabo la autenticación deberemos utilizar el módulo de apache [_mod_authnz_ldap_](http://www.yolinux.com/TUTORIALS/LinuxTutorialApacheAddingLoginSiteProtection.html#LDAP). Otros recursos donde explica como llevar a cabo la autenticación son:
* [How to Setup Apache Authentication using LDAP Active Directory](https://cloudinfrastructureservices.co.uk/how-to-setup-apache-authentication-using-ldap-active-directory/)
* [Apache with LDAP authentication](https://medium.com/@uri.tau/apache-and-ldap-cc7bff1f629d)

>[!NOTE]
>Nuestro servidor web, ubicado en la máquina _dmz_ deber responder con un dialogo de autenticación a la url:: ``` ip:/sad_secure``` 
## Anexo I. Arquitectura IP-Tables

![iptables chains](https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/img/iptables-in-linux.webp)


![iptables-chains](https://miro.medium.com/v2/resize:fit:720/format:webp/1*Vs4XnYTCI4fXYuGl2V3xfw.png)

**Contrack**: Seguimiento de paquetes
![iptables_conntrack_2](https://github.com/ASIR2-SGD/asir2-sgd.github.io/blob/main/img/iptables_conntrack_2.png?raw=true)


![iptables_conntrack_3](https://github.com/ASIR2-SGD/asir2-sgd.github.io/blob/main/img/iptables_conntrack_3.png?raw=true)
## Anexo II. Comados
### Netfilter
1. Borrado de reglas
	```bash
	netfilter-persistent flush
	```
2. Carga las reglas del fichero _/etc/iptables/rules.v4_
	```bash
	netfilter-persistent reload
	```
3. Guarda las reglas en el fichero _/etc/iptables/rules.v4_
	```bash
	netfilter-persistent save
	```
### IP-Tables
4. Lista la tabla filter(por defecto)
	```bash
	iptables -L
	```
5. Lista la cadena INPUT de la tabla filter
	```bash
	iptables -t filter -L INPUT
	```
6. Lista la tabla nat
	```bash
	iptables -t nat -L
	```
7. Aplica la política por defetco DROP a la cadena INPUT de la tabla _filter_
	```bash
	iptables -t filter -P INPUT DROP
	```
8. Borra(flush) las reglas de la cadena FORWARD de la tabla filter(por defecto)
	```bash
	iptables -F FORWARD
	```
9. NAT Maquerade
	```bash
	iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
	```

10. Aceptamos tráfico originado en el loobpack local, tráfico del servidor, destinado al servidor
	```bash
	iptables -A INPUT -i lo -j ACCEPT
	```
11. Aceptamos tráfico (respuesta) parte de una conexion ya establecida iniciada en el servidor
>[!NOTE]
> Esta regla utiliza el módulo _conntrack_ que permite a _iptables_ obtener el contexto necesario para evaluar paquetes que forman parte de una conexión 

>[!NOTE]
> TCP es un protocolo basado en conexión, por lo que una conexión ESTABLISHED esta bien definida. UDP es un protocolo no orientado a conexión, por lo que ESTABLISHED hace referencia a tráfico que ha tenido una respuesta y viceversa.

	```bash
	iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
	```

13. Denegamos tráfico _inválido_ a causa de una conexión, un interfaz o un puerto no existente.
	```bash
	iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
	```
14. Rechazamos el tráfico ICMP devolviendo un mensaje de error
	```bash
	iptables -A INPUT -p icmp -j REJECT --reject-with icmp-port-unreachable
	```
15. Rechazamos el tráfico proveniente de una red o ip
	```bash
	iptables -A INPUT -s 203.0.113.51 -j DROP
	iptables -A INPUT -s 203.0.113.0/24 -j DROP
	```
16. Rechazamos el tráfico proveniente de una red y un interfaz de red
	```bash
	iptables -A INPUT -i eth0 -s 203.0.113.51 -j DROP
	```
17. Permitimos el tráfico SSH de entrada de una red específica o Ip
	```bash
	iptables -A INPUT -p tcp -s 203.0.113.0/24 --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
	
	
	```
18. Permitimos el tráfico HTTP/S atraviese el firewall
```bash
	iptables -A FORWARD -p tcp -m multiport --dports 80,443 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
	iptables -A FORWARD -p tcp -s 203.0.113.0/24 -m multiport --dports 80,443 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT		
```
19. Permitimos el tráfico de la red interna a la red externa (asumiendo _eth0_ es la red interna y _eth1_ la externa)
	```bash
	sudo iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
	```
20. Cambia la dirección ip de destino (DNAT)
	```bash
	iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to-destination 192.168.1.2:80
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
