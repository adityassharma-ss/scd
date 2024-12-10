Azure Monitoring with Prometheus: Full Implementation Guide


---

1. Overview

Azure Monitoring with Prometheus allows you to collect, query, visualize, and alert on metrics for applications running in Azure. While Azure Monitor is Azure's native solution, Prometheus provides an open-source, Kubernetes-native approach to metric monitoring. Integration of Prometheus with Azure can be achieved using Azure Monitor Managed Service for Prometheus or through custom Prometheus server deployments.


---

2. Why Use Prometheus with Azure?

Kubernetes-native: Prometheus is designed for Kubernetes (AKS) and can scrape metrics from pods, nodes, and custom exporters.

Custom Metrics: Prometheus allows you to collect custom application metrics.

Alerting: Use Prometheus Alertmanager to create alerts based on metric conditions.

Integration with Grafana: Prometheus metrics are easily visualized in Grafana, offering robust dashboards.

Open-Source Flexibility: Avoid vendor lock-in with a fully open-source stack.



---

3. Key Components

Prometheus: For scraping and storing metrics.

Alertmanager: For routing alerts.

Node Exporter: For server-level metrics.

Application Exporters: Exporters for MySQL, Nginx, Redis, and more.

Grafana: For dashboard visualization.

Azure Monitor Managed Service for Prometheus: A fully managed Prometheus-compatible monitoring service.

Azure Kubernetes Service (AKS): Kubernetes cluster where workloads run.



---

4. Implementation Options

Option 1: Azure Monitor Managed Service for Prometheus

Pros: Fully managed, scales automatically, no infrastructure management.

Cons: Costs associated with the managed service.


Option 2: Self-hosted Prometheus in AKS

Pros: Full control, open-source, custom scraping configurations.

Cons: You manage scaling, storage, and upgrades.



---

5. Implementation Steps


---

Option 1: Azure Monitor Managed Service for Prometheus

1. Prerequisites

Azure CLI installed.

Owner or Contributor access to the Azure subscription.

Azure Kubernetes Service (AKS) cluster.



2. Enable Prometheus on Azure Monitor

az feature register --namespace "Microsoft.Insights" --name "Prometheus"
az provider register --namespace Microsoft.Insights


3. Install Prometheus for AKS

az aks enable-addons --resource-group <RESOURCE_GROUP> --name <AKS_CLUSTER_NAME> --addons monitoring


4. Access Metrics in Azure Monitor

Go to Azure Portal > Monitor > Metrics.

Select Prometheus (Preview).

Use KQL (Kusto Query Language) to query Prometheus metrics.



5. Alerting

Go to Azure Monitor > Alerts.

Create an alert rule using PromQL-based metrics.

Configure actions for alert notifications.





---

Option 2: Self-hosted Prometheus in AKS

1. Set up AKS Cluster

az aks create --resource-group <RESOURCE_GROUP> --name <AKS_CLUSTER_NAME> --node-count 2 --generate-ssh-keys
az aks get-credentials --resource-group <RESOURCE_GROUP> --name <AKS_CLUSTER_NAME>


2. Install Prometheus Using Helm

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace


3. Access Prometheus UI

kubectl port-forward --namespace monitoring svc/prometheus-server 9090:80

Visit: http://localhost:9090 to access the Prometheus UI.


4. Set up Grafana

helm install grafana grafana/grafana --namespace monitoring

Access Grafana UI:

kubectl port-forward --namespace monitoring svc/grafana 3000:3000

Default credentials: admin/admin


5. Add Prometheus Data Source in Grafana

URL: http://prometheus-server.monitoring:80

Add dashboards for Kubernetes, system, and custom application metrics.



6. Set up Exporters

Node Exporter:

helm install node-exporter prometheus-community/prometheus-node-exporter --namespace monitoring

Custom Application Exporters: Add instrumentation libraries in Python, Go, or Java apps to expose custom metrics.



7. Set up Alertmanager

Update alertmanager.yml configuration to define alert rules.

Send notifications to email, Slack, PagerDuty, etc.





---

6. Prometheus Configuration

Prometheus Scrape Configuration

scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        target_label: __address__
        regex: (.+)


---

7. Prometheus Metrics Examples


---

8. Prometheus Alerting

Alert Rule Example:

groups:
- name: kubernetes
  rules:
  - alert: HighCPUUsage
    expr: sum(rate(container_cpu_usage_seconds_total[5m])) by (pod) > 0.85
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High CPU usage detected on pod {{ $labels.pod }}"
      description: "The CPU usage for pod {{ $labels.pod }} has been over 85% for the last 5 minutes."

Sending Alerts to Slack:

Set up a webhook URL in Slack.

Configure alertmanager.yml:


receivers:
  - name: 'slack'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/XXXX/XXXX/XXXX'
        channel: '#alerts'
        send_resolved: true


---

9. Querying with PromQL

Examples of PromQL queries:

CPU Usage for Pods:

sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)

Memory Usage for Pods:

container_memory_usage_bytes / 1024 / 1024

Number of Restarts for Pods:

increase(kube_pod_container_status_restarts_total[1h])

Disk Usage:

node_filesystem_size_bytes{fstype="ext4"} - node_filesystem_free_bytes{fstype="ext4"}



---

10. Best Practices

Use Azure Monitor Managed Service if you don't want to manage infrastructure.

Scale Prometheus: Use Thanos or Cortex for large-scale setups.

Alerting: Configure alerts for critical resource usage and pod restarts.

Data Retention: Set up long-term storage for Prometheus metrics using Azure Blob Storage or Thanos.

Export Custom Metrics: Use libraries like prom-client for Node.js, prometheus-client for Python, or prometheus_client for Golang.



---

11. Conclusion

Azure provides managed Prometheus via Azure Monitor for easy integration.

For full control, you can deploy Prometheus in AKS.

Leverage Grafana dashboards, Alertmanager alerts, and PromQL queries for robust observability.

Use Azure Monitor for scalable, managed solutions. For full customization, opt for self-hosted Prometheus.


This guide provides a complete approach to implementing Prometheus for monitoring in Azure. Let me know if you'd like any specific section explained further.


