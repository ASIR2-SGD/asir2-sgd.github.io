---
layout: default
title: "Alloy Config file"
---

```bash
/etc/alloy/config.alloy
```

```bash
//Dashboard:3894

prometheus.exporter.apache "integrations_apache_http" {
  scrape_uri = "http://10.10.82.70/server-status?auto"
}

  

discovery.relabel "integrations_apache_http" {
targets = prometheus.exporter.apache.integrations_apache_http.targets
  rule {
    target_label = "instance"
    replacement  = constants.hostname
  }
  rule {
    target_label = "job"
    replacement  = "integrations/apache_http"
  }
}

  

prometheus.scrape "integrations_apache_http" {
  targets    = discovery.relabel.integrations_apache_http.output
  forward_to = [prometheus.remote_write.default.receiver]
  job_name   = "integrations/apache_http"
}


prometheus.remote_write "default" {
  endpoint {
	url = "http://mimir:8080/api/v1/push"

  }
}

livedebugging {
  enabled = true
}


```