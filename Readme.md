Got it! Here’s the formal document with the correct thresholds:

Change Implementation: Logical Disk Free Space Threshold in SCOM

Document Version
	•	Version: 1.0
	•	Created By: [Your Name]
	•	Reviewed By: [Reviewer’s Name]
	•	Approved By: [Approver’s Name]
	•	Date: [DD-MM-YYYY]

1. Purpose

This document outlines the process to modify the Logical Disk Free Space Monitor in System Center Operations Manager (SCOM) by updating existing alert thresholds and adding a new critical threshold at 5% free space.

2. Background

Currently, SCOM generates alerts based on the following thresholds:
	•	Warning Alert at 10% free space (90% utilization)
	•	Critical Alert at 5% free space (95% utilization)

To improve monitoring granularity, the thresholds will be adjusted as follows:
	•	Warning Alert at 15% free space (85% utilization)
	•	Critical Alert 1 at 10% free space (90% utilization)
	•	Critical Alert 2 at 5% free space (95% utilization)

3. Scope
	•	Applies to: All Windows Server 2012 & 2016 instances monitored by SCOM.
	•	Impacted Services: Disk space monitoring and alerting.
	•	Stakeholders: IT Operations, Infrastructure Team, SCOM Administrators.

4. Implementation Steps

4.1 Verify Existing Monitor & Management Packs
	1.	Open SCOM Operations Console.
	2.	Navigate to Authoring → Monitors.
	3.	Search for “Logical Disk Free Space” under Windows Server 2012/2016 Logical Disk.
	4.	Verify the existing thresholds and ensure that the required Management Packs are installed:
	•	Microsoft.Windows.Server.Library
	•	Microsoft.Windows.Server.2016.Discovery

	Note: If these are missing, import them before proceeding.

4.2 Override the Existing Monitor
	1.	Open the existing Logical Disk Free Space Monitor.
	2.	Right-click and select Overrides → Override for all objects of class: Windows Server 2016 Logical Disk.
	3.	Locate the Warning Threshold parameter and change it from 10% to 15% free space.
	4.	Locate the Critical Threshold parameter and change it from 5% to 10% free space.
	5.	Click Apply and OK.

4.3 Create a New Monitor for 5% Free Space Alert

Since the existing monitor will now generate a critical alert at 10%, a new monitor is required for 5% free space (95% utilization).

Steps to Create the New Monitor
	1.	Navigate to Authoring → Monitors.
	2.	Right-click Monitors → Create a Unit Monitor.
	3.	Select “Aggregate Rollup Monitor” → Performance-based Monitor Type.
	4.	In Target, select Windows Server 2016 Logical Disk.
	5.	Click Next, and configure the thresholds:
	•	Healthy Condition: More than 10% free space.
	•	Critical Condition: Less than 5% free space.
	6.	Configure Alert Settings:
	•	Name: Logical Disk Free Space - Critical at 5%.
	•	Severity: Critical.
	•	Description: Logical disk utilization has reached 95%. Immediate action required.
	7.	Save the monitor in a Custom Management Pack (e.g., Custom.Windows.Server.Monitors).

4.4 Validate & Deploy
	1.	Restart the SCOM Health Service on affected servers:

Restart-Service HealthService


	2.	Test by filling up a disk beyond 85%, 90%, and 95% utilization to confirm all alerts trigger correctly.
	3.	Monitor the SCOM Console for alert generation.
	4.	If errors occur, check:
	•	Targeting (ensure correct logical disk class).
	•	Management Pack dependencies.
	•	Alert parameter values.

5. Rollback Plan

If issues arise:
	1.	Revert the monitor overrides back to their previous values.
	2.	Disable the new 5% threshold monitor in SCOM.
	3.	Restart the Health Service on affected servers.
	4.	Verify that only the 15% warning and 10% critical alerts are active.

6. Change Management & Approval
	•	Change Request ID: [CR Number]
	•	Implementation Date: [Planned Date]
	•	Implementation Owner: [Your Name]
	•	Approval Status: Pending/Approved

7. References
	•	Microsoft SCOM Documentation: [Insert link]
	•	IT Operations Monitoring Policy: [Insert link]

This document is now ready to be added to Confluence. Let me know if you need any modifications!

