# app/prompts/cloud_prompts.py

aws_policy_prompt = """
You are a cloud security expert. Generate an AWS IAM policy in JSON format that satisfies the following requirements:
- Service: {service_name}
- Security Requirement: {security_requirement}

Ensure that the policy is compliant with AWS best practices.
"""

azure_policy_prompt = """
You are a cloud security expert. Generate an Azure security policy in JSON format that satisfies the following requirements:
- Service: {service_name}
- Security Requirement: {security_requirement}

Ensure that the policy is compliant with Azure security standards.
"""

gcp_policy_prompt = """
You are a cloud security expert. Generate a GCP security policy in JSON format that satisfies the following requirements:
- Service: {service_name}
- Security Requirement: {security_requirement}

Ensure that the policy follows GCP best practices.
"""
