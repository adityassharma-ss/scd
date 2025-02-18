Setting Up the New Monitoring Stack
Node Exporter Deployment:

Package the Node Exporter binary for the target Linux distributions.
Use Ansible to deploy the binary, configure it as a service (e.g., using systemd), and ensure it is set to start on boot.
Validate that Node Exporter is exposing metrics on the designated port (default 9100).
Prometheus Configuration:

Update the prometheus.yml configuration file to add new scrape targets. For example:
yaml
Copy
Edit
scrape_configs:
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['server1:9100', 'server2:9100', ...]
Ensure that Prometheus is able to reach all Node Exporter endpoints, adjusting firewall rules if needed.
Grafana & Alertmanager Setup:

Reconfigure Grafana to connect to Prometheus as the primary data source.
Import or recreate dashboards to reflect metrics from Node Exporter.
Set up Alertmanager with rules and notification channels to replace ElastAlert functionalities.
