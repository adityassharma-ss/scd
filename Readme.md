Data Flow
Node Exporter runs on every Linux server and exposes metrics on port 9100.
Prometheus scrapes data from all Node Exporter instances at regular intervals.
Prometheus stores the time-series data for historical analysis.
Alertmanager triggers alerts based on predefined rules (e.g., high CPU usage, disk failure).
Grafana queries Prometheus to create dashboards and visualize real-time server performance.
