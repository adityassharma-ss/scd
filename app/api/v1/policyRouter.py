# app/api/v1/policy_router.py
from fastapi import APIRouter, HTTPException
from app.models.policy_request import PolicyRequest
from app.services.policy_generation_service import get_policy

router = APIRouter()

@router.post("/generate_policy", summary="Generate cloud security policy")
async def generate_policy_api(request: PolicyRequest):
    try:
        policy, best_practice = get_policy(request.service_name, request.security_requirement)
        return {"policy": policy, "best_practice": best_practice}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
