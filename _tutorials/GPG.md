---
layout: default
title: GPG. Pretty Good Privacy
---
# Práctica GPG. Pretty Good Privacy
 
 >[!INFO] OpenPGP is the most widely used email encryption standard. It is defined by the OpenPGP Working Group of the Internet Engineering Task Force (IETF) as a Proposed Standard in [RFC 9580](https://www.rfc-editor.org/rfc/rfc9580.html)
  
## Contexto
El término criptografía proviene del griego *kyptós* 'oculto' y *grafé* 'escritura' y es definida como el arte de escribir con clave secreta o de un modo enigmático.

Gracias al uso de la criptografía se puede obtener una seria de ventajas de gran utilidad en el ámbito de la seguridad informáticfa como son:
* Confidencialidad
* Integridad
* Autenticidad
* No repudio
    

En esta práctica se trabajará sobre estos cuatro conceptos mediante la herramienta de comandos gpg (Pretty Good Privacy)

## Objetivos
* Entender la *confidencialidad, Integridad, Autenticidad* y no repudio mediante el uso de la herramienta *gpg*.
* Entender y poner en práctica la criptografía simetrica
* Entender y poner el práctica la criptografía asimétrcia
* Saber cifrar y descifrar mensajes mediante criptografía simétrica.
* Saber cifrar y descifrar mensajes mediante criptografía asimétrica.
* Saber firmar otras llaves generando así una relación de confianza entre usuarios de la comunidad.
* Ser capaces de firmar un documento y verificar que este ha sido firmado por quien dice ser.
* Ser capaces de importar/exportar claves a un servidor público
* Saber enviar correos cifrados y descifrar correos privados

## Comandos GPG
>[!WARNING]
> Para el correcto funcionamiento de `gpg` en un contenedor linux (LXC) es necesario llevar a cabo la siguiente configuración
> ```bash
> printf 'use-agent\npinentry-mode loopback\n' > ~/.gnupg/gpg.conf
> printf 'allow-loopback-pinentry\n' > ~/.gnupg/gpg-agent.conf
> ```

 1. **Cifrar y descifrar un mensaje mediante criptografía simétrica**
 ```bash
 gpg --armor --symetric --output <encrypted_file.asc>
 gpg --armor --decrypt <encripted_file.asc> --output <plain_file.txt>
 ```

>[!IMPORTANT]
> * Descubre como evitar que `gpg` solicite la contraseña para encriptar/desencriptar
> * Investiga sobre la opcion `--armor`, uso y finalidad
> * Investiga sobre los algoritmos de encriptación simétricos compatibles con `gpg` y como especificar el uso de uno en particular en el comando.
> * Desencripta el siguiente texto cifrado con la clave simétrica _asir2_
> 
> ```bash
> -----BEGIN PGP MESSAGE-----
>
>jA0ECQMKBeD5Nh596bT/0ooBe1dQceySdZjYYgFFCzQlhkzIS9D2I7rdiR8E1r7L
>KtM69GVltp1KfYP33RlXZPND7BDSLrQeFcO4zlD25IO2jePcZSzEU+O4lz10WGIl
>6dnQE8SoTgVeLXNgHE+W0PB+C+8ab47bc0zoBCIDfwG4nWlTFrKdok4jz6Jcwh3F
>51YTVHEIc2Qh7KU=
>=kC55
>-----END PGP MESSAGE-----
>```

 1. **Crear par de claves**
 ```bash
 $ gpg --full-gen-keys
 $ gpg --batch --passphrase '' --quick-gen-key USER_ID default default 
 ```
 2. **Listar/borrar claves pública/privada**
 ```bash
 $ gpg --list-key
 $ gpg --list-secret-keys
 $ gpg --list-public-keys
 $ gpg --list-public-keys --keyid-format=short
 $ gpg --delete-keys <key_id>
 
 ```
 3. **Importar/exportar claves publicas y privadas**
 ```bash
 $ gpg --output <public_key.asc> --armor --export <keyid>
 $ gpg --output <private_key.asc> --armor --export-secret-keys <keyid>
 $ gpg --import <key_file.asc> 
 ```
 4. **Importar y exportar de un servidor de claves**
 ```bash
 $ gpg --keyserver <URI> --search-keys <string of info>
 $ gpg --keyserver <URI> --receive-keys <keyid>
 $ gpg --keyserver <URI> --send-keys <keyid>
 $ gpg --keyserver <URI> --refresh-keys
 ```
 5. **Encriptar un documento con clave pública de destinatario**
 ```bash
 $ gpg --output <file_encrypted> --armor --encrypt --recipient 'some user ID value' <file_to_encrypt> 
 ```
 6. **Desencriptar un documento cifrado con nuetra clave publica haciendo uso de clave privada**
  ```bash
  $ gpg --decrypt <encrypted-file>
 ```
 7. **Firmar un mensaje y verificar la autoria de un mensaje**
 ```bash
 $ gpg --sign <file_to_sign>
 $ gpg --output <file_signed> --armor --default-key <keyid> --clearsign <file_to_sign>
 $ gpg --clearsing <file_to_sign> ##documento legible
 $ gpg --armor --detach-sign <signed_file>
 $ gpg --verify <signed_file>
 ```
## Actividades
>[!WARNING]
> En cada una de las actividades, realizadas, deberás presentar un documento con una breve descripción de los pasos realizados en la tarea y las instrucciones. Utiliza un formato adecuado para el `codigo`

>[!TIP]
> Puedes aprovechar y aprender a utilizar *markdown* un lenguaje de marcas muy sencillo con el que podrás hacer documentos como este mismo.

### Integridad y autoría de un documento/mensaje**
 Simula en esta actividad que alguien quiere cambiar un documento firmado, vamos a suponer que es un testamento.  Actua como si fueras un notario con su par de claves ([pública](https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/resources/files/notario-public-key.pub)/[privada](https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/resources/files/notario-private-key.key)) y has firmado la validez del testamento.
 
 1.  Importa las claves del notarios (_passphrase: sad_)
 2. Usa las claves para firmar documento [testamento.txt](https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/resources/files/testamento.txt) sin cifrar --clearsign
3. Modifica el documento firmado y verifica 
4. Explica los comandos utilizados.

### Firma un documento encriptado y verifica**
1. Descarga el par de claves [pública](https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/resources/files/asir2_student_pub.asc)/[privada](https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/resources/files/asir2_student_key.asc) de _asir2_student_
2. Impórtalas a tu anillo de claves 
	1. Necesitarás obtener el passphrase que obtendras descifrando el siguiente [documento](https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/resources/files/asir2_keys_passphrase.asc) de forma simétrica con la clave _'n0l0dig4$'_
3. Descrifra el siguiente [mensaje](https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/resources/files/task_encrypted_and_signed.asc) y haz lo que dice el mensaje
4. ¿Quién ha firmado el mensaje?


### Mailevelope
 * Importar clave privada
 * Subir clave pública al keyserver de mailevelope
 * Importar claves publicas
 * Enviar un mensaje cifrado y descifrar mensaje.  

### Firma claves de compañeros para crear un circulo de confianza
[Tutorial](https://gist.github.com/F21/b0e8c62c49dfab267ff1d0c6af39ab84)
En esta actividad debes desgargar del servidor de llaves usado en clase todas las claves de tus compañeros ) y firmarlas con tu clave privada.
1. Actualiza el documento compartido con tu identificador de clave y descarga las claves de los demás compañeros
2. Firma las claves públicas de tus compañeros con tu clave privada haciendo estas de confianza y ampliando el círculo de confianza.
3. Súbelas a la carpeta compartida correspondiente para que tus compañeros puedan descargarse sus claves firmadas por ti. Sigue el siguiente estandard de nomenclatura. `<apellido_nombre>_signed_by_<tu nombre>.asc'
4. Descargate tus claves públicas firmadas por tus compañeros y súbelas al servidor


 