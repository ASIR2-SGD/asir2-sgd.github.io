---
layout: default
title: PKI. OpenSSL Simple PKI
---
# Simple PKI(Public Key Infraestrucutra) with OpenSSL

 >[!NOTE]
 > OpenPGP is the most widely used email encryption standard. It is defined by the OpenPGP Working Group of the Internet Engineering Task Force (IETF) as a Proposed Standard in [RFC 9580](https://www.rfc-editor.org/rfc/rfc9580.htm)

![PKI Process](https://pki-tutorial.readthedocs.io/en/latest/_images/PKIProcess.png)

1.A requestor generates a CSR and submits it to the CA.
2.The CA issues a certificate based on the CSR and returns it to the requestor.
3.Should the certificate at some point be revoked, the CA adds it to its CRL.

# Simple PKI
[Tutorial](https://pki-tutorial.readthedocs.io/en/latest/simple/index.html)

![Simple PKI](https://pki-tutorial.readthedocs.io/en/latest/_images/SimplePKILayout.png)

```bash
pki
├── ca
│	 ├── root-ca
│	 │     └── root-ca.key
│	 ├── root-ca.crt
│	 ├── signing-ca
│	 │		 └── private
│	 │				├── signing-ca.key
│	 │				└── signing-ca-password.txt
│	 ├── signing-ca.crt
│	 └── signing-ca.csr
├── certs
│	 ├── issued
│	 │	 ├── lucas.crt
│	 │	 ├── david.crt
│	 │	 └── david.pem
│	 ├── requests
│	 │	 ├── lucas.csr
│	 │	 └── david.csr
├── crl
├── etc
└── sign_req.sh
```
# Comandos openssl
**Crear par de claves privada/pública**
```bash
openssl genrsa -des3 -out private_key.key 2048
openssl genrsa -out private_key.key 2048
openssl genrsa -out $(whoami)_key.key 2048

```
**Obtener clave pública a partir de par de claves.**
```bash
openssl pkey -pubout -in private.key -out pub_key.pub
```
**Crear CSR**
```bash
openssl req -new -key $(whoami)_key.key -out pki/requests/$(whoami)_request.csr
openssl req -new -key $CERTS_DIR/private/$(whoami)_key.key -config $CERTS_DIR/etc/my_config.conf -out $CERTS_DIR/csr/$(whoami)_request.csr
```
**Ver CSR**
```bash
openssl req -in shared/requests/$(whoami)_request.csr -noout -text
```

**Firmar CSR**
```bash
openssl ca -config etc/signing-ca.conf -in certs/requests/fred.csr -out certs/issued/fred.crt -extensions email_ext
```
**Ver certificado firmado**
```bash
openssl x509 -text -in yourdomain.crt -noout
```

**Verificar certificado en la cadena de confianza (Thrusted Chain)**
```bash
openssl verify -CApath /etc/ssl/certs cert_to_be_verified.pem
```

**Obtener clave pública del par de claves, certificado y CSR**
```bash
openssl pkey -pubout -in private.key -out pub_key.pub
openssl req  -pubout -in request.csr -out pub_key.pub
openssl x509 -pubout -in certificate.crt -out pub_key.pub
```

**Comprobar inconsistencias entre claves y certificados **
```bash
openssl pkey -pubout -in private.key | openssl sha256
openssl req -pubkey -in request.csr -noout | openssl sha256
openssl x509 -pubkey -in certificate.crt -noout | openssl sha256
```

**Convertir entre CRT y PEM**
```bash
openssl x509 -in mycert.crt -out mycert.pem -outform PEM
```


**Convertir a PKCS#12**
By default, OpenSSL generates keys and CSRs using the PEM format. However, there might be occasions when you need to convert your key or certificate into a different format to export it to another system.
```bash
openssl pkcs12 -export -name "yourdomain-digicert-(expiration date)" \
-out yourdomain.pfx -inkey yourdomain.key -in yourdomain.crt
```

**Firmar documentos**
```bash
openssl dgst -sha256 -sign private.key" -out sign.txt.sha256 sign.txt
openssl dgst -sha256 -verify  <(openssl x509 -in "$(whoami)s Sign Key.crt"  -pubkey -noout) -signature sign.txt.sha256 sign.txt
```
El comando anterior se utiliza para firmar documentos, este genera un hash del documento que es encriptado con la clave privada, creando de esta forma una firma digital. El inconveniente es que la firma y el documento están en ficheros separados.

**Firmar documentos PDF**
Utilizaremos la utilidad [open-pdf-sign](https://github.com/open-pdf-sign/open-pdf-sign) para firmar documentos _pdf_

```bash
$ mkdir -p ~/bin && cd ~/bin
$ wget https://github.com/open-pdf-sign/open-pdf-sign/releases/download/v0.3.0/open-pdf-sign.jar
$ echo 'PATH=$PATH:~/bin'
$java -jar open-pdf-sign.jar --add-page --page -1 --timestamp --input document.pdf --output document_signed.pdf --certificate certificate.crt --key private.key 
```



# Actividad
Crea un breve documento en formato _Markdown_ indicando brevemente los pasos y los comandos llevados a cabo. El documento debe ser coherente y con sentido. 
Genera y firma el documento
* Crea la siguiente estructura de ficheros y directorios

```bash
Documentos/SAD/certs <-certificados firmados por CA de clase
├── csr  			<- enlace via ssshfs a la carpeta pki/certs/requests de sshfs  
├── signed      	<- enlace via ssshfs a la carpeta pki/certs/issued de sshfs 
├── etc				<- configuración
└── private			<- clave privada
```

>[!TIP]
> Utiliza el comando `sshfs` para _montar_ una carpeta compartida con el servidor via ssh
---
```bash
sshfs -o allow_other,default_permissions ubuntu@ip:/home/ubuntu/pki/requests ~/certs/csr
sshfs -o allow_other,default_permissions ubuntu@ip:/home/ubuntu/pki/issued ~/certs/signed
```


* Crea un par de claves privadas/publica mediante OpenSSL, almacenala en la carpeta correspondiente a su uso
* [Descarga](https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/resources/files/openssl-server.conf) y modifica la plantilla de configuración para crear CSR 
```bash
wget https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/resources/files/openssl-server.conf
```

* Espera a que tu petición sea firmada y utilizando comandos openssl indica:
	* Nombre de la CA que ha firmado el certificado(emissor/issuer)
	* Validez del certificado
	* Hash del CA emissor

* Completa la memoria y firma el documento pdf con tu certificado.




# Glosario de términos
## Componentes
**Public Key Infrastructure (PKI)**
Arquitectura de seguridad donde la credibilidad se obtiene mediante la firma de una CA fiable.
**Certificate Authority (CA)**
Entidad que emite certificados y CRL
**Certificate**
Clave pública e ID vinculados por la firma de una CA
**Certificate Signing Request (CSR)**
Petición de solicitud de certificado. Contiene la clave pública y el ID a certificar.
**Certificate Revocation List (CRL)**
Lista de los certificados revocados (inválidos). Publicada por la CA a intervalos regulares.

## Jerarquia PKI
![CA Hierarchy](https://www.keytos.io/blog/img/root-ca-vs-issuing-ca.jpg)

**CA Root**
Una CA que no es certificada por ninguna otra, se basa únicamente en su propia reputación.
**Intermediate CA/subordinate CA**
Una CA Certificado por otra se denomina CA subordinada o CA Intermedia
**Singing CA/Issuing CA**
CA en la parte inferior de la jerarquia PKI. Emite los certificados para usuarios,servidores,etc.
## Formato de ficheros
**Privacy Enhanced Mail (PEM)**
En formato de texto. Codificado Base-64 con lineas de cabecera y pie. Formato preferido en OpenSSL y
la gran mayoría de software (e.g. Apache mod_ssl, stunnel).
Es un contenedor para almacenar claves y certificados (cadena de certificados)
**Distinguished Encoding Rules (DER)**
En binario. Formato preferido en entornos Windows. Tambíen el formato oficial par al descarga de certificados y CRLs.
**Signed Certificate (CRT)**
.crt or .cert son los ficheros firmados por una CA. Solo contiene un solo certificado

# Links
[Tutorial](https://pki-tutorial.readthedocs.io/en/latest/)

