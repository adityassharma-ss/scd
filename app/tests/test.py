# app/tests/test_policy_generation.py
import pytest
from app.services.policy_generation_service import generate_policy

@pytest.mark.asyncio
async def test_generate_aws_policy():
    service_name = "S3"
    security_requirement = "Encrypt data at rest"
    
    policy = await generate_policy(service_name, security_requirement)
    assert "Statement" in policy  # Check if valid AWS IAM policy structure
