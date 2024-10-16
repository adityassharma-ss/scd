{
  "scd_examples": [
    {
      "Control ID": "SCD-001",
      "Control Name": "Secure Data Encryption at Rest",
      "Description": "Ensure all data stored in the cloud service is encrypted at rest using industry-standard encryption algorithms.",
      "Implementation Details": [
        "Enable server-side encryption for all storage services.",
        "Use AES-256 encryption for data at rest.",
        "Implement key rotation policies.",
        "Store encryption keys in a secure key management service."
      ],
      "Responsibility": "Shared",
      "Review Frequency": "Quarterly Review",
      "Evidence Source": "Encryption configuration settings, key management logs"
    },
    {
      "Control ID": "SCD-002",
      "Control Name": "Multi-Factor Authentication (MFA)",
      "Description": "Implement multi-factor authentication for all user accounts to enhance access security.",
      "Implementation Details": [
        "Enable MFA for all user accounts, especially for privileged users.",
        "Support various MFA methods (e.g., SMS, email, authenticator apps, hardware tokens).",
        "Enforce MFA on all critical operations and sensitive data access.",
        "Regularly review and update MFA policies and supported methods."
      ],
      "Responsibility": "Customer",
      "Review Frequency": "Monthly Review",
      "Evidence Source": "MFA configuration settings, access logs, user account audit reports"
    }
  ]
}
