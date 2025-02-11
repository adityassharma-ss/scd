Report: Citrix Broker Service Monitoring in SCOM

Summary

During a recent incident, the Citrix Broker Service (BrokerService) was found to be unmonitored in SCOM, leading to a lack of alerts when the service failed. This resulted in unavailability of Citrix applications and business disruption. The following report details the investigation, root cause analysis (RCA), remediation steps, and the process to enable SCOM monitoring for Citrix Broker Service.

1. Root Cause Analysis (RCA) for Missing Alerts

Findings:
	•	The Citrix Broker Service was not configured for monitoring in SCOM.
	•	Servers running this service were agent-managed, but the service itself was not included in SCOM monitoring scope.
	•	No Windows Service Monitor was set up for BrokerService.
	•	Due to this gap, no alerts were triggered when the service failed.

Root Cause:
	•	Missing Service Monitor: The Citrix Broker Service was not explicitly added to SCOM monitoring.
	•	Lack of Proper Configuration: No SCOM rule or monitor was created to track BrokerService.
	•	Absence of Citrix Management Pack: The necessary Citrix monitoring components were not installed in SCOM.

2. Remediation Steps Taken

1. Verified Service & Server Status in SCOM
	•	Confirmed that Citrix servers were listed in SCOM > Administration > Agent-Managed.
	•	Checked Health Explorer in SCOM to see if BrokerService was monitored (it was missing).

2. Created a New Windows Service Monitor
	•	In SCOM > Authoring > Management Pack Objects > Monitors, created a Basic Service Monitor for Citrix Broker Service (BrokerService).
	•	Targeted Windows Server Operating System for all Citrix servers.
	•	Configured an alert trigger when the service was not running.

3. Enabled Alerting & Notifications
	•	Set up an alert rule in SCOM with Critical Severity.
	•	Configured email/SMS notifications to the IT operations team.

4. Tested Monitoring & Alerts
	•	Manually stopped the Citrix Broker Service (net stop BrokerService).
	•	Verified alert generation in SCOM Monitoring.
	•	Restarted the service (net start BrokerService) to confirm alert resolution.

3. Next Steps & Preventive Measures
	1.	Expand Monitoring Scope: Ensure all Citrix services critical to application availability are monitored.
	2.	Regular Health Checks: Periodically review monitored services in SCOM.
	3.	Incident Review: Conduct monthly alert validation tests.
	4.	Update Confluence Documentation:
	•	Document the Citrix Broker Service monitoring process in Confluence.
	•	Include steps to verify, configure, and test alerts in SCOM.
	•	Ensure IT teams are trained on monitoring and alert response procedures.

Confluence Documentation Update

A new Citrix Broker Service Monitoring page should be created in Confluence under the Monitoring & Alerting section. It should include:
	•	Purpose: Explain why monitoring BrokerService is critical.
	•	Step-by-Step Guide:
	•	How to check if the service is being monitored.
	•	How to create a Windows Service Monitor in SCOM.
	•	How to set up alerts & notifications.
	•	Troubleshooting: Steps to validate alerts and resolve failures.

Final Outcome

✅ Citrix Broker Service is now monitored in SCOM.
✅ Alerts will trigger if the service fails.
✅ Preventive measures are in place to avoid future monitoring gaps.

This report ensures that Citrix Broker Service failures will no longer go unnoticed, reducing downtime and improving response times
