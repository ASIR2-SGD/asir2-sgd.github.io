---
layout: default
title: "firewall"
---
# Práctica Firewall.
## Configuración de un cortafuegos basado en iptables

## Contexto
Los cortafuegos se utilizan con frecuencia para evitar que otros  usuarios de Internet no autorizados tengan acceso a las redes privadas  conectadas a Internet. Estos suelen actuar como un organismo de  inspección que verifica las conexiones que se establecen entre una red y un equipo local. Un cortafuegos regula, por lo tanto, la comunicación  entre ambos para proteger el ordenador contra programas maliciosos u  otros peligros de Internet.


## Objetivos
* Virtualizar el escenario necesario para llevar a cabo la práctica
* Conocer el funcionamiento de un cortafuegos basado en tablas y cadenas
* Crear las reglas en iptables
* Ser capaz de configurar el cortafuegos según las especificaciones del problema

## Desarrollo

### Prepapración del escenario virtual
Para llevar a cabo la práctica necesitamos tres contenedores (_firewall_ , _lan1_ y _lan2_) y un switch virtual (_ovs-br0_)


**TODO. DIAGRAMA RED**

```bash
$ incus launch images:ubuntu/noble firewall
$ incus config device override firewall eth0 name=wan
$ incus config device add firewall eth1 nic nictype=bridged parent=ovs-br0
$ incus exec firewall -- bash -c 'apt-get update && apt-get -y install  aptitude wget bash-completion nano xsel vim dns-masq nftables' 
$ incus exec firewall -- bash -c 'systemctl enable nftables.service'

$ incus launch images:ubuntu/noble lan1 --network ovs-br0
```

> [!IMPORTANT]
> **Actividad** 
> * El interfaz _eth1_ que conecta con la LAN tiene que tener una ip estática, lleva a cabo la configuración de red apropiada para dicha interfaz y aplicando los cambios mediante la utilidad _netplan_. 
> La ip para el interfaz _eth1_ debe ser 10.10.82.1. 
> Los cambios en la configuración de red se llevarán a cabo editando el fichero _/etc/netplan/10-lxc.yaml_
> * El _firewall_ deberá implementar funcionalidad DHCP para proveer a sus clientes LAN de ip dinámica. Lleva a cabo la configuración del servidor DHCP usando _dnsmasq_.
> Lleva a cabo la configuración y comprueba que los clientes LAN obtienen una ip de la red 10.10.82/0

> [!WARNING]
> El servidor DNS de _dnsmasq_ colisiona a hacer uso que el mismo puerto 53 que el servicio _systemd-resolve_, para evitar este problema y que ambos servidores DNS funcionen correctamente, deberás descomentar en el fichero _/etc/dnsmasq.conf_ la linea _bind-interfaces_ y asignar la interfaz _lan_ como la interfaz de escucha de peticiones DNS y DHCP 


Para que el _fw_ actue como router y redirecciones los paquetes a la itnerfaz de salida apropiada, debemos activar _forwarding_
De forma temporal mediante el comando
```bash
firewall# sysctl -w net.ipv4.ip_forward=1
```
Hacemos el cambio persistente editando el fichero _/etc/sysctl.conf_ y descomenta la linea 28

```bash
firewall# vi /etc/sysctl.conf
28 net.ipv4.ip_forward=1
```
Reiniciar el servicio _systemd-sysctl_
```bash
firewall# systemctl restart systemd-sysctl.service 
```
## Netfilter

Netfilter es una infraestructura integrada en el kernel de linux que permite interceptar y manipular paquetes de red, actuando como el motor principal de un _firewall_ para filter el tráfico y realizar NAT, utilizando herramientas como _iptables o _nfttables_ para definir políticas y réglas sobre los interfaces de red, organizadas en tablas y cadenas.
Netfilter maneja el trafico de red en diferentes puntos (__hooks__) a medida que pasa por el sistema. _nftables_ y su antecesor _iptables_ nos permite a nivel de usuario _anclar_ una cadena de reglas (callback function) en cada uno de los _hooks_ pudiendo descartar o aceptar paquetes según la política de seguridad deseada


![Netfilter hooks -simple block diagram](https://thermalcircle.de/lib/exe/fetch.php?w=700&tok=37d6df&media=linux:nf-hooks-simple1.png)


## Nftables


>[!TIP]
>Activa el autocompletado de comandos para el comando _nft_ descargandote el siguiente fichero en la carpeta _/etc/bash_completion.d/_
>`wget -O /etc/bash_completion.d/nft-completion https://raw.githubusercontent.com/Zulugitt/bash_completion/refs/heads/main/nft-completion`


### Conceptos básicos de nftables
Para el correcto manejo de nftables, es necesario entender su estructura básica, incluyendo tablas, cadenas, reglas y conjuntos

![tables, chains and rules](https://miro.medium.com/v2/resize:fit:720/format:webp/1*PUrIVW5lk0vlevTp6hQOzA.png)

* Tablas: Agrupación lógica de cadenas y reglas relacionadas
* Cadenas: Lista de reglas dentro de una tabla. Define los puntos(hooks) dentro de la linea de procesamiento del paquete donde las reglas son aplicadas. Las más comunes son:
	* **input**: Para paquetes destinados al procesamiento local
	* **output**: Para paquetes originados en el sistema local
	* **foward**: Para paquetes siendo enrutados (van de un interfaz a otro)
	* **prerouting**: Para paquetes antes de tomar una decision de enrutamiento (Usado tipicamente para DNAT)
	* **postrouting**: Para paquetes despues de tomar una decision de enrutamiento (Usado tipicamente para SNAT)
* Reglas: Define el criterio de filtrado y acciones a ser tomada en cada paquete. Suele consistir en una condición de coincidencia y us correspondiente acción, aceptar o descartar.
* Conjuntos: Permite agrupar múltiples elementos tales como ip's, puertos o direcciones MAC en un único objeto que puede ser referenciado en las reglas. Permite manejar un número complejo de reglas de forma más sencilla y eficiente.

![Essential Nfttables ruleset ](https://thermalcircle.de/lib/exe/fetch.php?w=700&tok=277ef3&media=linux:nf-hooks-nftables-ex2.png)

### Manejo básico de nftables 

```bash
nft list ruleset
nft flush ruleset
nft list ruleset > /etc/nftables.conf
```

#### Creando tablas y cadenas.
```bash
nft list tables
nft list table ip filter
nft add table <family> <name>
nft add table ip filter 

nft list chains
nft add chain <family> <table> <chain>
nft add chain ip filter input
nft add table ip nat 
nft add chain ip nat postrouting { type nat hook postrouting priority 100 \; policy accept \; }
```

#### Creando conjuntos (sets)
```bash
nft add set inet example_table example_set { type ipv4_addr \; }
nft add set inet example_table example_set { type ipv4_addr \; flags interval \; } #permite rango ip
nft add element inet example_table example_set { 192.0.2.1, 192.0.2.2 }
nft add element inet example_table example_set { 192.0.2.0-192.0.2.255 }
nft list sets
```




> [!IMPORTANT]
> **Actividad** 
> * Crea una tabla denominada _asir2_table_ para los paquets ipv4 e ipv6 , dentro de ella una cadena denomindada _asir2_chain_ asociada al _hook_ output con política por defecto _reject_
>	* ¿Qué significa esto?
>	* Propón algún ejemplo práctico con algún comando básico que permita demostrar el efecto de estas reglas.
> * Crea un conjunto _set_ de direcciones ipv4 denominado ip_admin, añade varias direcciones en él.
>	* Comprueba que efectivamente se han creando los conjuntos de valores.
>	* Propón y crea un conjunto de valores (no basado en direcciones ip) que creas puede ser de utilidad en la definición de reglas de un cortafuegos. Justifica tu respuesta.






nft add rule ip nat postrouting oifname "wan" masquerade



```
Para navegar en la internet, necesitamos utilizar una ip pública, para ello activaremosa traducción de direcciones privadas a públicas (NAT) en el cortafuegos
```bash
firewall# iptables -t nat -A POSTROUTING -o eth3 -j MASQUERADE
```

Para guardar la regla anterior de forma persistente, utilizamos el comando _netfilter-persistent_
```bash
vagrant@fw:$sudo netfilter-persistent save
```
Probamos conectividad desde las diferentes máquinas

```bash
vagrant@lan:$ ping 10.0.82.1
vagrant@lan:$ ping 10.0.82.200
vagrant@lan:$ ping 10.0.200.100
vagrant@lan:$ ping 192.168.82.100
vagrant@lan:$ ping yahoo.es
```

> [!IMPORTANT]
> Es importante verificar que lo hecho hasta ahora funciona correctamente apagadas las máquinas.
> Reinícilas _vagrant reload_ y prueba conctividad de nuevo.

> [!NOTE]
> El alumno deberá implementar el resto de reglas según se detalla en el siguiente apartado.
 

### Firewall - Reglas
![network_diagram]({% link /resources/img/network_diagram.png %})
- [ ] Permitir el tráfico desde el interfaz loopback
- [ ] No se permite el trafico entrante (dirigido a) ni saliente (generado por) del cortafuegos, exceptuando el tráfico _ssh_ proveniente desde nuestr ordenador anfitrión y el ordenador del profesor 192.168.82.101
- [ ] No se permite el tráfico de la red _dmz_ a la red _lan_ exceptuando el tráfico _ldap_ dirigido a al servidor _ldap_.
- [ ] No se permite el tráfico saliente (generado por) de la red _dmz_ exceptuando el mencionado en el apartado anterior
- [ ] Se permite el tráfico de la red lan a la red dmz
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

![iptables chains]({% link /resources/img/iptables-in-linux.webp %})


![iptables-chains](https://miro.medium.com/v2/resize:fit:720/format:webp/1*Vs4XnYTCI4fXYuGl2V3xfw.png)

**Contrack**: Seguimiento de paquetes
>[!NOTE]
TCP es un protocolo basado en conexión, por lo que una conexión ESTABLISHED esta bien definida. UDP es un protocolo no orientado a conexión, por lo que ESTABLISHED hace referencia a tráfico que ha tenido una respuesta y viceversa.

![iptables_conntrack_2]({% link /resources/img/iptables_conntrack_2.png %})


![iptables_conntrack_3]({% link /resources/img/iptables_conntrack_3.png %})
## Links
* [iptables-essentials](https://www.digitalocean.com/community/tutorials/iptables-essentials-common-firewall-rules-and-commands)
* [How To Implement a Basic Firewall Template with Iptables on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-implement-a-basic-firewall-template-with-iptables-on-ubuntu-20-04)
* [iptables, un manual sencillo](https://fp.josedomingo.org/seguridadgs/u03/iptables.html)
* [Instalación de dnsmasq en Ubuntu 22.04](https://www.ochobitshacenunbyte.com/2024/11/25/dnsmasq-configuracion-de-dns-y-dhcp-en-linux/)
* [How to use static IP addresses](https://netplan.readthedocs.io/en/stable/using-static-ip-addresses/)


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

## Anexo III. Firewall - Reglas - soluciones

- [x] Permitir el tráfico desde el interfaz loopback
```bash
vagrant@fw:$sudo iptables -A INPUT -i lo -j ACCEPT
vagrant@fw:$sudo iptables -A OUTPUT -o lo -j ACCEPT
```
- [x] No se permite el trafico entrante (dirigido a) ni saliente (generado por) del cortafuegos, exceptuando el tráfico _ssh_ proveniente desde nuestr ordenador anfitrión y el ordenador del profesor 192.168.82.101

```bash
vagrant@fw:$sudo iptables -A INPUT -p tcp -s 10.0.2.2 --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
vagrant@fw:$sudo iptables -A OUTPUT -p tcp -d 10.0.2.2 --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT

vagrant@fw:$sudo iptables -A INPUT -p tcp -s 192.168.82.101 --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
vagrant@fw:$sudo iptables -A OUTPUT -p tcp -d 192.168.82.101 --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT
```
- [x] Aplicamos una política restrictiva
```bash
vagrant@fw:$sudo iptables -t filter -P INPUT DROP
vagrant@fw:$sudo iptables -t filter -P OUTPUT DROP
```

- [x] Permitir tráfico desde la interfaz loopback
```bash
vagrant@fw:$sudo iptables -A INPUT -i lo -j ACCEPT
vagrant@fw:$sudo iptables -A OUTPUT -o lo -j ACCEPT
```

- [x] Aplicar una política restrictiva a la cadena FORWARD y abrir los puertos necesarios
```bash
iptables -t filter -P FORWARD DROP
```

- [x] No se permite el tráfico del servidor ldap a la red dmz exceptuando el establecido (iniciado en dmz)
```bash
iptables -A FORWARD -i eth1 -o eth2  -s 10.0.82.200 -d 10.0.200.0/24 -m conntrack --ctstate NEW -j DROP
```

- [x] No se permite el tráfico de la red _dmz_ a la red _lan_ exceptuando el tráfico _ldap_ dirigido a al servidor _ldap_.

```bash
iptables -A FORWARD -i eth2 -o eth1 -p udp -d 10.0.82.200 --dport 389 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i eth1 -o eth2 -p udp -s 10.0.82.200 --sport 389 -m conntrack --ctstate ESTABLISHED -j ACCEPT
iptables -A FORWARD -i eth2 -o eth1 -p tcp -d 10.0.82.200 --dport 389 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i eth1 -o eth2 -p tcp -s 10.0.82.200 --sport 389 -m conntrack --ctstate ESTABLISHED -j ACCEP
```
- [x] No se permite el tráfico saliente (generado por) de la red _dmz_ exceptuando el mencionado en el apartado anterior


- [x] Se permite el tráfico de la red lan a la red dmz
```bash
vagrant@fw:$sudo iptables -A FORWARD -i eth1 -o eth2  -s 10.0.82.0/24 -d 10.0.200.0/24 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
vagrant@fw:$sudo iptables -A FORWARD -i eth2 -o eth1  -s 10.0.200.0/24 -d 10.0.82.0/24 -m conntrack --ctstate ESTABLISHED -j ACCEPT
```

- [x] Se permite el tráfico al exterior (wan) generando en la red _lan_, exceptuando el tráfico proveniente del servidor _ldap_
```bash
vagrant@fw:$sudo iptables -A FORWARD -i eth3 -o eth1  ! -d 10.0.82.200 -m conntrack --ctstate ESTABLISHED -j ACCEPT
vagrant@fw:$sudo iptables -A FORWARD -i eth1 -o eth3  ! -s 10.0.82.200 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
```
- [x] Se permite el tráfico http/s del exterior dirigido a la _dmz_
```bash
vagrant@fw:$sudo iptables -A FORWARD -i eth3 -o eth2 -p tcp -m multiport --dports 80,443 -d 10.0.200.100 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
vagrant@fw:$sudo iptables -A FORWARD -i eth2 -o eth3 -p tcp -m multiport --sports 80,443 -s 10.0.200.100 -m conntrack --ctstate ESTABLISHED -j ACCEPT
```
- [x] Las peticiones provenientes del exterior al puerto 80/443 (http/s) serán redirigidas al servidor web de la _dmz_
```bash
vagrant@fw:$sudo iptables -t nat -A PREROUTING -i eth3 -p tcp --dport 80 -j DNAT --to-destination 10.0.200.100:80
vagrant@fw:$sudo iptables -t nat -A PREROUTING -i eth3 -p tcp --dport 443 -j DNAT --to-destination 10.0.200.100:443
```
