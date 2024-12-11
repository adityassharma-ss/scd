Azure Observability & Monitoring Document

Document Details

Document Title: Azure Observability & Monitoring Strategy

Created By: Sharma, Aditya [Non-Kenvue]

Date: December 06, 2024



---

1. Introduction

Effective observability and monitoring are critical for ensuring the health, security, and performance of Azure-based applications and infrastructure. This document outlines the comprehensive approach, key log types, monitoring services, automation strategies, and best practices for achieving world-class observability in Azure environments.


---

2. Logging and Monitoring Strategy

The goal is to establish a unified strategy for managing, configuring, and monitoring logs for both application and infrastructure layers in Azure. This strategy ensures end-to-end visibility, anomaly detection, and issue resolution.


---

3. Key Log Types

3.1 Application Logs

These logs capture events and activities related to the application layer.

Application Insights Logs: Diagnostic and request data from Azure Application Insights.

Error Logs: Capture exceptions and errors during runtime.

Performance Metrics: Metrics related to latency, throughput, and resource utilization.


3.2 Infrastructure Logs

These logs track system resources and infrastructure components.

Virtual Machines (VMs): Startup/shutdown events, batch processing, and OS-level events.

Kubernetes Clusters (AKS): Logs for container lifecycle events, resource usage, and network interactions.


3.3 Traffic Logs

These logs provide network-related activity details.

Network Flow Logs: Track inbound/outbound traffic data.

Firewall Logs: Capture rule evaluations and security-related events.


3.4 Security Logs

These logs ensure auditability and compliance.

User Access Logs: Track user login attempts, access patterns, and authentication events.

Unauthorized Access: Identify and record unauthorized access attempts.


3.5 Netman Logs

These specialized logs are used for network management and troubleshooting.

Bandwidth Monitoring: Track bandwidth usage.

Routing Issues: Identify routing errors.

Service-Level Agreements (SLA): Monitor SLA adherence for network performance.



---

4. Log Processing and Standards

4.1 Automated Logging Configuration

Automation: Log configurations are automated using Terraform, enabling consistent setup for diagnostic settings, storage, and monitoring.

Destination: Logs are routed to Log Analytics Workspaces, Event Hubs, and Storage Accounts.

Default Configurations: Default diagnostic settings automatically capture standard logs to reduce manual intervention.


4.2 Log Standards

Timestamps: Logs use ISO 8601 timestamps for precise event correlation.

Structured Logs: JSON-like structured logs make querying efficient.

Query Capabilities: Use Kusto Query Language (KQL) for filtering and analyzing logs.



---

5. Monitoring Services

5.1 Azure Application Insights

Application Performance Monitoring (APM): Captures request/response times, exceptions, and dependency calls.

End-to-End Visibility: Provides a comprehensive view of the application's health.

Integration: Integrated with Azure Monitor for advanced analysis.


5.2 Log Analytics Workspace

Centralized Logging: Aggregates logs from multiple Azure services.

Features: Enables queries, dashboards, and trend analysis.

Querying: Users can filter logs by service, type, and severity.


5.3 Azure Storage Accounts

Storage for Logs: Logs are automatically stored in Azure Storage Accounts.

Automation: Terraform automates the configuration of diagnostic settings.


5.4 Virtual Machines (VMs)

Diagnostics: Logs startup/shutdown events and batch processing activities.

Automation: Terraform automates the configuration of logging and monitoring on VMs.


5.5 OpenSearch Integration

Agent Installation: Logs from containerized services are captured via agents.

Container Logs: Ensures lifecycle events and diagnostics are logged.



---

6. Tenant and Region Management

6.1 Tenant Segregation

Global Tenants: Operate across multiple regions (East US, South-East Asia, Europe).

China Tenants: Dedicated environment with strict compliance measures.


6.2 Multi-Region Management

Custom Terraform Modules: Tailored for regional and tenant-specific configurations.

Compliance: Unique configurations for China to meet compliance requirements.



---

7. Migration and Cost Optimization

7.1 Incremental Migration

Phased Approach: Services are migrated incrementally to maintain system stability.

Validation: Logs are compared post-migration to ensure parity with the original environment.


7.2 Cost Optimization

Open-Source Tools: Evaluate OpenSearch for cost-effective log analysis.

Service Consolidation: Eliminate redundancy across multi-cloud environments.



---

8. Challenges and Recommendations

8.1 Log Filtering

Filtering at Ingestion: Reduce log volume by filtering unnecessary data at ingestion.

Filter Criteria: Use severity levels (error, warning, informational) and service types (e.g., VM, storage).


8.2 Scaling Diagnostic Settings

Complexity: Managing diagnostic settings for multiple services and regions is challenging.

Solution: Automate configuration using Terraform to maintain consistency.


8.3 Network Monitoring

Network Feasibility: Ongoing efforts with the network feasibility team to enhance traffic log monitoring.

Tools: Use Azure Network Watcher for advanced monitoring.



---

9. Best Practices

9.1 Automation and Standardization

Use Terraform to automate log configurations across all Azure services.

Maintain standardized log formats for consistency.


9.2 Dedicated Log Analytics Workspaces

Allocate dedicated workspaces for key teams to ensure isolation and logical separation.


9.3 Proactive Monitoring

Define Alerts: Configure alerts for critical performance thresholds, downtime, and security issues.

Custom Dashboards: Create Azure Monitor dashboards for real-time insights.



---

10. Long-Term Goals

1. Open-Source Transition: Gradually adopt OpenSearch to reduce licensing costs.


2. Enhanced Dashboards: Develop dashboards using Azure Monitor and third-party visualization tools.


3. Continuous Improvement: Update Terraform modules as new Azure services are introduced.




---

11. Summary of Key Log Types


---

12. Glossary

KQL (Kusto Query Language): The query language used in Azure Monitor and Log Analytics for querying logs.

Log Analytics Workspace: Centralized repository for Azure logs.

Terraform: Infrastructure as Code (IaC) tool to automate Azure resource provisioning.

OpenSearch: Open-source alternative to Elasticsearch for log analysis and searching.

AKS: Azure Kubernetes Service, a managed Kubernetes service.



---

This document provides a complete strategy for observability and monitoring in Azure. It ensures effective log management, unified monitoring, and cost optimization while meeting multi-region compliance requirements. With automation using Terraform, the system remains scalable, auditable, and future-ready.


