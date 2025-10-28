---
layout: default
title: "Lista de control de accesos ACL"
---
# Lista de control de accesos (ACL)

## Contexto
Una vez un usuario ha sido autenticado, el sistema debe darle acceso solo a los recursos a los que ha sido autorizado por parte del administrador. Esta definición de roles y permisos, se consigue mediante la definición de usuarios y grupos y la lista de control de accesos (ACL, Access Control List).

## Objetivos
* Entender la creación de usuarios y grupos en el sistema operativo Linux así como sus permisos sobre los recursos.
* Entender la creación de listas de control de acceso asi como sus definiciones de persmisos.
* Llevar a cabo una implementación de un supuesto caso de autorización mediante ACL.
* Desarrollar, verificar y documentar la práctica.
  
## Sistema de permisos nativos del sistema operativo linux.

Los permisos se aplican sobre **elementos del sistema de archivos**, tales como archivos regulares, directorios, sockets Unix, enlaces simbólicos, nodos de dispositivos, etc.
* Lectura (**`r`**: Read): la entidad asociada podrá leer el elemento.
* Escritura (**`w`**: Write): la entidad asociada podrá escribir o modificar el elemento.
* Ejecución (**x**: eXecution): la entidad asociada podrá ejecutar el elemento.

Las entidades sobre las que tienen vigencia estos permisos son:

* Usuario dueño (**`u`**: User): usuario dueño del elemento en el sistema de archivos.
 * Grupo al que pertenece (**`g`**: Group): grupo al que pertenece el elemento.
* Otros usuarios (**`o`**: Others): el resto de los usuarios del sistema que no son ni el dueño del elemento, ni pertenecen al grupo del elemento.


![posix permisions]({% link /resources/img/acl_posix_perm.jpeg %})

### Limitaciones
Estos permisos tienen algunas limitaciones. Consideremos el siguiente ejemplo:
```bash
 drwxr-xr--  1 diego usuarios  916 Jun  7 20:51 miarchivo.sh
 ```
Aquí el usuario dueño, `diego`, tiene permisos de lectura, escritura y ejecución sobre el archivo `miarchivo.sh`, los usuarios que pertenecen al grupo `usuarios` pueden leer y ejecutar este archivo, y el resto de los usuarios del sistema solamente pueden leer dicho archivo.

Si quisiéramos que el usuario `juan` pueda modificar este archivo podríamos tomar varios cursos de acción, pero todas ellas limitadas y en detrimento de los permisos actuales.
### ACL 
Las solución pasa por hacer uso de representaciones de permisos para elementos del sistema de archivos, que **extienden** los permisos nativos POSIX

#### Acl mínimas
Son las equivalentes a los permisos POSIX
![Acl mínimas]({% link /resources/img/acl_minimas.jpeg %})

#### Acl extendidas
Cuando hablamos de **ACL extendidas** (con máscara), las clases de permisos de usuario dueño y otros coinciden con los que vemos en la salida de `ls -l`, pero la clase de **permisos de grupo** puede contener entradas de **usuarios o grupos nombrados** adicionales
![acl extendidas]({% link /resources/img/acl_extendidas.jpeg %})

#### Instalación de acl
```bash
apt-get install acl
```
#### Otorgando permisos a grupos y usuarios
```bash
setfacl -m u:uaa:rw- archivo.txt
setfacl -m u:usuario1:rw-,u:usuario2:r--,g:grupo1:r-- archivo.txt
```

En el caso de que el destino sea un directorio y quisiéramos aplicar la ACL a todos los elementos interiores de manera recursiva, podemos utilizar el modificador `-R`:
```bash
setfacl -Rm u:usuario1:rw- directorio/
```
Para eliminar una ACL creada por error podemos utilizar el modificador `-x` o `--remove`.
```bash
setfacl -x u:uaa archivo.txt
```
Dicho sea de paso, podemos eliminar todas las ACL’s creadas para un archivo o directorio utilizando el modificador `-b` (o `--remove-all`) de esta forma:
```bash
setfacl -b archivo.txt`
```

Muchas veces es necesario que todos los elementos, archivos o directorios, que sean creados dentro de un directorio, obtengan las mismas ACL’s que el directorio padre. Esto puede lograrse con el modificador `-d` o `--default` de `setfacl`
```
setfacl -dm u:andy:r directorio/
```
La máscara marcará el **límite máximo** de permisos de la clase grupo actualmente configurados, y se actualizará cada vez que carguemos una nueva ACL.
Podemos modificar la máscara como cualquier otro permiso
```bash
setfacl -m m::r archivo.txt
```

Los permisos nativos, también tienen representación en acl y por lo tanto pueden modificarse con el comando `setfacl`

Los siguientes comandos son equivalentes
```bash
chmod u+rwx archivo.txt
setfacl -m u::rwx archivo.txt
```

```bash
chmod g+r archivo.txt
setfacl -m g::r archivo.txt
```
## Actividad
En una nueva instancia de incus denominada `acl`:
* Crea una carpeta denominada /shared con la siguiente estructura de ficheros y directorios.
```bash
root@acl:~# tree /shared
/shared
├── aula13
├── aula14
├── aula82
├── comun
└── misc
```

Usando los comandos `adduser`y `addgroup`
Crea los siguientes usuarios y grupos, agrega los usuarios al grupo indicado:
```bash
students:x:1006:
teachers:x:1007:
asir2:x:1008:asir2_1,asir2_2
smr1a:x:1009:smr1a_1,smr1a_2
asir1:x:1010:asir1_1,asir1_2
```

```bash
asir2_1:x:1005:1006:asir2_1,,,:/home/asir2_1:/bin/bash
asir2_2:x:1004:1006:asir2_2,,,:/home/asir2_2:/bin/bash
asir1_1:x:1006:1006:asir1_1,,,:/home/asir1_1:/bin/bash
asir1_2:x:1007:1006:asir1_2,,,:/home/asir1_2:/bin/bash
smr1a_1:x:1009:1006:smr_a_1,,,:/home/smr1_a_2:/bin/bash
smr1a_2:x:1010:1006:smr_a_1,,,:/home/smr1_a_1:/bin/bash
teacher1:x:1011:1007:teacher1,,,:/home/teacher1:/bin/bash
teacher2:x:1012:1007:teacher2,,,:/home/teacher2:/bin/bash
```

>[!TIP]
> Con fines educativos y de prueba, puedes crear usuarios sin necesidad de indicar la contraseña con el siguiente comando
> ```bash
> adduser --disabled-password --ingroup <group> --shell /bin/bash --gecos "nombre" <username>
> ```

>[!NOTE]
> Comprueba que tu configuración de usuarios y grupos coincide con la deseada mediante el comando ```gentent group``` y ```getent passwd```
>

Asigna los permisos a cada recurso según lo indicado en la tabla
**TODO**

| Recurso          | Student Access | Teachers Access | Extra     |
| ---------------- | -------------- | --------------- | --------- |
| ./shared/aula13/ | aula13:r       |                 |           |
| ./shared/aula14/ | aula14:r       |                 | asir2:rwx |
| ./shared/aula82/ | aula82:r       |                 |           |
| ./shared/comun/  | dsd            |                 |           |
| ./shared/misc/   | dsd            |                 |           |
|                  | dsd            |                 |           |


### Comprobación y verificación
Diseña un escenario de prueba creando ficheros y carpetas nuevas y cambiando de usuario para llevar a cabo las comprobaciones de permisos necesarios.

### Entrega
Entrega un `bash script`que automatice completamente, desde la creación de directorios, grupos e usuarios así como la asignación de permisos *acl* para llevar a cabo la actividad completa.

Vuelca la ejecución el comando ```getfacl -R <carpeta>``` en un fichero denominado getfacl_nombre_alumno.txt

>[!WARNING]
> El fichero entregado se debe ejecutar sin ningún error y reproducir el escenario esperado de la actividad.

