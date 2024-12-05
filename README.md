SCOM Windows Monitoring Setup Documentation
1. Introduction to SCOM

System Center Operations Manager (SCOM) is a Microsoft enterprise-grade tool designed to monitor the health, performance, and availability of IT services and infrastructure in both on-premise and cloud environments. It enables centralized monitoring of critical components such as:

    Infrastructure Components: Domain controllers, Active Directory, DHCP, DNS, Hypervisors, etc.
    System Features: CPU, memory metrics, storage, and network statistics.

SCOM provides insights through comprehensive dashboards, enabling proactive issue resolution and optimized IT operations.
2. Components of SCOM
a) Management Group

) Management Group

The Management Group is the core logical entity in a SCOM deployment, encompassing all objects, configurations, and data. It functions similarly to a domain or Active Directory and serves as the foundation of the SCOM hierarchy.

Key aspects include:

    Contains multiple Management Servers and Databases based on the environment.
    Provides centralized management and scalability for monitoring services.

b) Management Server

The Management Server plays a crucial role in collecting, processing, and analyzing data received from agents installed on monitored systems. It also communicates with the databases for storing configurations and operational data.
c) Operations Console

The Operations Console is the administrative interface for connecting to and managing the SCOM environment. It allows authorized users to perform tasks such as:

    Configuring monitors and rules.
    Accessing performance reports.
    Monitoring health statuses.

d) Operational Database

This SQL-based database stores real-time operational data such as configurations, customizations, and management packs. It interacts with the Management Server for live updates and quick troubleshooting.
e) Data Warehouse Database

The Data Warehouse (DW) is a historical database for storing log changes, performance data, and reporting metrics.

    Default retention period: 300 days.
    Used for long-term analytics and compliance reporting.

f) Web Console

The Web Console is a browser-based interface for remote monitoring of tasks and operational health. However, this feature is not implemented in the current environment.
g) Reporting Server

This server generates reports based on data from the DW database. Currently, Grafana is utilized for reporting in the absence of a dedicated reporting server.
h) Gateway Server

The Gateway Server bridges communication between agents and the Management Server in different domains. Certificate-based authentication is used in its absence.
3. Monitoring Scope

SCOM is configured to monitor:

    Core Metrics: CPU, memory, storage, and network performance.
    Services: Backup tasks, scheduled jobs, and application URLs.
    Custom Monitoring: Configurable rules and monitors for specific applications or services.

4. Scope of Work
SCOM Administration

    Setting up and managing Management Groups.
    Installing, updating, and removing agents.
    Configuring service and event monitoring.
    Creating and customizing monitoring rules.

URL Monitoring

Configuring HTTP/HTTPS monitors for applications.
Agent Management

Troubleshooting agent issues and ensuring proper data flow to the Management Server.
Reporting

Generating and analyzing reports from the Data Warehouse or Grafana dashboards.
5. Environment Overview
Production Environment

    3 Management Servers.
    2 Databases (Operational and DW).

Dev Environment

    2 Management Servers.
    1 Database shared between instances.

Legacy Monitoring

    Older servers are monitored using a separate SCOM 2016 environment due to compatibility issues.

6. Key Metrics and Limits

    Simultaneous Operations Console Users: 50.
    Agent-Monitored Computers: 3000.
    Agent-Managed Linux/Unix Systems: 6000.

7. Best Practices
Infrastructure Design

    Use high-availability configurations for Management and Database Servers.
    Maintain separate environments for development, QA, and production to ensure operational stability.

Security

    Use certificate-based authentication for agents in untrusted domains.
    Grant role-based access control (RBAC) to limit administrative privileges.

Monitoring Optimization

    Avoid excessive rule/monitor creation to prevent data overload.
    Regularly archive and clean up the Data Warehouse to improve performance.

Automation

    Automate agent deployment via tools like Chef or Ansible.
    Schedule regular database backups and performance tuning.

8. Data Flow

    Agent: Collects performance and health data from monitored systems.
    Management Server: Aggregates and processes data from agents.
    Operational Database: Stores current configurations and performance metrics.
    Data Warehouse: Logs historical data for analytics and reporting.
    Console/Grafana: Provides real-time visualization and reporting.

This document outlines the current setup, responsibilities, and optimization strategies for SCOM at Kenvue. Please review and provide feedback for additional details or customizations.
