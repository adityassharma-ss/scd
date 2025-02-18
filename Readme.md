Core Components
Node Exporter:

Deployed on every server to collect system-level metrics (CPU, memory, disk I/O, network stats, etc.).
Acts as a lightweight agent that exposes metrics in a Prometheus-compatible format.
Prometheus Server:

Centralized time-series database that scrapes metrics from Node Exporter instances.
Provides powerful querying, alerting (via Alertmanager), and storage capabilities.
Grafana:

Visualization layer that will be reconfigured to use Prometheus as its primary data source.
Offers customizable dashboards for real-time insights.
Alertmanager:

Replaces ElastAlert to manage and dispatch alerts based on Prometheus rules.
Supports grouping, inhibition, and silencing of alerts.
Enabling Technologies
Ansible:
Automates the installation, configuration, and deployment of Node Exporter across all servers.
Ensures consistent configurations and streamlines the rollout process.
Facilitates integration with Prometheus by updating scrape configurations and managing firewall rules if necessary.
