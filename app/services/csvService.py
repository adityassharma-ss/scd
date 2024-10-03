# app/services/csv_service.py
import csv

def load_policies(csv_file_path: str):
    policies = []
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            policies.append(row)
    return policies

def find_policy(service_name: str, security_requirement: str, policies: list):
    for policy in policies:
        if policy["ServiceName"].lower() == service_name.lower() and \
           policy["SecurityRequirement"].lower() == security_requirement.lower():
            return policy
    return None
