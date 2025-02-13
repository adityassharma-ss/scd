Monitoring Configuration Update: Logical Disk Free Space Thresholds

Document Information

Document Title	Logical Disk Free Space Monitoring Configuration Update
Version	1.0
Author	[Your Name]
Department	IT Operations
Date	[Date]
Reviewed By	[Reviewer Name]
Approved By	[Approver Name]
Status	Approved
Classification	Internal Use Only

Objective

This document provides a detailed step-by-step guide to updating Logical Disk Free Space Monitoring thresholds in SCOM (System Center Operations Manager) to improve alerting and response times for low disk space situations.

Key Changes:
	1.	Warning threshold updated from 10% to 15%.
	2.	Critical threshold updated from 5% to 10%.
	3.	Additional Critical alert introduced at 5%.

Scope
	•	Applies to Windows Server 2012 & 2016 instances monitored via SCOM.
	•	Targets Logical Disk Free Space (%) under Windows Performance Counters.
	•	Implements Static Threshold Monitoring with Single and Double Thresholds.

Implementation Approach

To meet the new alerting requirements, two types of monitors will be created:
	1.	Double Threshold Monitor
	•	Triggers a Warning at 15%.
	•	Triggers a Critical Alert at 10%.
	•	Reduces the number of monitors needed by combining both alerts into one.
	2.	Single Threshold Monitor (Simple)
	•	Triggers a Critical Alert at 5%.
	•	Ensures the lowest threshold still generates an alert separately.

Step-by-Step Configuration in SCOM

Step 1: Create a Double Threshold Monitor (15% Warning, 10% Critical)

1.1 Open the Operations Console
	1.	Log in to the SCOM Operations Console.
	2.	Navigate to Authoring → Expand Management Pack Objects → Click Monitors.

1.2 Create a New Monitor
	1.	Right-click Monitors → Create a Monitor → Unit Monitor.
	2.	Select:
	•	Windows Performance Counters
	•	Static Thresholds
	•	Double Threshold
	3.	Click Next.

1.3 Define Monitor Settings
	1.	Name: Logical Disk Free Space - Warning & Critical
	2.	Description: Triggers a warning at 15% and critical at 10%.
	3.	Select Management Pack:
	•	Choose an unsealed management pack (e.g., Custom.Windows.Server.Monitors).
	•	Avoid saving in a sealed Microsoft MP.
	4.	Click Next.

1.4 Set Target & Parent Monitor
	1.	Target: Windows Server 2016 Logical Disk.
	2.	Parent Monitor: Availability.
	3.	Click Next.

1.5 Configure Performance Counter
	1.	Click Select → Choose:
	•	Object: LogicalDisk
	•	Counter: % Free Space
	•	Instance: _Total
	•	Click OK.
	2.	Click Next.

1.6 Set Thresholds
	1.	Warning Threshold: 15%
	2.	Critical Threshold: 10%
	3.	Click Next.

1.7 Configure Health States
	1.	Healthy: Free Space > 15%
	2.	Warning: 10% ≤ Free Space < 15%
	3.	Critical: Free Space < 10%
	4.	Click Next.

1.8 Configure Alerts
	1.	Enable ✅ “Generate an alert for this monitor”.
	2.	Alert Name: Logical Disk Free Space - Warning & Critical
	3.	Severity:
	•	Warning: Medium
	•	Critical: High
	4.	Alert Description:

Warning: Logical disk $Data/Context/Property[@Name='DeviceID']$ free space is below 15%.  
Critical: Logical disk $Data/Context/Property[@Name='DeviceID']$ free space is below 10%. Immediate action required.


	5.	Click Create.

Step 2: Create a Single Threshold Monitor (5% Critical Alert)

2.1 Open the Operations Console

Follow Step 1.1 to navigate to Monitors.

2.2 Create a New Monitor
	1.	Right-click Monitors → Create a Monitor → Unit Monitor.
	2.	Select:
	•	Windows Performance Counters
	•	Static Thresholds
	•	Single Threshold
	3.	Click Next.

2.3 Define Monitor Settings
	1.	Name: Logical Disk Free Space - Critical at 5%
	2.	Description: Triggers a critical alert when logical disk free space falls below 5%.
	3.	Select Management Pack: Choose the same unsealed MP as before.
	4.	Click Next.

2.4 Set Target & Parent Monitor
	1.	Target: Windows Server 2016 Logical Disk.
	2.	Parent Monitor: Availability.
	3.	Click Next.

2.5 Configure Performance Counter

Follow Step 1.5 to select % Free Space.

2.6 Set Threshold
	1.	Threshold Type: Simple
	2.	Operator: Less than
	3.	Threshold Value: 5
	4.	Click Next.

2.7 Configure Health States
	1.	Healthy: Free Space > 10%
	2.	Critical: Free Space < 5%
	3.	Click Next.

2.8 Configure Alerts
	1.	Enable ✅ “Generate an alert for this monitor”.
	2.	Alert Name: Critical: Logical Disk Free Space Below 5%
	3.	Severity: High
	4.	Alert Description:

The free space on logical disk $Data/Context/Property[@Name='DeviceID']$ has fallen below 5%. Immediate action required.


	5.	Click Create.

Step 3: Validate the Configuration

3.1 Restart SCOM Health Service

Run the following command on monitored servers:

Restart-Service HealthService

3.2 Simulate Low Disk Space
	•	Fill a disk until it reaches 85%, 90%, and 95% usage.
	•	Check the SCOM Monitoring Console for the alerts.

3.3 Verify Alerts in SCOM
	1.	Navigate to Monitoring → Windows Computers.
	2.	Select a test machine → Open Health Explorer.
	3.	Confirm that:
	•	Warning Alert appears at 15%.
	•	Critical Alert appears at 10%.
	•	Additional Critical Alert appears at 5%.

Conclusion
	•	The new thresholds (15%, 10%, and 5%) ensure better visibility into disk space issues.
	•	Double Threshold reduces unnecessary monitors.
	•	Separate 5% Critical Alert ensures extreme conditions are flagged.

Next Steps

✅ Upload to Confluence under [Monitoring Configuration Updates].
✅ Notify NOC / IT Operations Team about the change.
✅ Monitor alert behavior for one week.

Let me know if you need modifications!
