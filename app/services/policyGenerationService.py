# app/services/policy_generation_service.py
import json
from app.services.csv_service import load_policies, find_policy
from app.core.config import settings

csv_file_path = settings.csv_file_path  # path to the CSV file

def get_policy(service_name: str, security_requirement: str):
    policies = load_policies(csv_file_path)
    policy_data = find_policy(service_name, security_requirement, policies)

    if not policy_data:
        raise Exception(f"No policy found for service {service_name} and requirement {security_requirement}")
    
    policy_json = json.loads(policy_data["JSONPolicy"])
    best_practice = policy_data["BestPractice"]
    
    return policy_json, best_practice
