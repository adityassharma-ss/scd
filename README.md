
Your manager has asked you to work on documenting and improving the configuration of thresholds and polling conditions for alerts and ticket creation in SCOM (System Center Operations Manager). Here’s how you can understand, process, and implement this request:


---

What Does This Mean?

1. Thresholds: These are the predefined limits or conditions set in SCOM that trigger alerts when crossed (e.g., CPU usage > 90% for 5 minutes).


2. Polling Conditions: These refer to how often SCOM checks for specific metrics or conditions (e.g., every 1 minute, 5 minutes).


3. Alerting and Ticket Creation: When thresholds are breached, SCOM generates alerts. Some alerts may automatically create tickets in the incident management system.


4. Purpose: The aim is to:

Document existing configurations.

Identify and adjust thresholds that might be too close or overly sensitive.

Provide stakeholders with a clear reference.





---

How Are You Going to Process Through This?

1. Understand Current Configurations:

Log into SCOM and review the existing thresholds and polling intervals for key monitoring metrics.

Identify alert rules and their triggers.

Note down escalation workflows tied to alerts (e.g., ticket creation).



2. Review Historical Data:

Analyze past incidents and alerts to identify patterns of false positives or missed critical events.

Determine if any thresholds or polling conditions need adjustments.



3. Engage Stakeholders:

Discuss with team members or stakeholders to understand their expectations and requirements for alerting.

Confirm any specific metrics they want closely monitored or thresholds they consider critical.



4. Document Findings:

Create a detailed document listing all thresholds, polling conditions, and associated alert rules.

Highlight any configurations you recommend modifying.





---

What Do You Have to Do?

1. Inventory Monitoring Rules:

List all active monitoring rules, thresholds, and their polling conditions.

Note which rules create tickets automatically.



2. Evaluate Thresholds:

Identify thresholds that are too tight or too loose.

Check for "OR" conditions that might lead to unexpected alerts.



3. Propose Changes:

Suggest adjustments to thresholds and polling intervals based on historical data and stakeholder input.

Include reasoning for each change in your documentation.



4. Create a Reference Document:

Compile all information into an easy-to-reference format (e.g., Excel sheet or Word document).

Ensure it’s clear and shareable with stakeholders.





---

How Are You Going to Do This?

1. Access SCOM:

Log in to SCOM and navigate to monitoring and alert rules.

Export configurations if possible for easier documentation.



2. Analyze Historical Alerts:

Use SCOM’s reporting tools to review alerts over a specific period.

Identify patterns of false positives or ineffective alerts.



3. Collaborate with Teams:

Schedule discussions with relevant teams to validate findings and gather insights.



4. Draft the Document:

Organize data by category (e.g., CPU, Memory, Disk, Network).

Include details like threshold value, polling interval, alert severity, and ticket workflow.



5. Share and Iterate:

Present the document to your manager and stakeholders for review.

Incorporate feedback and finalize.





---

Solution Deliverables

1. Comprehensive Document:

Contains all thresholds, polling intervals, and alert configurations.

Includes recommendations for improvements.



2. Action Plan for Updates:

List of changes to be implemented in SCOM.

Timeline for completing updates.



3. Improved Monitoring Setup:

Reduced false positives and missed critical alerts.

Easy reference for stakeholders.




This approach ensures a thorough understanding of the existing setup, identifies areas of improvement, and provides a clear solution to meet the requirements.

