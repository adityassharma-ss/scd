from langchain_openai import OpenAI
from src.utils.config import Config

class AIModel:
    def __init__(self):
        self.model = OpenAI(api_key=Config().get_openai_api_key(), temperature=0.7)

    def generate_scd(self, cloud, service, control_name, description):
        """Generate a security control definition using AI model"""
        prompt = (
            f"You are a cloud security expert. Generate a detailed security control definition for the following:\n\n"
            f"Cloud: {cloud}\n"
            f"Service: {service}\n"
            f"Control Name: {control_name}\n"
            f"Description: {description}\n\n"
            f"Include:\n"
            f"- Implementation Details\n"
            f"- Responsibilities (cloud provider/customer)\n"
            f"- Audit frequency\n"
            f"- Evidence Required\n"
            f"- Additional Details\n"
        )

        try:
            response = self.model.invoke(prompt)
            return response.strip()
        except Exception as e:
            print(f"Error generating SCD: {e}")
            return "Error generating SCD"
