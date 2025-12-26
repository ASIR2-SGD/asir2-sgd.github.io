---
layout: default
title: Apache TLS
---
# Apache TLS / PKI(Public Key Infrastructure)

## Contexto
Autoridades certificadoras son las responsables de emitir certificados digitales para verificar identidades en internet (servidores, personas, conexiones).
El uso de estos certificados permiten conexiones confiables, además de autenticidad y no repudio.
TLS (Transport Layer Security) es un protocolo de seguridad basado en criptografía asimétrica que establece un canal seguro entre dos hosts
    
En esta práctica configuraremos nuestro servidor web (Apache) para establecer conexiones seguras mediante el protocolo HTTPS.
El certificado digital que usaremos deberá estar firmado por una Autoridad Certificadora que crearemos y configuraremos.

## Links
* [Autoridades certificadorase](https://devopscube.com/create-self-signed-certificates-openssl/)
  
* [Crear una autoridad certificadora - Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-and-configure-a-certificate-authority-on-ubuntu-22-04)
* [Configurar TLS en Apache](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-20-04)
* [Configurar NFS](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-22-04)


## Objetivos
* Entender el papel de una CA y el proceso de creación de certificados digitales
* Crear y configurar una CA mediante la utilidad *easy-rsa*
* Crear par de claves para crear una petición de certificado
* Saber firmar peticiones de certificados digitles(CSR)
* Compartir ficheros(certificados) en la red mediante NFS
* Configurar el protocolo https del servidor web apache para transmisiones seguras.
* Verificar y documentar de forma clara, concisa y completa los pasos llevados a cabo para la finalización de la práctica.

## Desarrollo

Para simular un entorno más real, configuraremos nuestro contenedor de Apache con una _ip_ del aula, para crearemos un _bridge_ entre el interfaz virtual _eth0_ y nuestro interfaz real. Esto en incus es muy sencillo con el comando
```bash
$ incus network list
$ incus launch images:ubuntu/noble apache --network <interfaz_host> 
```

>[!NOTE]
> Por defecto, la dirección ip la cogerá mediante _dhcp_ de la _gw_ del aula como si se tratase de un _host_ más.
> Si necesitamos una ip _static_ deberemos editar el fichero _/etc/netplan/10-lxc.yaml_

Crea la siguente estructura de directorios para tener nuestros certificados organizados
```bash
.
└── certs
    ├── csr
    ├── etc
    ├── private
    └── signed

```
La _CA_ denominada _pki_ comparte dos carpetas para que podamos enviarle nuestras peticiones de firma _requests_ y obtener los cetificados firmados _issued_. Ámbas carpetas se encuentran en la carpeta _/home/ubuntu/pki/certs_
Accede a ellas de forma fácil mediante _sshfs_
```bash
$ sshfs -o allow_other,default_permissions ubuntu@ip:/home/ubuntu/pki/requests /home/ubuntu/certs/csr/
$ sshfs -o allow_other,default_permissions ubuntu@ip:/home/ubuntu/pki/issued /home/ubuntu/certs/signed/
```

>[!TIP]
>Mejora la práctica y tu puntuación en ella haciendo los puntos de monaje persistentes, es decir que se creen cuando arranca el sistema.


### Conexiones seguras.

#### Creación de certificados
Para habilitar las conexiones seguras _TLS_ en tu servidor web, deberás obtener un certificado firmado por la CA de clase.
Para ello debes crear una petición

* Crea la carpeta _~/certs/etc_ donde guardarás la configuración de tu petición de certificado. modifica la [plantilla](https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/resources/files/openssl-server.conf) a tus necesidades

> [!TIP]
> Añade el la seccion _alt_names_ un DNS a tu elección y la IP de tu server

* Utiliza el siguiente comando para crear la petición
```bash
username=<student-gva-username>
openssl req -new \
   	-config certs/etc/my-server.conf \
   	-out certs/csr/apache.$username.local.csr \
   	-keyout certs/private/apache.$username.local.key
```

**Responde:**
* _¿Para que sirve la opción req?._
* _¿Para que sirve la opción keyout?._
* _¿Cuál es la finalidad del comando anterior?_


Una vez creada la petición, notifica a la CA para que lleve a cabo la firma del certificado.
Utiliza el comando `openssl x509 -in <certificado> -noout -text` para inspeccionar el certificado y responde:

* _¿Cuál es emisor del certificado?_
* _¿Cuál es el identificador (SubjectKeyIdentifier) del certificado?_
* _¿Cuál es el identificador del emisor del certificado?_

Abre el certificado raiz _root-ca.crt_ y comprueba que el identificador del certificado raiz coincide con el identificador del emisor de tu certificado. 
Explora el comando `openssl x509 -in <certificado> -noout -ext subjectKeyIdentifier` para obtener directamente el identificador.

* _¿Qué comando de openssl obtiene directamente el identificador del emisor?_
* _¿Qué comandos has utilizado para comparar si _id_issuer == cert_issuer_id_?



#### Configuración Apache2

Habilita las conexione SSL en tu servidor apache usando el certificado firmado

* Crea la carpeta _/etc/apache2/ssl_ y _/etc/apache2/ssl/private_ para el certificado y su correspondiente clave privada
* Tomando como ejemplo el fichero _/etc/apache2/sites-available/default-ssl.conf_ crea el tuyo propio denominado _apache.$username.local.conf_ con la configuración necesaria para habilidar las conexiones SSL mediante el protocolo TLS. Para ello deberás referenciar tanto tu certificado como la clave privada.

* Crea una página web de prueba y comprueba desde el navegador, que efectivamente las conexiones son seguras 

* Añade el certificado raiz al navegador
    * Firefox [tutorial](https://stackoverflow.com/questions/1435000/programmatically-install-certificate-into-mozilla)
    * Chrome [tutorial](https://stackoverflow.com/questions/19692787/how-to-install-certificate-in-browser-settings-using-command-prompt)


*TODO*
Memoria firmada