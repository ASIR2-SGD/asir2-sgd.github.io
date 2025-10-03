
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
incus$ incus exec grafana -- apt-get update && apt-get install aptitude wget bash-completion gpg 
 ```
 
## Grafana
**Instalar y configurar grafana**
* Añadir repositorios zabbix
```bash
incus$ incus shell grafana
grafana$ wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor > /etc/apt/keyrings/grafana.gpg
grafana$ echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | tee /etc/apt/sources.list.d/grafana.list
grafana$ apt-get update && apt-get -y install grafana
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

## Loki

## Mimir

## Tempo
