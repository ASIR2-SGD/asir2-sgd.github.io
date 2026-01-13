---
layout: default
title: Kerberos
---
# Kerberos

# Arquitectura
## Componentes
![Componentes Kerberos](https://miro.medium.com/v2/resize:fit:720/format:webp/1*NbvqDTvTl8RS49dtFHjG7A.png)
## Protocolo
![Kerberos protocol 1](https://danlebrero.com/images/kerberos-for-dummies-2.jpg)
___
![Kerberos protocol 2]({% link /resources/img/Kerberos01.png %})

## Glosario de términos
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

## Actividad I. ssh-server & kerberos

| Realm | Primary KDC | User principal | Admin principal |
| ----------|----------| ----------| ------------|
| ASIR2.GRAO | kdc01.asir2.grao | ubuntu | ubuntu/admin |

## Escenario en Incus
Para llevar a cabo la práctica, deberemos construir el siguiente escenario con contenedores
* Servidor de nombres 
* KDC
* krb-cli
* ssh-server

Las máquinas _KDC_, _krb-cli_ y _ssh-server_ están en la red _krbbr0_. La resolución de nombres, esencial para que el protocolo de autenticación Keberos, funcione correctamente la hace _dnssrv_

**Network**
* _Type_ : bridged managed
* _Name_ : krbbr0
* _Net ip/mask_ : 10.144.144.0/24
* _nameserver_ : _ip-dnssrv_
* _search domain_ : asir2.grao

```bash
$ incus network create krbbr0 \
      ipv4.address=10.144.144.1/24 \
      ipv6.address=none ipv4.nat=true \ 
      ipv4.dhcp.ranges = 10.144.144.100-10.144.144.100 \
      dns.nameservers = <ip-dns-server> \
      dns.domain = asir2.grao
```

**DNS** 

```bash
$ incus launch images:ubuntu/noble dnssrv
$ incus exec dnssrv -- bash -c 'apt-get update && apt-get -y install  aptitude wget bind9 dnsutils bash-completion nano xsel vim'
```

Configurar
* [Tutorial](https://documentation.ubuntu.com/server/how-to/networking/install-dns/#install-dns)

## Kerberos [tutorial](https://documentation.ubuntu.com/server/how-to/kerberos/install-a-kerberos-server/)
### KDC 

```bash
$ incus launch images:ubuntu/noble kdc --network krbbr0
$ incus exec kdc -- bash -c 'apt-get update && apt-get -y install  aptitude wget krb5-kdc krb5-admin-server bash-completion nano xsel vim' 
```

> [!WARNING]
> Kerberos confia en la resolución de nombres, por lo que es importante tener un servidor _DNS_ correctamente configurado y con los registros necesarios para el correcto funcionamiento del _KDC_.

> [!TIP]
> _kinit_ inspecciona el fichero _/etc/krb5.conf_ para encontra con que _KDC_ contactar. Esto tiene el inconveniente que en un despliege con cientos de clientes, si modificamos la ip del _KDC_ deberemos reflefar ese cambio en el fichero. El _KDC_ puede ser encontrado via busquedas DNS, para ello debes añadir registros _TXT_ y _SRV_ a tu servidor de nombres.
> Mejora tu calificación llevando la mejora mencionada.


### krb-cli
```bash
$ incus launch images:ubuntu/noble krb-cli --network krbbr0
$ incus exec krb-cli -- bash -c 'apt-get update && apt-get -y install  aptitude wget krb5-user krb5-config bash-completion nano xsel vim'
root@kdc-client:~# kinit ubuntu
root@kdc-client:~# klist
```

### Servidor SSH Kerberizado
```bash
$ incus launch images:ubuntu/noble ssh-server --network krbbr0
$ incus exec ssh-server -- bash -c 'apt-get update && apt-get -y install krb5-user krb5-config openssh-server aptitude wget bash-completion nano xsel vim'
root@ssh-server-k:~# kinit ubuntu/admin
root@ssh-server-k:~# klist
root@ssh-server-k:~# kadmin
kadmin: add_principal -randkey host/ssh-server.asir2.grao@ASIR2.GRAO
kadmin: ktadd host/ssh-server.asir2.grao
klist -ke /etc/krb5.keytab 
```

## Actividad II. Apache web server & kerberos
> [!IMPORTANT]
> Puedes mejora tus conocimientos sobre kerberos así como tu calificación en la asignatura llevando a cabo la _kerberización_ del servidor web apache. Busca información reslacionada en internet con las siguienes palabra clave _apache kerberized_. Crea un escenario similar al de la actividad I.





## Links
* [Kerberos explained in pictures]https://danlebrero.com/2017/03/26/Kerberos-explained-in-pictures/
* [Kerberos Authentication Explained](https://www.youtube.com/watch?v=5N242XcKAsM&t=18s)
* [Introduction to Kerberos](https://documentation.ubuntu.com/server/explanation/intro-to/kerberos/)
* [Configuring OpenSSH to use Kerberos Authenticatio](https://www.kevindiaz.dev/blog/configuring-openssh-to-use-kerberos-authentication.html)


## Anexo II. Analogía feria atracciones
![Kerberos protocol 2]({% link /resources/img/Kerberos02.png %})

> Una forma de  pensar en  el uso de Kerberos  es  imaginar que  vas a  un  parque de atracciones.
> Cuando  llegas al  parque, te diriges  a  la puerta principal. Luego, te diriges a la taquilla principal (el servidor de autenticación en el centro de distribución de claves) y compras un pase de un día para el parque (un ticket que te da acceso).

>  Recibes una pulsera *morada* (porque el morado es el color del miércoles) que indica que has pagado la entrada para ese día y que tienes acceso completo al parque. La pulsera de color es válida para todo el día.

> Mientras estás en el parque, debes adquirir entradas adicionales para las atracciones.  Te acercas a la taquilla de la atracción (servidor de tickets) y la empleada se da cuenta de que llevas una pulsera *morada*. Le dices que quieres montarte en la montaña rusa. Ella te expide un ticket (ticket de sesión) para la montaña rusa.

>  Cuando llegas a la montaña rusa, el encargado de la montaña rusa ve tu pulsera morada y acepta el ticket que te ha dado la taquillera. El encargado de la montaña rusa no necesita consultar con la taquillera porque ese es el único lugar donde podrías haber conseguido ese ticket. 

> Al  final del  día,  cuando  cierra el parque, la pulsera morada del miércoles ya no te identifica.  El color de la pulsera del jueves es naranja. También te diste cuenta de que tú hiciste todo el trabajo. Ninguno de los vendedores de entradas ni los operadores de las atracciones se comunicaron entre sí.  Dependía de ti.


## Anexo I. Misc comands
```bash
incus network set incusbr0 dns.domain asir2.grao
getent hosts 10.149.165.99 
resolvectl dns <network_bridge> <dns_address>
resolvectl domain <network_bridge> ~<dns_domain>

/usr/sbin/sshd -d -d -d -p 2223
ssh -vv ubuntu@ssh-server.asir2.grao -p 2223
```