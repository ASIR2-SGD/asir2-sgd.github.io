---
layout: default
title: Radius
---
# Práctica radius.
## Implementación de un servidor de autenticación basando en raidus e integración con LDAP

## Contexto
RADIUS (del inglés Remote Access Dial In User Service) es un protocolo que destaca por ofrecer un mecanismo de seguridad, flexibilidad, capacidad de expansión y una administración simplificada de las credenciales de acceso a un recurso de red
Los servidor RADIUS son ampliamente usados por los operadores de Internet (PPPoE), pero también se utilizan mucho en las redes WiFi de hoteles, universidades o en cualquier lugar donde queramos proporcionar una seguridad adicional a la red inalámbrica

## Links
* [Freeradius instalation and configuration](https://simplificandoredes.com/en/freeradius-installation-and-configuration)

## Objetivos
* Implentar un servidor de autenticación RADIUS con integración a un directorio LDAP donde tendremos nuestros usuarios.
* Configurar un punto de acceso que proporcionan conectividad WiFi con autenticación WPA2/WPA3-Enterprise.
* Desarrollar un plan de actuación para llevar a cabo la práctica, generando y organizando los pasos necesarios para que esta concluya de forma exitosa.

## Desarrollo

### Pasos previos
* Actualizar los tests correspondientes

### LDAP
* Crear el nodo raiz aul82.local

>[!WARNING]
> El comando _dpgk-reconfigure_ creará un nuevo árbol eliminando cualquier configuración anterior (TLS, Contraseña administrador). No será necesario ejecutarlo si dc=aula82,dc=local ya está creado y con los usuarios insertados.

```bash
$sudo dpkg-reconfigure slapd
```

Idicar aula82.local como _domain name_

* Agregar los usuarios de radius
```bash
$ldapadd -D cn=admin,dc=aula82,dc=local -w 1 -H ldap:// -f add-system-users.ldif
```

* Agregar el usuario _freerad_ para leer al contraseña desde el servidor radius
```bash
$ldapadd -D cn=admin,dc=aula82,dc=local -w 1 -H ldap:// -f add-freerad-user.ldif
```

* Modificar las ACL para que el usuario _freerad_ tenga permisos de lectura sobre el atributo _userPassword_
```bash
$sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f modify-freerad-userpassword-read-permisions.ldif
```

### Freeradius
* instalar los paquetes
```bash
$sudo apt-get install freeradius freeradius-ldap
```

* Agregar el usuairo vagrant al grupo freeradius
```bash
$sudo usermod -G freerad vagrant
```

* Activar el módulo ldap en freeradius
```bash
$sudo -u freerad bash -c "cd /etc/freeradius/3.0/mods-enabled 
&& ln -s ../mods-available/ldap"
```

* Configurar el módulo ldap Activar el módulo ldap en freeradius
```bash
$sudo vi /etc/freeradius/3.0/mods-enabled/ldap
```
Cambiar las lineas indicadas con los siguientes valores
```bash
19  server = 'localhost'
28  identity = 'cn=freerad,dc=aula82,dc=local'
29  password = 1
33  base_dn= 'dc=aula82,dc=local'
```

* Permitir la conexión de clientes de la red del aula
```bash
$sudo vi /etc/freeradius/clients.conf
```
Agregar las lineas indicadas
```bash
316 client vagrant-int-network {
317         ipaddr          = 172.0.82.0/24
318         secret          = testing123
319 }
320 
321 
322 client aula82-network {
323         ipaddr          = 192.168.82.0/24
324         secret          = testing123
325 }

```

* Reiniciar el servicio freeradius
```bash
$sudo systemctl restart freeradius.service
```

## Comprobación
* Probar conectividad del cliente mediante la utilidad _radtest_
```bash
$radtest -x alumno 1 172.0.82.1 1812 aula82-network-password
```

* Probar conectividad desde el AP


>[!NOTE]
> A realizar por el alumno

