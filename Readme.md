A. Deploy Node Exporter on All Linux Servers
Installation Steps (Automated using Ansible):

Download Node Exporter binary on each Linux server.
Extract the binary and move it to /usr/local/bin/.
Create a systemd service to ensure Node Exporter runs at startup.
Enable the service and verify it is exposing metrics on http://localhost:9100/metrics.
