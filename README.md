SCOM Windows Monitoring Setup & Working


---

1. Introduction to SCOM

System Center Operations Manager (SCOM) is a comprehensive enterprise-grade monitoring tool from Microsoft, designed to provide real-time visibility into the health, performance, and availability of IT services and infrastructure. SCOM supports both on-premises and cloud-based environments, enabling centralized monitoring of critical components.

Key Features of SCOM:

Infrastructure Monitoring: Tracks health, availability, and performance of domain controllers, Active Directory, DHCP, DNS, hypervisors, and other essential services.

System Monitoring: Monitors system metrics like CPU, memory, storage, and network usage.

Centralized Dashboards: Provides real-time insights and visual representations for proactive issue resolution.



---

2. Components of SCOM

a) Management Group

The Management Group is the logical foundation of the SCOM architecture. It consists of:

Multiple Management Servers: Enables load balancing and high availability.

Databases: Operational Database and Data Warehouse are part of the Management Group.

Centralized Control: Provides a unified view and streamlined management for all SCOM components.


b) Management Server

The Management Server is responsible for:

Data Collection & Processing: Gathers data from agents on monitored systems.

Communication: Sends and receives updates from the Operational Database and Data Warehouse.

Agent Management: Deploys, upgrades, and maintains SCOM agents.


c) Operations Console

The Operations Console is the primary interface used by administrators for:

Monitoring Health & Alerts: Tracks system health and raises alerts.

Configuring Monitors & Rules: Sets up monitoring rules and thresholds.

Accessing Reports: Allows access to performance and health reports.


d) Operational Database (OpsDB)

The Operational Database is a SQL-based database that stores:

Real-Time Data: Configuration data, health status, and current operational state.

Temporary Storage: Supports fast queries and quick troubleshooting.


e) Data Warehouse Database

The Data Warehouse Database serves as long-term storage for historical data:

Retention Period: Default of 300 days.

Data Storage: Stores performance metrics, event data, and log changes.

Reporting Source: Used to generate reports for compliance and auditing.


f) Web Console

The Web Console is a browser-based tool for remote access to SCOM data.

Access Anywhere: View system health and performance remotely.

Lightweight Option: No need to install the full Operations Console.


g) Reporting Server

The Reporting Server generates detailed reports using Data Warehouse data.

Report Customization: Custom reports can be created for performance and compliance.

Grafana Integration: In some cases, Grafana is used as an alternative to visualize reports.


h) Gateway Server

The Gateway Server acts as an intermediary for agent communication when agents are in different domains.

Secure Communication: Uses certificate-based authentication.

Cross-Domain Support: Allows agents in untrusted domains to communicate with the Management Server.



---

3. Installing, Uninstalling, and Upgrading SCOM Agent

The SCOM Agent plays a critical role in collecting data from monitored systems and forwarding it to the Management Server.

Key Communication Ports


---

a) Installing the SCOM Agent

Method 1: Using SCOM Console

1. Launch the Operations Console.


2. Navigate to Administration > Device Management > Agent Managed.


3. Right-click and select Discovery Wizard.


4. Choose Windows Computers as the Discovery Type.


5. Enter the domain credentials with permissions to install agents.


6. Add the system by specifying the computer name(s) or IP range.


7. Select the discovered target system and assign it to the Management Server.


8. Complete the installation using default or custom settings.


9. Verify the agent in Agent Managed.



Method 2: Manual Installation

1. Copy the SCOM agent installer from the SCOM Management Server (e.g., C:\Program Files\Microsoft System Center\OperationsManager\Server\Agent).


2. Launch the MOMAgent.msi file.


3. Accept the license agreement and configure the target system's Management Server details.


4. Complete the installation and verify in the Operations Console.



Method 3: Command-Line Installation

msiexec.exe /i MOMAgent.msi /qn USE_SETTINGS_FROM_AD=0 MANAGEMENT_GROUP=<ManagementGroupName> MANAGEMENT_SERVER=<ManagementServerFQDN>


---

b) Repairing the SCOM Agent

Method 1: Repair via SCOM Console

1. Open Control Panel > Programs and Features.


2. Locate Microsoft Monitoring Agent in the list of installed programs.


3. Click Change and select Repair.


4. Follow the wizard instructions and restart the server if prompted.



Method 2: Repair via Command Line

msiexec.exe /fa MOMAgent.msi /qn

Method 3: Repair Using PowerShell

Get-SCOMAgent -DNSName <FQDN> | Repair-SCOMAgent


---

c) Uninstalling the SCOM Agent

Method 1: Uninstall via SCOM Console

1. Go to Administration > Agent Managed.


2. Select the target system.


3. Right-click and choose Uninstall.



Method 2: Manual Uninstallation

1. Go to Control Panel > Programs and Features.


2. Locate Microsoft Monitoring Agent.


3. Click Uninstall and follow the prompts.




---

d) Upgrading the SCOM Agent

Method 1: Automatic Upgrade

1. Enable Automatic Agent Updates from Administration > Settings > Agent.


2. Agents will automatically upgrade during policy synchronization.



Method 2: Manual Upgrade

1. Obtain the latest agent installer from the SCOM Management Server.


2. Follow the manual installation process to overwrite the existing version.



Method 3: Command-Line Upgrade

msiexec.exe /i MOMAgent.msi /qn USE_SETTINGS_FROM_AD=0 MANAGEMENT_GROUP=<ManagementGroupName> MANAGEMENT_SERVER=<ManagementServerFQDN>


---

4. Best Practices for SCOM Setup

1. Port Management: Ensure all necessary ports are open to allow communication between components.


2. Agent Health Checks: Use PowerShell commands to check agent health.


3. Database Maintenance: Regularly maintain the Data Warehouse and OpsDB for optimal performance.


4. Monitoring Rules: Configure custom rules and alerts for critical system metrics.


5. Load Balancing: Use multiple Management Servers to distribute workloads.


6. Agentless Monitoring: Leverage agentless monitoring where possible to reduce administrative overhead.




---

5. Conclusion

System Center Operations Manager (SCOM) is a robust monitoring solution that provides comprehensive insights into IT infrastructure health, performance, and availability. By utilizing its key components—Management Servers, Databases, Agents, and Gateway Servers—organizations can ensure optimal performance of critical systems. Implementing best practices, maintaining communication ports, and following effective installation, repair, and upgrade processes will ensure a seamless monitoring experience.

References

1. System Center Solutions - Infrastructure Monitoring | Microsoft


2. Secure your Infrastructure Monitoring with SCOM | Microsoft Community Hub




