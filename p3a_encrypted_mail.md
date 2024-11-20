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

 1. **Cifrar y descifrar un mensaje mediante criptografía simétrica**
 1. **Crear par de claves**
 1. **Listar claves pública/privada**
 1. **Importar/exportar claves publicas y privadas**
 1. **Importar y exportar de un servidor de claves**
 1. **Encriptar un documento con clave pública de destinatario**
 1. **Desencriptar un documento cifrado con nuetra clave publica haciendo uso de clave privada**
 1. **Firmar un mensaje y verificar la autoria de un mensaje**
 2. **Itegridad y autoria de un documento/mensaje**
     * Simula que alguien quiere manipular tu testamento. 
      * Firma el documento testamento.txt sin cifrar --clear-sign
      * Modifica el documento firmado y verifica 
 
 4.  **Mailevelope**
      * Importar clave privada
      *  Subir clave pública al keyserver de mailevelope
      *  Importar claves publicas
      *  Enviar un mensaje cifrado y descifrar mensaje.
  
  5. **Firma un documento encriptado y verifica**
      * Firma el docuento testamento.txt pero está vez lo vas a encriptar para que únicamente lo pueda leer el compañero notario (importar clave secreta) 
   1.  **Firma claves de compañeros para crear un circulo de confianza** 
     * [Tutorial](https://gist.github.com/F21/b0e8c62c49dfab267ff1d0c6af39ab84)

 