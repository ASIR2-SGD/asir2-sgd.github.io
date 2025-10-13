---
layout: default
title: "Alloy Config file"
---

```bash
/etc/alloy/config.alloy
```

```bash
// Sample config for Alloy.
//
// For a full configuration reference, see https://grafana.com/docs/alloy
logging {
  level = "warn"
  format = "json"
  write_to = [loki.write.default.receiver]
}

loki.write "default" {
  endpoint {
    url = "http://loki:3100/loki/api/v1/push"
  }
}

prometheus.exporter.unix "default" {
  include_exporter_metrics = true
  disable_collectors       = ["mdadm"]
}

prometheus.scrape "default" {
  targets = array.concat(
    prometheus.exporter.unix.default.targets,
    [{
      // Self-collect metrics
      job         = "alloy",
      __address__ = "127.0.0.1:12345",
    }],
  )

  forward_to = [
  // TODO: components to forward metrics to (like prometheus.remote_write or
  // prometheus.relabel).
  ]
}

prometheus.exporter.self "metamonitoring" {
}

prometheus.scrape "metamonitoring" {
  targets    = prometheus.exporter.self.metamonitoring.targets
  forward_to = [prometheus.remote_write.default.receiver]
}

prometheus.remote_write "prometheus" {
  endpoint {
	url = "http://prometheus:9090/api/v1/write"

	tls_config {
	  cert_file = "/etc/alloy/tls/alloy.crt"
	  key_file = "/etc/alloy/tls/alloy.key"
	  ca_file = "/etc/alloy/tls/prometheus.crt"
	  server_name = "prometheus"
	}
  }
}

prometheus.remote_write "default" {
  endpoint {
	url = "http://mimir:8080/api/v1/push"

  }
}

tracing {
  sampling_fraction = 0.1
  write_to	    = [otelcol.exporter.otlp.default.input]
}

otelcol.exporter.otlp "default" {
  client {
	endpoint = "http://tempo:3200"
  }
}

prometheus.scrape "incus" {
    scheme        = "https"
    metrics_path  = "/1.0/metrics"
    targets = [{
            __address__ = "10.10.10.1:8444",
            job         = "incus",
            }]
    tls_config {
            insecure_skip_verify = true
    }
    forward_to = [prometheus.remote_write.default.receiver]
}

livedebugging {
  enabled = true
}


```