
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
	* Grafana
	* Alloy
	* Loki
	* Mimir
	* Tempo
	* srv1
	* srv2
	* srv3
 ```bash
incus$ incus launch images:ubuntu/24.04 grafana --network asirnetwork      
incus$ incus list -n4st
```
Instalación de paquetes y repositorios necesarios
```bash
incus$ incus exec <instance> -- bash -c 'apt-get update && apt-get -y install  aptitude wget bash-completion gpg' 
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
## Loki

## Mimir

## Tempo
