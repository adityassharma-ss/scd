
	•	
<NonSystemDriveErrorMBytesThreshold>1000</NonSystemDriveErrorMBytesThreshold>
<NonSystemDriveErrorPercentThreshold>5</NonSystemDriveErrorPercentThreshold>
<TimeoutSeconds>360</TimeoutSeconds>
<DebugFlag>false</DebugFlag>

5.2 Windows Server 2012 Configuration

<SystemDriveWarningThreshold>500</SystemDriveWarningThreshold>
<SystemDriveErrorThreshold>300</SystemDriveErrorThreshold>
<NonSystemDriveWarningThreshold>2000</NonSystemDriveWarningThreshold>
<NonSystemDriveErrorThreshold>1000</NonSystemDriveErrorThreshold>

5.3 AD Server Configuration

<IntervalSeconds>3600</IntervalSeconds>
<TimeoutSeconds>300</TimeoutSeconds>
<ThresholdWarn>20</ThresholdWarn>
<ThresholdError>10</ThresholdError>

6. Governance & Compliance

6.1 Ownership & Responsibilities

Role	Responsibility
IT Operations	Monitor alerts, resolve incidents
Infrastructure Team	Optimize disk space utilization
Security Team	Ensure compliance with IT policies
Business Owners	Impact assessment for critical applications

6.2 Escalation Matrix

Alert Type	Action	Escalation Level
Warning	Notify IT Support	IT Operations
Critical	Trigger Incident	Infrastructure Team
Critical (Unresolved)	Escalate to Management	IT Director

6.3 Reporting & Audit
	•	Monthly reports on disk space trends.
	•	Automated incident tracking via ITSM tools.
	•	Quarterly compliance reviews for adherence to storage policies.

7. Appendix

7.1 Performance Counters Used

Counter Name	Description
LogicalDisk % Free Space	Measures available space percentage
LogicalDisk Free Megabytes	Measures available MB space

7.2 Incident Response Checklist
	•	Step 1: Identify impacted servers.
	•	Step 2: Free up space (log rotation, cleanup scripts).
	•	Step 3: Review historical trends.
	•	Step 4: Implement preventive measures (storage expansion, archiving).

8. Conclusion

This Disk Space Alert System ensures proactive monitoring, alerting, and resolution of disk space issues across Windows and AD servers. The structured approach aligns with enterprise IT governance, compliance, and incident management best practices.

Would you like to customize any section further, such as adding automation scripts or integration details for ServiceNow or Splunk?
