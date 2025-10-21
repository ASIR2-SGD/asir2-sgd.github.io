---
layout: default
title: "Grafana stack metrics"
---

# Grafana Metrics Stack
La actividad consiste en obtener y visualizar la métrica de nuestra red simulada en _incus_ para ello deberemos crear y configurar varias instancias de _ubuntu 24.04_ cada una con su función que se describe brevemente a continuación:
* Grafana : Web UI app para la visualización de 
**Pasos**
* Crear red asir network
 ```bash
  incus$ incus network create asirnetwork \
      ipv4.address = 10.10.82.1/24 \
      ipv4.nat = true \ 
      ipv4.dhcp.ranges = 10.10.82.100-10.10.82.200 \
      ipv4.dhcp.routes = 0.0.0.0/0,10.10.82.1 \
      ipv6.address = none
      
  incus$ incus network show asirnetwork     
 ```
* Crear instancias para las máquinas:
	* grafana
	* alloy
	* loki
	* mimir
	* tempo
	* srv1
	* srv2
	* srv3

```bash
incus$ incus launch images:ubuntu/24.04 grafana --network asirnetwork      
incus$ incus list -n4st
```

Instalación de paquetes y repositorios necesarios

```bash
incus$ incus exec <instance> -- bash -c 'apt-get update && apt-get -y install  aptitude wget bash-completion gpg nano xsel vim' 
incus$ incus exec <instance> -- bash -c 'wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor > /etc/apt/keyrings/grafana.gpg'
incus$ incus exec <instance> -- bash -c 'echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | tee /etc/apt/sources.list.d/grafana.list'

```
 
## Grafana
**Instalar y configurar grafana**

* Añadir repositorios zabbix

```bash
incus$ incus exec grafana -- bash -c ' apt-get update && apt-get -y install grafana'
incus$ incus shell grafana
```

* Habilitar servicio al arranque

```bash
grafana$ systemctl enable grafana-server.service
grafana$ systemctl start grafana-server.service
```
* Comprueba que el servicio está escuchando
```bash
grafana$ ss -atunp
```

* Logging (admin/admin)

```bash
http://<ip-grafana>:3000
```

## Alloy
Alloy permite la recolección y procesamiento de los datos de telemetría de diferentes fuentes

```bash
incus$ incus exec alloy -- bash -c ' apt-get update && apt-get -y install alloy'
incus$ incus shell alloy

```

* Habilitar servicio al arranque

```bash
alloy$ systemctl enable alloy.service
alloy$ systemctl start alloy.service
```

* Comprueba que el servicio está escuchando

```bash
alloy$ ss -atunp
```

* Fichero configuración

```bash
/etc/default/alloy
/etc/alloy/config.alloy
```

* Permitir acceso remoto al UI

```bash
/etc/default/alloy
...
CUSTOM_ARGS = "--server.http.listen-addr=0.0.0.0:12345"
...
```

```bash
/etc/alloy/config.alloy

livedebugging {
  enabled = true
}
```

Podemos consultar el correcto funcionamiento de _Alloy_ a través de su [API](https://grafana.com/docs/alloy/latest/reference/http/)

```shell
curl alloy-ip:12345/-/ready
curl alloy-ip:12345/-/healthy
```

**Tareas**
* Configurar alloy para que obtenga métricas de si mismo [tutorial](https://grafana.com/docs/alloy/latest/collect/metamonitoring/)
* Obtener métrica de incus server y visualizar en grafana [tutorial](https://linuxcontainers.org/incus/docs/main/metrics/)
* Enviar los logs de incus server a loki [tutorial](https://linuxcontainers.org/incus/docs/main/server_config/#server-options-logging)
* Obtener métricas de un servidor linux a través de [node exporter](https://gist.github.com/nwesterhausen/d06a772cbf2a741332e37b5b19edb192)
* Obtener remote syslogs y reenviar a loki [tutorial](https://grafana.com/docs/alloy/latest/monitor/monitor-syslog-messages/)


## Loki

Loki almacena de forma eficiente los _logs_ que pueden ser explorados mediante un lenguaje de consulta (LogQL)

```bash
incus$ incus exec loki -- bash -c ' apt-get update && apt-get -y install loki'
incus$ incus shell loki
```

>[!WARNING]
>La configuración por defecto de loki no permite iniciar el servicio de forma correcta. Es necesario desactivar la opción *enable_multi_varian_queries: true* del fichero de configuración /etc/loki/config.yml

* Habilitar servicio al arranque

```bash
alloy$ systemctl enable loki.service
alloy$ systemctl start loki.service
```

* Comprueba que el servicio está escuchando

```bash
alloy$ ss -atunp
```

Podemos comprobar el correcto funcionamiento de _loki_ consultando la [API](https://grafana.com/docs/loki/latest/reference/loki-http-api/)

```bash
curl loki-ip:3100/ready
curl loki-ip:3100/services
```

## Mimir

[Mimir](https://grafana.com/docs/mimir/latest/get-started/) es una base de datos  compatible con _prometheus_ que permite configurar alertas.

```bash
incus$ incus exec mimir -- bash -c ' apt-get update && apt-get -y install mimir'
incus$ incus shell mimir
```

**Configuración**
Tras la instalación, debemos modificar la configuración de mimir, puedes descargar una configuració operativa para nuestros propósitos con el siguiene comando:

```bash
wget -O /etc/mimir/config.yml https://raw.githubusercontent.com/ASIR2-SGD/asir2-sgd.github.io/refs/heads/main/resources/files/mimir_config.yml
```

Reiniciar el servicio tras la configuración y comprobar que está activo al arranque

```bash
mimir$ systemctql restart mimir
mimir$ systemctl status mimir
```

Comprueba que el servicio está escuchando

```bash
mimir ss -atunp
```


Comprueba el estado de _mimir_ consultando la [API](Podemos comprobar el correcto funcionamiento de _loki_ consultando la [API](https://grafana.com/docs/loki/latest/reference/loki-http-api/)

```bash
curl mimir-ip:8080/ready
curl mimir-ip:8080/api/v1/user_stats
curl mimir-ip:8080/api/v1/status/flags
curl mimir-ip:8080/config
```

>[!NOTE]
>Para configurar _mimir_ como datasource en grafana deberás indicar la siguietne ruta en el campo _Connection_http://mimir-ip:port/prometheus


![grafana-mimir-dashboard]({% link /resources/img/grafana-mimir-dashboard.png %})
## Métricas de incus
Incus facilita enormemente la tarea de obtener valores de [métrica](https://linuxcontainers.org/incus/docs/main/metrics/) de  sus instancias que podemos obtener con el comando ```bash incus query /1.0/metrics```. Debemos exponerlas para que sean accesibles medianta la API, deberemos llevar a cabo algunos cambios en la configuración global

```bash
incus$ incus config set core.https_address ":8443"
incus$ incus config set core.metrics_address ":8444"
incus$ incus config set core.metrics_authentication false
```

De esta forma exponemos incus en la red , accede a ```bash https://incus-ip:8443``` y sigue los pasos para crear una conexión TLS necesaria.

Incus también puede enviar los logs a _loki_ llevando a cabo los siguientes cambios en la configuraición global.
```bash
incus$ incus config set logging.loki01.target.type  loki
incus$ incus config set logging.loki01.target.address  <loki-ip>:3100
incus$ incus config set logging.loki01.lifecycle.types  instance
incus$ incus config set logging.loki01.types lifecycle,network-acl,logging
```

Comprueba y corrige la configuraición global de incus en caso de que sea necesario mediante los comandos.

```bash
incus$ incus config show
incus$ incus config edit
```

## Actividad. Métricas apache/mysql
Se propone en la siguiente actividad que el alumno sea capaz de configurar los componentes vistos para visualizar la información e métrica de un servidor web apache.
**Pasos**
- [ ] Crear nueva instancia en incus denominada apache
- [ ] Instala y configura el servidor apache
- [ ] Expón los datos de métrica del servidor apache [tutorial](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/integrations/integration-reference/integration-apache-http/#before-you-begin)
- [ ] Configurar _alloy_ para que recoja los datos de métrica de apache y los almacene en _mirmir_.[Manual](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/integrations/integration-reference/integration-apache-http/#configuration-snippets-for-grafana-alloy)
- [ ] Muestra los datos en _grafana_


I