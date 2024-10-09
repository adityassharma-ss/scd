import pandas as pd
from langchain_openai import ChatOpenAI
from src.utils.config import Config

class AIModel:
    def __init__(self):
        # Initialize the OpenAI model
        self.model = ChatOpenAI(api_key=Config().get_openai_api_key(), temperature=0.7)

    def generate_scd(self, cloud, service, control_name, description):
        """Generate a security control definition using AI model."""
        prompt = (
            f"You are a cloud security expert. Generate a detailed security control definition based on the following:\n"
            f"Cloud: {cloud}\n"
            f"Service: {service}\n"
            f"Control Name: {control_name}\n"
            f"Description: {description}\n"
            f"Provide the Implementation Details, Responsibility, Frequency, and Evidence required.\n"
        )

        try:
            messages = [{"role": "user", "content": prompt}]
            response = self.model.invoke(messages)
            response_text = response.content
            clean_response = response_text.strip()
            return clean_response
        except Exception as e:
            print("Error generating SCD:", e)
            return None
