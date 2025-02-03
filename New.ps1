Subject: SCOM URL Migration & Monitoring – Next Steps

Hi Rahul,

Good afternoon!

For the SCOM URL Migration & Monitoring, we’ve completed 25 IAM Group URLs, which were moved to centralized Grafana under the Cyber - IAM Group. Now, we need to finalize the approach for the remaining 264 URLs.

Key Points:

Support Group Mapping: URLs need ticket creation on alerts. How do we map them to support groups?

Pre-work: The Kenvue team needs to complete groundwork before migration.

Migration Process: URLs will be added to black-box exporter, configured, and deployed via Helm charts in AWS-EKS (FinOps Cluster).

Alerting & Monitoring: Ignio integration is done, but alert verification depends on the Lerio team. Grafana dashboards need to be set up.


Query:

Previously, URLs were grouped under Cyber - IAM Group in Grafana.

Should we follow the same approach or place them directly in the directory?


Let’s connect to finalize the plan.

Thanks,
[Your Name]


