---
layout: default
title: Apache TLS
---
# Apache TLS / PKI(Public Key Infrastructure)

## Contexto
Autoridades certificadoras son las responsables de emitir certificados digitales para verificar identidades en internet (servidores, personas, conexiones).
El uso de estos certificados permiten conexiones confiables, además de autenticidad y no repudio.
TLS (Transport Layer Security) es un protocolo de seguridad basado en criptografía asimétrica que establece un canal seguro entre dos hosts
    




## Objetivos
* Entender el protocolo TLS y HTTPS
* Entender el papel de una CA y el proceso de creación de certificados digitales
* Crear y configurar una CA mediante la utilidad *easy-rsa*
* Crear par de claves para crear una petición de certificado
* Saber firmar peticiones de certificados digitles(CSR)
* Compartir ficheros(certificados) en la red mediante NFS
* Configurar el protocolo https del servidor web apache para transmisiones seguras.
* Verificar y documentar de forma clara, concisa y completa los pasos llevados a cabo para la finalización de la práctica.

## TLS (Transport Layer Security)
_TLS_ es un protocolo de seguridad ampliamente usado diseñado para facilitar privacidad y seguridad en las comunicaciones a través de internet. El uso principal de TLS es encriptar comunicaciones entre el cliente y el servidor.
_HTTPS_ es una implementación de _TLS_ que es usado por los servidores web y otras servicios web. Cualquier sitio que utilice _HTTPS_ esta por lo tanto haciendo uso de _TLS_

### Protocolos (Handshake)
![TLS Protocol](https://supertokens.com/static/9cff8404dcf549f68f947fc906ae76a9/29007/tls1.3.png)

Durante el _handshake_ TLS el cliente y el servidor:
* Especifican que versión de TLS (1.0, 1.2, 1.3, etc.) van usar y que suite de cifrado usar.
> Hi, I’m your friend, and I want to start a secure conversation. Here are the languages I can speak (types of encryption I can use), and here are some secrets (keys) I’m willing to use to help us understand each other.” 

* El servidor se autentica como el auténtico mediante el envio de un certificado
> To prove they are the rightful owner of the web site(and not an imposter), your friend shows you a badge (certificate) that a trusted authority has signed.

* Generate session keys for encrypting messages between them after the handshake is complete 
> After checking the badge, you both agree on a special, private language (a shared secret) for your conversation. This final agreement on a shared secret solidifies your communication channel’s security.


## Actividad

### Guión esquemático

> 1. Crear petición de certificado y enviar a la CA.
> 2. Instalar el certificado raíz en nuestro sistema operativo.
> 3. Crear, modificar y activar tu web site basándote en el fichero existente _/etc/apache/sites-available/default-ssl.conf_
> 4. Configurar, probar y verificar mediante un navegador web

En esta práctica configuraremos nuestro servidor web (Apache) para establecer conexiones seguras mediante el protocolo HTTPS.
El certificado digital que usaremos deberá estar firmado por una Autoridad Certificadora que crearemos y configuraremos.

### Container creation and setup
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
La _CA_ denominada _pki_ comparte dos carpetas para que podamos enviarle nuestras peticiones de firma _requests_a y obtener los cetificados firmados _issued_. Ámbas carpetas se encuentran en la carpeta _/home/ubuntu/pki/certs_
Accede a ellas de forma fácil mediante _sshfs_
```bash
$ sshfs -o allow_other,default_permissions ubuntu@ip:/home/ubuntu/pki/requests /home/ubuntu/certs/csr/
$ sshfs -o allow_other,default_permissions ubuntu@ip:/home/ubuntu/pki/issued /home/ubuntu/certs/signed/
```

>[!TIP]
>Mejora la práctica y tu puntuación en ella haciendo los puntos de monaje persistentes, es decir que se creen cuando arranca el sistema.

### Creación de certificados
Para habilitar las conexiones seguras _TLS_ en tu servidor web, deberás obtener un certificado firmado por la CA de clase.
Para ello debes crear una petición

* Crea la carpeta _~/certs/etc_ donde guardarás la configuración de tu petición de certificado. modifica la [plantilla](https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/resources/files/openssl-server.conf) a tus necesidades

> [!TIP]
> Añade el la seccion _alt_names_ un DNS a tu elección y la IP de tu server


* Utiliza el siguiente comando para crear la petición
```bash
username=<student-gva-username>
openssl req -new \
   	-config certs/etc/apache.$username.request.asir2.grao.conf \
   	-out certs/csr/apache.$username.asir2.grao.csr \
   	-keyout certs/private/apache.$username.asir2.grao.key
```

**Responde:**

1. _Explica la función de cada uno de los ficheros enumerados y utilizados en las prácticas_
    * apache.$username.asir2.grao.key
    * apache.$username.asir2.request.grao.conf
    * apache.$username.asir2.grao.csr
    * apache.$username.asir2.grao.crt
    * apache.$username.asir2.grao.conf
    * root-ca.crt
2. _¿Para que sirve la opción req?._
3. _¿Para que sirve la opción keyout?._
4. _¿Cuál es la finalidad del comando anterior?_

### Instalación del certificado raiz

Para llevar a cabo la el reconocimiento en nuestro S.O del certificado raiz _ca-root.crt_, deberemos copiar este en la carpeta _/usr/local/share_ca-certificates/_ y ejecutar el comando _update-ca-certificates_ 


Una vez creada la petición, notifica a la CA para que lleve a cabo la firma del certificado.
Utiliza el comando `openssl x509 -in <certificado> -noout -text` para inspeccionar el certificado y responde:

5. _Explica qué es un certificado raiz y porqué es neceario instalarlo en nuestro S.O_
5. _¿Qué hace el comando _update-ca-certificates_?. ¿en que carpeta están los certificados del sistema?. Indica el comando para comprobar que el certificado raiz de clase esta instalado y reconocible por el S.O
5. _¿Cuál es emisor del certificado?_
6. _¿Cuál es el identificador (SubjectKeyIdentifier) del certificado?_
7. _¿Cuál es el identificador del emisor del certificado?_


Abre el certificado raiz _root-ca.crt_ y comprueba que el identificador del certificado raiz coincide con el identificador del emisor de tu certificado. 
Explora el comando `openssl x509 -in <certificado> -noout -ext subjectKeyIdentifier` para obtener directamente el identificador.

8. _¿Qué comando de openssl obtiene directamente el identificador del emisor?_
9. _¿Qué comandos has utilizado para comparar si _id_issuer == cert_issuer_id_?

> [!TIP]
> Muchos ficheros de configuración incluyen comentarios anteponiendo el caracter '#'. En algunas  ocasiones será necesario eliminar esos comentarios y líneas en blanco. Puedes usar el comando sed con las siguientes opciones.
___
```bash
sed -e '/^\s*#.*$/d' -e '/^\s*$/d' file
```
10. _Explica la finalidad usando lenguaje natural (nada de tecnicismos) la finalidad de las dos expresiones regulares usadas en el comando anterior_




### Configuración Apache2

Habilita las conexione SSL en tu servidor apache usando el certificado firmado

* Crea la carpeta _/etc/apache2/ssl_ y _/etc/apache2/ssl/private_ para el certificado y su correspondiente clave privada
* Tomando como ejemplo el fichero _/etc/apache2/sites-available/default-ssl.conf_ crea el tuyo propio denominado _apache.$username.asir2.grao.conf_ con la configuración necesaria para habilidar las conexiones SSL mediante el protocolo TLS. Para ello deberás referenciar tanto tu certificado como la clave privada.
> [!WARNING]
> Es probable que sea necesario activar el modulo _ssl_ con el comando _a2enmod <nombre_modulo>_ para activar las conexiones seguras. 

* Crea una página web de prueba y comprueba desde el navegador, que efectivamente las conexiones son seguras  

* Añade el certificado raiz al navegador
    * Firefox [tutorial](https://stackoverflow.com/questions/1435000/programmatically-install-certificate-into-mozilla)
    * Chrome [tutorial](https://stackoverflow.com/questions/19692787/how-to-install-certificate-in-browser-settings-using-command-prompt)



## Entrega
* Enviar en un documento **firmado** en formato _markdown_ denominado *username_apache_tls.md* Con las respuestas a las preguntas planteadas en la actividad. Indica cuando sea necesario el comando utilizado. 
Crea un Anexo denominado _Anexo I. Ficheros de configuración_ y añade el contenido en texto (reducelo si es muy grande) excluyendo comentarios y líneas en blanco (utiliza el tip de la pregunta 10) de los siguientes ficheros.
    * apache.$username.asir2.grao.key
    * apache.$username.asir2.request.grao.conf
    * apache.$username.asir2.grao.csr
    * apache.$username.asir2.grao.crt
    * apache.$username.asir2.grao.conf

Utiliza el formato _markdown_ adecuado para tener un documento estructurado y legible.
* Comprueba el correcto funcionamiento de la actividad mediante la ejecución exitosa de los tests

### Propuestas de mejora
Las siguientes propuestas de mejora de la práctica se plantean al alumno como reto para que mejore sus destrezas y conocimientos de las herramientas de administrdor de sistemas y mejore su nota en la asignatura.

* **Mejora I-** Automatiza la creación y configuración del escenario propuesto para el la práctica que has llevado a cabo mediante el uso de un fichero _Taskfile.yml_ 


## Links
* [Autoridades certificadorase](https://devopscube.com/create-self-signed-certificates-openssl/)
  
* [Crear una autoridad certificadora - Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-and-configure-a-certificate-authority-on-ubuntu-22-04)
* [Configurar TLS en Apache](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-20-04)
* [Configurar NFS](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-22-04)