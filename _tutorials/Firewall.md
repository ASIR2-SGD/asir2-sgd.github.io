---
layout: default
title: "firewall"
---
# Firewall.

## Contexto
Los cortafuegos se utilizan con frecuencia para evitar que otros  usuarios de Internet no autorizados tengan acceso a las redes privadas  conectadas a Internet. Estos suelen actuar como un organismo de  inspección que verifica las conexiones que se establecen entre una red y un equipo local. Un cortafuegos regula, por lo tanto, la comunicación  entre ambos para proteger el ordenador contra programas maliciosos u  otros peligros de Internet.


## Objetivos
* Virtualizar el escenario necesario para llevar a cabo la práctica
* Conocer el funcionamiento de un cortafuegos basado en tablas y cadenas
* Crear las reglas en iptables
* Ser capaz de configurar el cortafuegos según las especificaciones del problema


## Netfilter

Netfilter es una infraestructura integrada en el kernel de linux que permite interceptar y manipular paquetes de red, actuando como el motor principal de un _firewall_ para filter el tráfico y realizar NAT, utilizando herramientas como _iptables o _nfttables_ para definir políticas y réglas sobre los interfaces de red, organizadas en tablas y cadenas.
Netfilter maneja el trafico de red en diferentes puntos (__hooks__) a medida que pasa por el sistema. _nftables_ y su antecesor _iptables_ nos permite a nivel de usuario _anclar_ una cadena de reglas (callback function) en cada uno de los _hooks_ pudiendo descartar o aceptar paquetes según la política de seguridad deseada


![Netfilter hooks -simple block diagram](https://thermalcircle.de/lib/exe/fetch.php?w=700&tok=37d6df&media=linux:nf-hooks-simple1.png)


## nftables


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

### Contrack: Seguimiento de paquetes

>[!NOTE]
>TCP es un protocolo basado en conexión, por lo que una conexión ESTABLISHED esta bien definida. UDP es un protocolo no orientado a 
>conexión, por lo que ESTABLISHED hace referencia a tráfico que ha tenido una respuesta y viceversa.

![iptables_conntrack_2]({% link /resources/img/iptables_conntrack_2.png %})


![iptables_conntrack_3]({% link /resources/img/iptables_conntrack_3.png %})

### Nftables 

#### Instalación
```bash
sudo apt-get -y install nftables
systemctl enable nftables.service
systemctl start nftables.service
systemctl status nftables.service
```

#### Listado reglas y persistencia

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
nft delete table ip nat

nft list chains
nft add chain <family> <table> <chain>
nft add chain ip filter input
nft add table ip nat 
nft add chain ip nat postrouting { type nat hook postrouting priority 100 \; policy accept \; }
nft add chain family mytable mychain '{ policy drop; }'
nft delete chain ip nat postrouting
```

#### Creando conjuntos (sets)
```bash
nft add set inet example_table example_set { type ipv4_addr \; }
nft add set inet example_table example_set { type ipv4_addr \; flags interval \; } #permite rango ip
nft add element inet example_table example_set { 192.0.2.1, 192.0.2.2 }
nft add element inet example_table example_set { 192.0.2.0-192.0.2.255 }
nft list sets
```


**Responde I. nfttables basics** 
1. Crea una tabla denominada _asir2_table_ para los paquets ipv4 e ipv6 , dentro de ella una cadena denomindada _asir2_chain_ asociada al _hook_ output con política por defecto _reject_
2. ¿Qué significa esto?
3. Propón algún ejemplo práctico con algún comando básico que permita demostrar el efecto de estas reglas.
4. Crea un conjunto _set_ de direcciones ipv4 denominado ip_admin, añade varias direcciones en él.
5. Comprueba que efectivamente se han creando los conjuntos de valores.
6. Propón y crea un conjunto de valores (no basado en direcciones ip) que creas puede ser de utilidad en la definición de reglas de un cortafuegos. Justifica tu respuesta.

#### Logging and rate limit
Podemos registar la actuación de las reglas del cortafuegos y limitar el número de paquetes con propósito de auditoria y evitar ciertos ataques.

```bash
sudo nft add rule inet my_filter_table input tcp dport 22 log prefix "SSH Drop:" level warning
sudo nft add rule inet my_filter_table input tcp dport 22 drop
sudo nft add rule inet my_filter_table input icmp type echo-request limit rate 10/second accept
sudo nft add rule inet my_filter_table input icmp type echo-request drop
```

### Reglas. La Lógica

#### Match Expresion

| Protocol matching  | |
| --------------| -----------------------|
| tcp dport 22 	| TCP destination port |
| udp sport 53	| UDP source port 	|
| icmp type echo-request | ICMP type |
| ip protocol tcp | IP protocol |

| Address matching | |
| --------------| -----------------------|
| ip saddr 192.168.1.0/24 | Source IP range |
| ip daddr != 10.0.0.0/8 | Destination IP (not) |
| ip saddr { 1.2.3.4, 5.6.7.8 } | Multiple IP Interface matching |
| iif eth0 | Input interface |
| oif "wlan*" | Output interface (wildcard) |
| iifname "docker0" | Interface by name |

| Connection tracking | |
| --------------| -----------------------|
| ct state established |  Connection state |
| ct state new,related |  Multiple states |
| ct direction original |  Connection direction |

| Time-based matching | |
| --------------| -----------------------|
| meta hour "09:00"-"17:00" |  Time range |
| meta day { "Monday", "Friday" } |  Specific days 

|Packet properties | |
| -----------------| ---------------- |
| meta length 40-100 | Packet size range |
| meta mark 0x123 |  Packet mark |
| meta priority 0 |  Priority

#### Sentencias (Acciones)

|  Basic actions | |
| --------|----------|
| accept |  Allow packet |
| drop |  Silent drop |
| reject |  Send rejection |
| return |   Return to calling chain |


|  Logging | |
| --------|----------|
| log |  Basic logging |
| log prefix "SSH: " |  With prefix |
| log level emerg | Log level Counters and statistics|
| counter | Count packets/bytes |
| counter packets 100 bytes 8000 |  Set initial values |

|  Target modification | |
| --------|----------|
| snat to 1.2.3.4 |  Source NAT |
| dnat to 192.168.1.10 |  Destination NAT |
| masquerade | Dynamic SNAT |

|  Packet modification | |
| --------|----------|
| meta mark set 0x123 |  Set packet mark |
| meta priority set 0 |  Set priority |

|  Rate limiting | |
| --------|----------|
| limit rate 10/minute |  Basic rate limiting |
| limit rate over 100/minute drop |  Burst protection |

|  Advanced actions | |
| --------|----------|
| queue |  Send to userspace |
| dup to device eth1 |  Duplicate packet |

**Responde II. Reglas nftables** 
1. Crea una regla que acepte las conexiones _ssh_ del interfaz _eth0_
2. Crea una regla que permita el tráfico entre el interfaz enp2s0 y enp1s0
3. Crea un conjunto denominado _inernal_nets_ con varias redes ipv4
3. Crea una regla que acepte las conexiones ip provenientes del conjunto _internal_nets_ creado en el paso anterior.
3. Crea una regla que aplique _masquerade_ a los paquetes salitenes por el interfaz "eth0"
3. Crea una regla que aplique _masquerade_ a los paquetes salitenes por el interfaz "eth0" y provenientes del conjunto _internal_nets_
3. El servidor _ldap_ se encuentra en la ip 10.10.10.11. Haz _port-forwarding_ si el paquete proviene de la interfaz "wan" y va dirigido al puerto usado por el servicio _ldap_
3. Crea una regla que cambie la dirección de destino a 10.1.0.10 si el paquete va dirigido a los puertos 80 o 443
3. Crea una regla que accepte las conexiones cuyo esado sea _new_, _established_ o _related_.
3. Crea una regla para que el servidor web únicamente acepte 100 paquetes por minuto y ráfagas cortas de 200.
3. Crea una regla que deniege las conexiones cuyo estado sea _invalid_.
3. Crea una regla para que el servidor _ssh_ acepte únicamente 50 paquetes por minuto.
3. Crea una regla para que los paquetes _ssh_ descartados se registren con el prefijo _"SSH rate limit exceeded: "_.
3. Crea un conjunto denominado _port_scanners_ e incluye varias ip de ejemplo
3. Referencia el conjunto anterior en una regla que deniege el acceso si proviene de alguna de las ips del conjunto.
3. Crea una cadena denominada _input_wan_ que permita el tráfico _icmp_ de tipo _echo-request_ y el _udp_ dirigido al puerto 68 (DHCP). Deniega el resto
3. Crea en una tabla denominada _asir2_table_ una cadena_base denominada _asir2_input_ asocianda al punto (hook) input. Para todo el tráfico proveniente del interfaz "eth0" salta a la cadena creada en el paso anterior.


#### Añadir, insertar y eliminar reglas
```bash
nft add rule <family> <table> <chain> <match expresion> <action>
nft add rule inet filter input  iifname "eth0" tcp dport {443, 80} accept
# inserta reglas en una posición específica
nft -a list table inet filter
nft add rule inet filter input position 123 iifname "eth0" tcp dport {443, 80} accept #before position
nft insert rule inet filter input position 123 iifname "eth0" tcp dport {443, 80} accept #after position
nft delete rule inet filter input handle 178
```

**Responde III. Estudio reglas nft-incus** 
1. A partir del siguiente [fichero](https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/resources/files/nft-incus.txt) de reglas usadas por el servidor _incus_
2. Analiza las reglas indicando y enumerando el número de cadenas y tablas
3. Explica a modo general y usando un lenguaje natural las reglas de la cadena _in.incusbr0_
4. Explica en el contexto el propósito de la única regla en la cadena pstrt.incusbr0




## Actividad I. Configuración de un cortafuegos con nftables
Para llevar a cabo la práctica necesitamos tres contenedores (_firewall_ , _lan1_ y _lan2_) y un switch virtual (_ovs-br0_)

### Diagrama de red
1. Dibuja un diagrama de red **hecho a mano** del escenario propuesto, indicando los interfaces e ip's


Crea el cortafuegos y añadele un segundo interfaz de red denominado _lan_, renombra el interfaz _eth0_, creado por defecto a _wan_ para mayor claridad.

```bash
$ incus launch images:ubuntu/noble firewall
$ incus config device override firewall eth0 name=wan
$ incus config device add firewall eth1 nic name=lan nictype=bridged parent=ovs-br0
# Aprovisionamiento básico del firewall
$ incus exec firewall -- bash -c 'apt-get update && apt-get -y install  aptitude wget bash-completion nano xsel vim dnsmasq nftables' 
$ incus exec firewall -- bash -c 'systemctl enable nftables.service'
# Creación de los clientes
$ incus launch images:ubuntu/noble lan1 --network ovs-br0
```

### Basic firewall config
**Pasos**

1. El interfaz _eth1_ que conecta con la LAN tiene que tener una ip estática. Lleva a cabo la configuración de red apropiada para dicha interfaz y aplicando los cambios mediante la utilidad _netplan_. 
	* La ip para el interfaz _lan(eth1)_ debe ser 10.10.82.1. 
	* Los cambios en la configuración de red se llevarán a cabo creando un nuevo fichero (básate en _/etc/netplan/10-lxc.yaml_) _/etc/netplan/20-firewall.yaml_
2. El _firewall_ deberá implementar funcionalidad DHCP para proveer a sus clientes LAN de ip dinámica. Lleva a cabo la configuración del servidor DHCP usando _dnsmasq_.
Lleva a cabo la configuración y comprueba que los clientes LAN obtienen una ip de la red 10.10.82/0

> [!WARNING]
> El servidor DNS de _dnsmasq_ colisiona a hacer uso que el mismo puerto 53 que el servicio _systemd-resolve_, para evitar este problema y que ambos servidores DNS funcionen correctamente, deberás descomentar en el fichero _/etc/dnsmasq.conf_ la linea _bind-interfaces_ y asignar la interfaz _lan_ como la interfaz de escucha de peticiones DNS y DHCP 


Para que el _firewall_ actue como enrutador y redirecciones los paquetes a la interfaz de salida apropiada, debemos activar _forwarding_
De forma temporal mediante el comando
```bash
firewall# sysctl -w net.ipv4.ip_forward=1
```
Hacemos el cambio persistente editando el fichero _/etc/sysctl.conf_ y descomenta la linea 28

```bash
firewall# vi /etc/sysctl.conf
28 net.ipv4.ip_forward=1
```
Aplica los cambios reiniciando el servicio _systemd-sysctl_
```bash
firewall# systemctl restart systemd-sysctl.service 
```


### Firewall config II 
**Pasos**

En este momento, y aunque hemos configurado el _firewall_ como enroutador, **NO** es posible salir a _internet_ con los clientes lan. Analiza y entiende el problema llevando a cabo las modificaciones necesarias en las reglas del _firewall_ para permitir la salida de los clientes al exterior.
1. Comprueba que los clientes _lan_ obtienen ip del _firewall_ en la red apropiada.
2. Comprueba que en un principo no pueden salir al exterior
3. ¿Porqué los clientes aunque obtienen ip y hemos activado el contenedor como enrutador no pueden acceder a la wan?
3. Añade las reglas apropiadas el _firewall_ para permitir a los clienes acceder a la wan

Las respuestas de las siguiente reglas se deben de acompañar con el comando y breve explicación que verifique que efectivamente, la regla tiene el efecto deseado.
- [ ] Aplicar una política restrictiva a la cadena input/output/forward
- [ ] Permitir el tráfico desde el interfaz loopback
- [ ] Con el objetivo de permitir los servicios mínimos, en el cortafuegos, permite el tráfico entrante para: 
	* ICMP
	* _ssh_
	* Peticiones DHCP
	* Peticiones DNS	
- [ ] Con el objetivo de permitir los servicios mínimos, en el cortafuegos, permite el tráfico saliente para: 
	* Actualizaciones del sistema 
	* Peticiones DNS
	* Conexiones _legítimas_ (established, related)
	* ICMP
- [ ] Permitir que atraviese (forward) el cortafuegos únicamente el trafico proveniende de la LAN



## Actividad 2. DMZ
Una DMZ Zona Desmilitarizada) es una red perimetral segura y aislada en una infraestructura de red, diseñada para alojar servidores y servicios que necesitan ser accesibles desde Internet (como servidores web, de correo, DNS) sin comprometer la seguridad de la red interna (LAN).

* Añade una tercera interfaz denominada _dmz(eth2)_ con la ip 10.10.100.1/24
* Crea un servidor web de prueba o utiliza uno ya existente y modifica la configuración de red para conectarlo a la red DMZ (deberas usar un switch virtual ovs-br1)

A las reglas del cortafuegos del ejercicio anterior, añade las siguientes relacionadas con la seguridad del la zona DMZ
* No se permite ningún tráfico entre la LAN y DMZ excepto el trafico HTTP/S
* No se permite el tráfico entre DMZ y LAN/WAN excepto el tráfico legítimo 
* Se permite el tráfico _ssh_ hacia el servidor _web_ provieniente únicamente del cliente _lan1_
* Las conexiones provenientes de wan al puerto 80,433 deben redirigirse al servidor web (DNAT)

### Entrega
Envia un documento _pdf_ firmado (creado con _markdown_) con los siguientes apartados
* Diagrama lógico de red *hecho a mano* indicando las redes existentes(id.red/máscara) ip's e interfaces de red
* Comandos y breve explicación cuando así lo requiera, ejecutados.
* Respuestas a las preguntas planteadas.
* Anexos con los ficheros de configuración más relevantes usados en la práctica.


### Propuestas de mejora
Las siguientes propuestas de mejora de la práctica se plantean al alumno como reto para que mejore sus destrezas y conocimientos de las herramientas de administrdor de sistemas y mejore **notablemente** su nota de la asignatura.

* **Mejora I-** Automatiza la creación y configuración del escenario propuesto para el la práctica 1 que has llevado a cabo mediante el uso de un fichero _Taskfile.yml_ 
* **Mejora II-** Amplia y experimenta tus conocimientos instalando y configurando en un entorno virtual igual al propuesto el cortafuegos basado en FreeBSD, Opensense. Puedes encontrar los pasos esquematizados en la sección extra de los apuntes
* **Mejora III-**Basándote en la mejora anterior, utiliza la herramienta _ansible_ para automatizar el proceso de configuración del escenario de la práctica.


---
[NO TERMINADA]

## Actividad 3. OpenWRT 


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


> [!TIP]
> Se metódico y cuidadoso a la hora de establecer las reglas. Crea un fichero (script) bien documentado con a medida que vas añadiendolas. Comprueba el efecto de cada una y ejecuta los _tests_ de regresión para verificar que las reglas añadidas no rompen el estado anterior.



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



## Links
* [iptables-essentials](https://www.digitalocean.com/community/tutorials/iptables-essentials-common-firewall-rules-and-commands)
* [How To Implement a Basic Firewall Template with Iptables on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-implement-a-basic-firewall-template-with-iptables-on-ubuntu-20-04)
* [iptables, un manual sencillo](https://fp.josedomingo.org/seguridadgs/u03/iptables.html)
* [Instalación de dnsmasq en Ubuntu 22.04](https://www.ochobitshacenunbyte.com/2024/11/25/dnsmasq-configuracion-de-dns-y-dhcp-en-linux/)
* [How to use static IP addresses](https://netplan.readthedocs.io/en/stable/using-static-ip-addresses/)
