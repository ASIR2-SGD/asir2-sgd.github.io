---
layout: default
title: Kerberos
---
# Kerberos

Kerberos es un protocolo de autenticación de red que permite a usuarios y servicios verificar sus identidades de forma segura en redes inseguras, usando un tercero de confianza (el KDC) y criptografía de clave secreta para emitir "tickets" digitales, evitando enviar contraseñas por la red. Permite el inicio de sesión único (SSO), autenticando al usuario una sola vez para múltiples servicios.

# Arquitectura
## Componentes
![Componentes Kerberos](https://miro.medium.com/v2/resize:fit:720/format:webp/1*NbvqDTvTl8RS49dtFHjG7A.png)
## Protocolo
### Analogía feria atracciones
![Kerberos protocol 2]({% link /resources/img/Kerberos02.png %})

> Una forma de  pensar en  el uso de Kerberos  es  imaginar que  vas a  un  parque de atracciones.
> Cuando  llegas al  parque, te diriges  a  la puerta principal. Luego, te diriges a la taquilla principal (el servidor de autenticación en el centro de distribución de claves) y compras un pase de un día para el parque (un ticket que te da acceso).

>  Recibes una pulsera *morada* (porque el morado es el color del miércoles) que indica que has pagado la entrada para ese día y que tienes acceso completo al parque. La pulsera de color es válida para todo el día.

> Mientras estás en el parque, debes adquirir entradas adicionales para las atracciones.  Te acercas a la taquilla de la atracción (servidor de tickets) y la empleada se da cuenta de que llevas una pulsera *morada*. Le dices que quieres montarte en la montaña rusa. Ella te expide un ticket (ticket de sesión) para la montaña rusa.

>  Cuando llegas a la montaña rusa, el encargado de la montaña rusa ve tu pulsera morada y acepta el ticket que te ha dado la taquillera. El encargado de la montaña rusa no necesita consultar con la taquillera porque ese es el único lugar donde podrías haber conseguido ese ticket. 

> Al  final del  día,  cuando  cierra el parque, la pulsera morada del miércoles ya no te identifica.  El color de la pulsera del jueves es naranja. También te diste cuenta de que tú hiciste todo el trabajo. Ninguno de los vendedores de entradas ni los operadores de las atracciones se comunicaron entre sí.  Dependía de ti.

![Kerberos protocol 1](https://danlebrero.com/images/kerberos-for-dummies-2.jpg)
___
![Kerberos protocol 2]({% link /resources/img/Kerberos01.png %})

![Kerberos protocol 3](https://www.varonis.com/hubfs/Imported_Blog_Media/Kerberos-Graphics-1-v2-787x790.jpg)


## Actividad I. Autenticación en un servidr ssh mediante kerberos
### Guión esquemático

> 1. Crea la red krb-net
> 2. Crea las instancias necesarias
> 2. Crea,configura y comprueba el correcto funcionamiento del servidor dns para la red krb-net.
> 3. Configurar el KDC añadiendo los prear, modificar y activar tu web site basándote en el fichero existente _/etc/apache/sites-available/default-ssl.conf_
> 4. ....


Crea una red denominada krb-net para experimentar y aprender el funcionamiento del protocolo _kerberos_. La red formada por el KDC, un cliente y un servidor ssh _kerberizado_, permitirá una vez autenticado el cliente y obtenido el TGT, solicitar el TS al servidor ssh y acceder a el sin necesidad de presentar las credenciales (usuario/contraseña)

| Realm | Primary KDC | User principal | Admin principal |
| ----------|----------| ----------| ------------|
| ASIR2.GRAO | kdc01.asir2.grao | ubuntu | ubuntu/admin |

### Escenario en Incus
Para llevar a cabo la práctica, deberemos construir el siguiente escenario con contenedores
* Servidor de nombres 
* KDC
* krb-cli
* ssh-server

Las máquinas _KDC_, _krb-cli_ y _ssh-server_ están en la red _krb-net_. La resolución de nombres, esencial para que el protocolo de autenticación Keberos, funcione correctamente la hace _dnssrv_

**Network**
* _Type_ : bridged managed
* _Name_ : krb-net
* _Net ip/mask_ : 10.144.144.0/24
* _nameserver_ : _ip-dnssrv_
* _search domain_ : asir2.grao

```bash
$ incus network create krb-net \
      ipv4.address=10.144.144.1/24 \
      ipv6.address=none ipv4.nat=true \
      ipv4.dhcp.ranges=10.144.144.100-10.144.144.200 \
      dns.nameservers=10.144.144.2 \
      dns.search=asir2.grao
```

### DNS
En el apartado anterior hemos creado la red _asir2.grao(10.144.144.0/24)_. Para el correcto funcionamiento de _kerberos_ es necesario disponer de un servidor DNS para dicha zona correctamente configurado. Este, tal y como le hemos indicando tiene una ip fija 10.144.144.2 que es la que que el servidor DHCP (10.144.144.1) pasará a sus clientes entre otros parámetros de red.
Será necesarios configurar el fichero _/etc/netplan/10-lxc.yaml_

```bash
$ incus launch images:ubuntu/noble dnssrv --network krb-net
```

Modifica la configuración de red del servidor dns y asignale una dirección fija
```bash
#/etc/netplan/10-lxc.yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: false
      dhcp-identifier: mac
      addresses: [10.144.144.2/24]
      nameservers:
        addresses: [10.144.144.2]
        search: [asir2.grao]
      routes:
        - to : default
          via: 10.144.144.1                           
```

Aplica los cambios mediante el comando _netplan apply_
Es necesario instalar en nuestro servidor de nombres de la zona _asir2.grao_ el paquete _bind9_ enre otras utilidades para que este actue como tal.
Nuestra configuración actual que podemos obtenerla mediante el comando _resolvectl status_ indica que el servidor de nombres para resolver nombres de domino es el mismo, por lo que es el pez que se muerde la cola.

> [!TIP]
> Podemos asignar de forma temporal un servidor de nombres para poder instalar los paquetes mediante el comando _resolvectl dns eth0 10.144.144.1_

Intala los paquetes necesarios.
```bash
$ incus exec dnssrv -- bash -c 'apt-get update && apt-get -y install  aptitude wget bind9 dnsutils bash-completion nano xsel vim'
```

**Responde:**

1. _¿Qué serie de pruebas has llevado a cabo para concluir que es la configuración del servidor de nombres la que no es correcta para poder instalar los paquetes, indica los comandos?_
2. _¿Quién es 10.144.144.1?,¿Por que lo has asignado como servidor de nombres?,¿Qué otras funciones tiene?_
3. _¿Habría funcionado si huberamos puesto los servidores de google 8.8.8.8 como servidores de nombre en nuestra configuración?. ¿Explica el motivo?_

Vamos ahora a configurar nuestro servidor de nombres para que sea responsable de la zona _asir2.grao_, esto quiere decir que es él quien tiene la responsabilidad de devolver la _ip_ correspondiente a las peticiones dentro del dominio _asir2.grao_.
Nuestro servidor de nombres actua como _caching nameserver_. Las peticiones que este no sepa resolver deberá reenviarlas a otro servidor de nombres.

> [!NOTE]
> Las siguientes indicaciones están basada sen el [tutorial](https://documentation.ubuntu.com/server/how-to/networking/install-dns/#install-dns) de configuración del servicio DNS de ubuntu. Se recomienda consultarlas para cualquier duda o aclaración.

```bash
#/etc/bind/named.conf.options
options {
    forwarders {
        10.144.144.1;        
    };
};
```




A continuación configuramos nuestro servidor como servidor primario de la zona a administrar _asir2.grao_

```bash
#/etc/bind/named.conf.local
zone "asir2.grao" {
    type master;
    file "/etc/bind/db.asir2.grao";
};
```

Creamos los registros para la zona

```bash
#/etc/bind/db.asir2.grao
;
; BIND data file for asir2.grao
;
$TTL    604800
@       IN      SOA     asir2.grao. root.asir2.grao. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL

@       IN      NS      ns.asir2.grao.
@       IN      A       10.144.144.2
ns      IN      A       10.144.144.2
#---------------
#Place your records here
#--------------
```

**Responde:**

4. _¿Qué es un _caching nameserver_ indica las características frente a un _DNS forwarder_
5. _¿Por que has indicando 10.144.144.1 como forwarders?. ¿Qué otros valores sería correcto poner?_
6. _¿Investiga cual es el servidor de nombres del IES?, ¿Qué comando has utilizado para saberlo?_
7. _Explica con tus propias palabras el siguiente registro_
>```@       IN    NS     ns.example.com.```


Para la resolución inversa (ip -> name)
```bash
#/etc/bind/named.conf.local
zone "144.144.10-in-addr.arpa" {
    type master;
    file "/etc/bind/db.144.144.10";
};
```

```bash
#/etc/bind/db.10.144.144
;
; BIND data file for 10.144.144
;
$TTL    604800
@       IN      SOA     ns.asir2.grao. root.asir2.grao. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL

@       IN      NS      ns.
2       IN      PTR 	ns.asir2.grao
#---------------
#Place your records here
#--------------
```

**Testeando el servidor DNS**

Es fundamental aprender a testear y comprobar las cosas y no dejar nada al libre albedrio, que será en un alto porcentaje susceptible de fallos y problemas.

Una herramienta muy util para realiza consultas a un servidor de nobres es **dig**
```bash
dig @10.144.144.2 kdc.asir2.grao A
dig @10.144.144.2 asir2.grao SOA
dig @10.144.144.2 asir2.grao NS
``` 

Para verifira si nuestro fichero de zona es correcto y se carga correctamente podemos utilizar el comando _named-checkzone_
**Responde:**

8. _Ejecuta y explica que hacen las consultad del comando dig anteriores_
9. _¿A que servidor de nombres realizamos la consulta si omitimos el parámetro @10.144.144.2?_
10. _Investiga sobre el comando [_named-checkzone_](https://documentation.ubuntu.com/server/how-to/networking/install-dns/#named-checkzone)e indica el comando que ejecutarías para verificar que el fichero de zona asir2.grao es correcto_


## Kerberos 
[Guía instalación y configuración kerberos server](https://documentation.ubuntu.com/server/how-to/kerberos/install-a-kerberos-server/)
### KDC 

```bash
$ incus launch images:ubuntu/noble kdc --network krb-net
$ incus exec kdc -- bash -c 'apt-get update && apt-get -y install  aptitude wget krb5-kdc krb5-admin-server bash-completion nano xsel vim' 
```

> [!WARNING]
> Kerberos confia en la resolución de nombres, por lo que es importante tener un servidor _DNS_ correctamente configurado y con los registros necesarios para el correcto funcionamiento del _KDC_.

> [!TIP]
> _kinit_ inspecciona el fichero _/etc/krb5.conf_ para encontra con que _KDC_ contactar. Esto tiene el inconveniente que en un despliege con cientos de clientes, si modificamos la ip del _KDC_ deberemos reflejar ese cambio en el fichero. El _KDC_ puede ser encontrado via busquedas DNS, para ello debes añadir registros _TXT_ y _SRV_ a tu servidor de nombres.
> Mejora tu calificación llevando la mejora mencionada.


### krb-cli
```bash
$ incus launch images:ubuntu/noble krb-cli --network krb-net
$ incus exec krb-cli -- bash -c 'apt-get update && apt-get -y install  aptitude wget krb5-user krb5-config bash-completion nano xsel vim'
root@kdc-client:~# kinit ubuntu
root@kdc-client:~# klist
```

**Responde:**

11. _¿Qué diferencias hay entre el comando kadmin.local y kadmin?,¿Por qué esa diferenciación?_
12. _¿Qué hace el comando `addprinc`?_
13. _¿Para que sirve el fichero /etc/krb5kdc/kadm5.acl? ¿Que significado tiene la regla?_
>```*/admin@EXAMPLE.COM    *```
14. _Explica con tus propias palabra que hace el comando kinit y el comando klist_


### Servidor SSH Kerberizado
```bash
$ incus launch images:ubuntu/noble ssh-server --network krb-net
$ incus exec ssh-server -- bash -c 'apt-get update && apt-get -y install krb5-user krb5-config openssh-server aptitude wget bash-completion nano xsel vim'
root@ssh-server-k:~# kinit ubuntu/admin
root@ssh-server-k:~# klist
root@ssh-server-k:~# kadmin
kadmin: add_principal -randkey host/ssh-server.asir2.grao@ASIR2.GRAO
kadmin: ktadd host/ssh-server.asir2.grao
klist -ke /etc/krb5.keytab 
```
**Responde:**

15. _¿Explica el comando ktadd y situalo en el contexto de la práctica?,¿Por qué hay que usarlo?_
16. _¿Dentro del contexto de kerberos, que es un SPN, enumero un SPN usado en la práctica?_
17. _Dentro del contexto de kerberos, define y ejemplifica con tus propias palabras los siguietes términos. Busca una analogia del mundo real asociando los términos:_
	* TGS 
	* TGT
	* TS
	* AS


## Entrega
* Entrega un documento **estructurado** con una breve explicación(función) de los comando usados para la configuración tanto del cliente como del servidor así como de los pasos llevados a cabo para la comprobación de correcto funcionamiento de la actividad.
* Completa el documento con un diagrama de red **hecho  a mano** de la red de la actividad.
* Completa el documento con un diagrama temporal **hecho a mano**, similar al estudiado en clase que explique de forma gráfica los pasos para autenticarse mediante el protocolo _kerberos_ a un servicio. 
	* La clave del usuario es de color naranja
	* La clave del servicio (MySql) es de color morado
	* Enumera los pasos llevados a cabo y una breve explicación de lo que hace cada uno y que se obtiene.
* Completa el documento con anexos de los ficheros de configuración (sin comentario ni espacios en blanco) usados.
* Responde a las preguntas propuestas durante la realización de la práctica.

Utiliza el formato _markdown_ adecuado para tener un documento estructurado y legible.

### Propuestas de mejora
Las siguientes propuestas de mejora de la práctica se plantean al alumno como reto para que mejore sus destrezas y conocimientos de las herramientas de administrdor de sistemas y mejore su nota en la asignatura.

* **Mejora I-Obtención del KDC a través de DNS queries** Añade las entradas correspondienes en el servidor DNS para obtener la ip del servidor KDC mediante consultas DNS
* **Mejora II-Kerberizando servicios** Mejora tus conocimientos sobre kerberos así como tu calificación en la asignatura llevando a cabo la _kerberización_ del servidor de un servicio, que pueden ser un servidor web, una base de datos(MySQL, Hive, Spark) un servicio de carpetas compartidas (NFS, Samba) u otro servicio a tu elección. Busca información reslacionada en internet con las siguienes palabra clave _<servicio> kerberized_.
* **Mejora III-Automatización** Automatiza la creación y configuración del escenario mediante un _taskfile.yaml_ mejorando notablemente tus conocimiento de _scripting_. Da un paso más allá y prueba a automatizar la configuración del servidor DNS así como la del servidor _ssh_



## Links
* [Kerberos explained in pictures]https://danlebrero.com/2017/03/26/Kerberos-explained-in-pictures/
* [Kerberos Authentication Explained](https://www.youtube.com/watch?v=5N242XcKAsM&t=18s)
* [Introduction to Kerberos](https://documentation.ubuntu.com/server/explanation/intro-to/kerberos/)
* [Configuring OpenSSH to use Kerberos Authentication](https://www.kevindiaz.dev/blog/configuring-openssh-to-use-kerberos-authentication.html)
* [How to Integrate LDAP and Kerberos](https://www.linuxtoday.com/blog/integrate-ldap-kerberos/)
* [Kerberizando SSH en Linux](https://juanjoselo.wordpress.com/2018/02/18/kerberizando-ssh-en-linux/)
* [Domain Name Service (DNS)](https://documentation.ubuntu.com/server/how-to/networking/install-dns/#install-dns)



## Anexo I. Glosario de términos
* _KDC_ : Key Distribution Center. Cerebro de Kerberos. Está dividido en tres partes ejecutados en un mismo proceso.
	* _Database_: Contiene los _principals_ y sus contraseñas asociadas. Las contraseñas no son usadas directamente, se genera una _key_ a partir de la contraseña (salt) que es usada para encriptar mensajes.
	* _Authentication Server (AS)_: Punto de entrada para el cliente cuando interactua con el protocolo de autenticación Kerberos. Emite _TGT_ 
	* _Ticket Granting Service (TGS)_: Responsable de emitir al cliente un tiquet que permite al cliente autenticarse en un servicio. Emite _Service Tickets_. El cliente envía al TGS el TGT obtenido del AS y solicita al TGS un tiquet para un servicio en concreto.
* _keytab_: fichero que contiene datos encriptados como las contraseñas para los _pricipals_ (usuarios o servicios)
* _principal_: Cualquier entidad dentro del dominio Kerberos (usuarios, hosts y servicios) posee un identificador único así como una contraseña. Se identifica mediante una cadena de texto para la cual han sido asignadas las credenciales (tiquet). El formato típico para un _principal_ suele ser _primary/instance@REALM_
	* _primary_: La primera parte es, en el caso de un usuario es su nombre de usuario, en caso de un servicio el nombre del servicio.
	* instance: La segunda parte da información sobre la primera parte, en caso de ser un usuario suele ser el rol del usuario (user/admin). En caso de un host suele ser su FQDN (webserver.example.com)
	* _Realm_: Podemos entender un _Kerberos realm_ como el domino  en el cual un Kerberos AS tiene la autoridad de autenticar usuarios, hosts, o servicios. Suele estar formada por una única base de datos Kerberos y uno o más KDC. Por convenio, el _realm_ suele nombrarse en mayúsculas para diferenciarlo de un domino de internet.
* _cliente_: Entidad que obtiene un tiquet, normalmente un usuario o un host
* _ticket_: Credenciales electrónicas temporales que verifican la identidad del cliente para un servicio en particular
* _TGT_: Ticket-Granting Ticket: Un tiquet especial que permite al cliente obtener tickets adicionales dentro del mismo _realm_. Este TGT permite al usuario acceder a varios servicios sin necesidad de introducir la contraseña estableciendo comunicaciones seguras y capacidades de single sign-on(SSO)

## Anexo II. Misc comands
```bash
incus network set incusbr0 dns.domain asir2.grao
getent hosts 10.149.165.99 
resolvectl dns <network interface> <dns_address>
resolvectl domain <network interfacee> ~<dns_domain>

/usr/sbin/sshd -d -d -d -p 2223
ssh -vv ubuntu@ssh-server.asir2.grao -p 2223
```