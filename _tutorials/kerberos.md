---
layout: default
title: Kerberos
---
# Kerberos

# Arquitectura
![Componentes Kerberos](https://miro.medium.com/v2/resize:fit:720/format:webp/1*NbvqDTvTl8RS49dtFHjG7A.png)
![Diagrama Kerberos](https://danlebrero.com/images/kerberos-for-dummies-2.jpg)

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

## Actividad. ssh-server & kerberos

| Realm | Primary KDC | User principal | Admin principal |
| ----------|----------| ----------| ------------|
| ASIR2.GRAO | kdc01.asir2.grao | ubuntu | ubuntu/admin |

### KDC 
* __Instalación__ [tutorial](https://documentation.ubuntu.com/server/how-to/kerberos/install-a-kerberos-server/)
```bash
$ incus launch images:ubuntu/noble kdc
$ incus exec kdc -- bash -c 'apt-get update && apt-get -y install  aptitude wget krb5-kdc krb5-admin-server bash-completion nano xsel vim' 
```

> [!WARNING]
> Kerberos confia en la resolución de nombres, por lo que es importante tener un servidor _DNS_ correctamente configurado y con los registros necesarios para el correcto funcionamiento del _KDC_.
> En nuestro caso, por simplicidad se modificara el fichero _/etc/hosts_ con los nombres e ip's correspondientes.

> [!TIP]
> _kinit_ inspecciona el fichero _/etc/krb5.conf_ para encontra con que _KDC_ contactar. Esto tiene el inconveniente que en un despliege con cientos de clientes, si modificamos la ip del _KDC_ deberemos reflefar ese cambio en el fichero. El _KDC_ puede ser encontrado via busquedas DNS, para ello debes añadir registros _TXT_ y _SRV_ a tu servidor de nombres.
> Mejora tu calificación llevando la mejora mencionada.


* __Configuración__ 

### Cliente
````bash
$ incus launch images:ubuntu/noble kdc
$ incus exec kdc -- bash -c 'apt-get update && apt-get -y install  aptitude wget krb5-user krb5-config bash-completion nano xsel vim'
root@kdc-client:~# kinit ubuntu
root@kdc-client:~# klist
```


* __Servidor SSH Kerberizado__
```bash
$ incus launch images:ubuntu/noble ssh-server-k
$ incus exec ssh-server-k -- bash -c 'apt-get update && apt-get -y install krb5-user krb5-config openssh-server aptitude wget bash-completion nano xsel vim'
root@ssh-server-k:~# kinit ubuntu/admin
root@ssh-server-k:~# klist
root@ssh-server-k:~# kadmin
kadmin: add_principal -randkey host/ssh-server.asir2.grao@ASIR2.GRAO
kadmin: ktadd host/ssh-server.asir2.grao

```


## Links
* [Kerberos explained in pictures]https://danlebrero.com/2017/03/26/Kerberos-explained-in-pictures/
* [Kerberos Authentication Explained](https://www.youtube.com/watch?v=5N242XcKAsM&t=18s)
* [Introduction to Kerberos](https://documentation.ubuntu.com/server/explanation/intro-to/kerberos/)


```bash
$ incus create eve-ng --empty --vm -c limits.cpu=2 -c limits.memory=4GiB -d root,size=20GiB
$ incus config device add eve-ng install disk source=<eve-ng.iso> boot.priority=10
$ incus start eve-ng --console=vga
$ incus config device remove eve-ngt install
$ incus console mint --type=vga
$ incus launch --vm mint22-image mint22 -c limits.memory=4GiB -c limits.cpu=4 -c security.secureboot=false --console=vga
```