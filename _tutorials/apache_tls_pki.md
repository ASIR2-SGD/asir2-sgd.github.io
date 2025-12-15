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

La _CA_ denominada _pki_ comparte dos carpetas para que podamos enviarle nuestras peticiones de firma _requests_ y obtener los cetificados firmados _issued_. Ámbas carpetas se encuentran en la carpeta _/home/ubuntu/pki/certs_
Accede a ellas de forma fácil mediante _sshfs_
```bash
$ sshfs -o allow_other,default_permissions ubuntu@ip:/home/ubuntu/pki/requests /home/ubuntu/certs/csr/
$ sshfs -o allow_other,default_permissions ubuntu@ip:/home/ubuntu/pki/issued /home/ubuntu/certs/signed/
```

>[!TIP]
>Mejora la práctica y tu puntuación en ella haciendo los puntos de monaje persistentes, es decir que se creen cuando arranca el sistema.

Crea un CSR para tu servidor, ver práctica [PKI / OpenSSL]({% link _tutorials/openssl-pki.md %})

*TODO*

* Configura Apache para crear una conexión segura TLS
	* Instalar  certificado digital de la autoridad certificadora en el sistema
	* Crear solicitud de certificado (CSR)
	* Enviar solicitud a CA
	* Firmada la solictud configurar apache para uso de HTTPS 

>[!WARNING]
> ...