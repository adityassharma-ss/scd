# app/models/policy_request.py
from pydantic import BaseModel

class PolicyRequest(BaseModel):
    service_name: str
    security_requirement: str
