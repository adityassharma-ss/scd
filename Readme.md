5. Visualization Latency in Grafana
The latency between Azure Monitor collecting metrics and their visualization in Grafana depends on several factors, including data aggregation intervals, data export processes, and network conditions. Here's a detailed breakdown:

5.1. Data Aggregation and Availability:

Platform Metrics Collection: Azure Monitor collects platform metrics from Azure resources at regular intervals, typically every one minute. These metrics are pre-aggregated and stored in a time-series database. 
MICROSOFT LEARN - https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/data-platform-metrics?

Data Availability: After collection, there's a short processing delay before metrics become available for querying. This latency is generally around 3 minutes. 
MICROSOFT LEARN - https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/data-platform-metrics?
