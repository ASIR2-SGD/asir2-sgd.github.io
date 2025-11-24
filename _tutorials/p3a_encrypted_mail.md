# Práctica 3a. GPG Pretty Good Privacy

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

## Desarrollo
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




 2. **Crear par de claves**
 ```bash
 gpg --full-gen-keys
 gpg --batch --passphrase '' --quick-gen-key USER_ID default default 
 ```
 3. **Listar claves pública/privada**
 ```bash
 ```
 4. **Importar/exportar claves publicas y privadas**
 ```bash
 ```
 5. **Importar y exportar de un servidor de claves**
 ```bash
 ```
 6. **Encriptar un documento con clave pública de destinatario**
 ```bash
 ```
 7. **Desencriptar un documento cifrado con nuetra clave publica haciendo uso de clave privada**
 ```bash
 ```
 8. **Firmar un mensaje y verificar la autoria de un mensaje**
 ```bash
 ```
 9. **Itegridad y autoria de un documento/mensaje**
 ```bash
 ```

     * Simula que alguien quiere manipular tu testamento. 
      * Firma el documento testamento.txt sin cifrar --clear-sign
      * Modifica el documento firmado y verifica 
 
 10.  **Mailevelope**
      * Importar clave privada
      *  Subir clave pública al keyserver de mailevelope
      *  Importar claves publicas
      *  Enviar un mensaje cifrado y descifrar mensaje.
  
  11. **Firma un documento encriptado y verifica**
      * Firma el docuento testamento.txt pero está vez lo vas a encriptar para que únicamente lo pueda leer el compañero notario (importar clave secreta) 
   12.  **Firma claves de compañeros para crear un circulo de confianza** 
     * [Tutorial](https://gist.github.com/F21/b0e8c62c49dfab267ff1d0c6af39ab84)

 