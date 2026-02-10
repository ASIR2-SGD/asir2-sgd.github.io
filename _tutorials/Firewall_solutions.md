---
layout: default
title: "firewall_iptables"
---
# Práctica Firewall.
## Soluciones
```bash
#!/usr/bin/nft -f

flush ruleset

table inet filter {
	#Define sets for efficiency
	set web_ports {
		type inet_service
		elements = {80,443,8080,8443}
	}	
	
	set admin_ips {
		type ipv4_addr
		elements = {10.10.81.100}
	}	
	chain input {
		type filter hook input priority filter; policy drop;
	
			
		iif lo accept comment "allow from loopback";
		ip protocol icmp accept comment "allow icmp";
		ct state {established,related} accept comment "allow tracked connections";
		iif {lan,dmz} udp dport 53 accept comment "accept dns req";
		iif {lan,dmz} udp dport 67 accept comment "accept dhcp req";
		iif wan udp dport 68 accept comment "accept dhcp ack";
		iif lan tcp dport 22 ip saddr @admin_ips accept comment "accept ssh connections from admin ips"
	}

	chain forward {
		type filter hook forward priority filter; policy drop;

		iif lan oif wan ip protocol icmp accept comment "allow icmp";
		iif lan oif wan tcp dport @web_ports  accept comment "allow icmp";
		ct state {established,related} accept comment "allow tracked connections";
	}

	chain output {
		type filter hook output priority filter; policy drop;
		
		oif lo accept comment "allow from loopback";
		ip protocol icmp accept comment "allow icmp";
		ct state {established,related} accept comment "allow tracked connections";
		oif wan udp dport 53 accept comment "allow dns req";
		oif {lan,dmz} udp dport 68 accept comment "allow dhcp ack";
		oif wan udp dport 67 accept comment "allow dhcp req";
		oif wan tcp dport @web_ports accept comment "allow web req";
	}
}
table inet nat {
	chain postrouting {
		type nat hook postrouting priority srcnat; policy accept;
		oifname "wan" masquerade
	}
}
```