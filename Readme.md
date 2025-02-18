C. Deploy Alertmanager for Notifications
Install Alertmanager on the Prometheus server.
Configure alerting rules to notify on high CPU, memory, or disk issues.
Define notification channels (Email, Slack, PagerDuty, etc.).
Example Alert Rule (/etc/prometheus/alert.rules.yml):

```
groups:
  - name: High CPU Alert
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 90
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High CPU Usage on {{ $labels.instance }}"
          description: "The CPU usage has been above 90% for the last 5 minutes."
```
