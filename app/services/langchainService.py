# app/services/langchain_service.py
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from app.core.config import settings

llm = OpenAI(openai_api_key=settings.openai_api_key, temperature=settings.model_temperature)

def create_policy_chain(service_name: str, security_requirement: str):
    prompt_template = PromptTemplate(
        input_variables=["service_name", "security_requirement"],
        template="""
        You are an expert in cloud security. Generate an AWS security policy for the following service:
        - Service: {service_name}
        - Security Requirement: {security_requirement}

        The output should be a JSON formatted policy that complies with AWS IAM standards.
        """
    )
    chain = llm.chain(prompt_template)
    return chain
