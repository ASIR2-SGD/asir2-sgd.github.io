# Práctica 3b. Autoridades certificadoras (CA) y Public Key Infrastructure (PKI) y Apache TLS

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

##Pasos previos
* Configurar VM con ip pública de aula
* Configurar NFS Server en cada máquina
* Configurar NFS Client a CA_TEAM y CA_CENTRAL

##Pasos CA
* Crear y configurar Certification Authority (CA Server)

>[!NOTE]
> Obtenemos (ca.crt y ca.key) Explicar que es cada fichero

* Compartir certificado digital de la autoridad certificadora (ca.crt) 


##Pasos solicitante
* Instalar  certificado digital de la autoridad certificadora en el sistema
* Crear solicitud de certificado (CSR)
* Enviar solicitud a CA
* Firmada la solictud configurar apache para uso de HTTPS 

>[!WARNING]
> Verificar y demostrar que sompos capaces de establecer conexiones seguras HTTPS con nuestro servidor web y que el certificado de nuestro servidor web está firmado por la CA de clase.