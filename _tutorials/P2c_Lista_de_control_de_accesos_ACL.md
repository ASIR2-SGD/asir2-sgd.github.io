# Práctica 2c. Lista de control de accesos (ACL)

## Contexto
Una vez un usuario ha sido autenticado, el sistema debe darle acceso solo a los recursos a los que ha sido autorizado por parte del administrador. Esta definición de roles y permisos, se consigue meidnate la definición de usuarios y grupos y la lista de control de accesos (ACL, Access Control List).

## Objetivos
* Entender la creación de usuarios y grupos en el sistema operativo Linux así como sus permisos sobre los recursos.
* Entender la creación de listas de control de acceso asi como sus definiciones de persmisos.
* Llevar a cabo una implementación de un supuesto caso de autorización mediante ACL.
* Desarrollar, verificar y documentar la práctica.
  

## Desarrollo
### Paso 1. Pasos previos
#### Instalación y verificación de ACL
#### Directorios y usuarios

>[!NOTE]
> Explicar y mostrar mediante el comando tree la estructura de ficheros y directorios creada

>[!NOTE]
> Resumir en una tabla los permisos para cada recurso
>


| Recurso                       | Student Access  | Teachers Access   | Extra           |
|-----------                    |-----------      |---                |---              |  
| ./Alumnos/Compartido/Comun    |    rwx          |                   |                 |
| ./Alumnos/Compartido/...    |   dsd             |                   | asir2:rwx       |
| ./Alumnos/Compartido/...    |   dsd             |                   |                 |
| ./Alumnos/Compartido/...    |   dsd             |                   |                 |
| ./Alumnos/Compartido/...    |   dsd             |                   |                 |
| ./Alumnos/Compartido/...    |   dsd             |                   |                 |




### Paso 2. Asignación de permisos a cada recurso
>[!NOTE]
> No es necesario mostrar todos los comandos ya que son repetitivos, únicamente los más representativos

### Paso 3.Comprobación y verificación
>[!NOTE]
> Llevar a cabo la comprobación cambiando de usuario y comprobando con uno o más casos postivos y negativos que el funcionamiento de la práctica es como se esperaba. 
