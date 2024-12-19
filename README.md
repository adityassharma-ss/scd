Task Documentation for Resolving SCOM Health Service Issue on Windows Server


---

Incident Details

Incident Number: INC000000453438
Server: MCCUSFWACPTSP1 (Windows Server 2016)
Service: CLOUDX-VIRTUAL HOSTING (OPC)
Environment: Production
Impact: Large
Urgency: Medium
Priority: P3

Issue:
The SCOM Health Service on MCCUSFWACPTSP1 is in an unhealthy state. The system failed to load certain rules, likely caused by cache corruption or connectivity issues after server migration from Nicom to Vemale.com.


---

Objective

Restore the health of the SCOM agent and re-establish connectivity with the SCOM Management Server.


---

Steps to Resolve

1. Initial Checks

Ping the server to check connectivity:

ping MCCUSFWACPTSP1

Check RDP access to the server.

Review Event Viewer (Applications & Services > Operations Manager) for SCOM errors.



---

2. Agent Health Check

Log in to the server via RDP.

Check if Microsoft Monitoring Agent (HealthService) is running:

services.msc

Check agent status:

cd "C:\Program Files\Microsoft Monitoring Agent\Agent"
momagent /status



---

3. Clear SCOM Agent Cache

1. Stop Health Service:

net stop HealthService


2. Clear Cache:

del /q "C:\Program Files\Microsoft Monitoring Agent\Agent\Health Service State\*"


3. Restart Health Service:

net start HealthService




---

4. Re-register SCOM Agent (if issue persists)

1. Remove and Reinstall Agent:

momagent /remove
momagent /install
momagent /register


2. Clear Cache Again:

momagent /clearcache


3. Restart Health Service:

net start HealthService




---

5. Validation

Check Event Viewer for SCOM-related Event IDs (2115, 2120, 21016).

Ensure MCCUSFWACPTSP1 appears as Healthy in the SCOM Console under Monitoring > Agent Health.

Verify DNS and connectivity to the management server:

Test-NetConnection -ComputerName <SCOM Management Server FQDN> -Port 5723



---

Issue Root Cause

The issue occurred due to cache corruption or connectivity issues during the migration from Nicom to Vemale.com.


---

Resolution Summary

Cleared the agent cache.

Restarted the Health Service.

Re-registered the SCOM agent.

Verified that the server was listed as Healthy in the SCOM Console.



---

Rollback Plan

1. Verify network connectivity and DNS lookup for the SCOM Management Server.


2. Restart the Health Service.


3. Re-check logs in Event Viewer.


4. Escalate to SCOM Admin if unresolved.




---

Reference Commands


---

Prepared By: [Your Name]
Date: [Date]
Reviewed By: [Reviewer Name]
Approval Status: Pending / Approved


