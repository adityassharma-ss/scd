B. Deploy Prometheus on a Central Monitoring Server
Download and install Prometheus.
Create the Prometheus configuration file (prometheus.yml).
Define scrape jobs to collect metrics from all Node Exporter instances.
Start Prometheus and verify it's scraping data.
Example Prometheus Configuration (/etc/prometheus/prometheus.yml):

```
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'node_exporter'
    static_configs:
      - targets:
        - 'server1:9100'
        - 'server2:9100'
        - 'server3:9100'
