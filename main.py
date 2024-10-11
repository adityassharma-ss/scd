import openai
import pandas as pd
from src.utils.config import Config

class AIModel:
    def __init__(self):
        # Initialize the OpenAI model with API key and parameters
        self.model = openai.ChatCompletion.create(
            model="gpt-4", 
            api_key=Config().get_openai_api_key(), 
            temperature=0.7
        )

    def generate_scd(self, cloud, service, control_name, description, user_prompt):
        """Generate a security control definition using AI model based on user input."""
        prompt = (
            f"You are a cloud security expert. Generate a detailed security control definition based on the following:\n"
            f"Cloud: {cloud}\n"
            f"Service: {service}\n"
            f"Control Name: {control_name}\n"
            f"Description: {description}\n"
            f"User Prompt: {user_prompt}\n"
            f"Provide the Implementation Details, Responsibility, Frequency, and Evidence required."
        )

        try:
            print(f"Prompt sent to the model:\n{prompt}")  # Debugging: show the prompt
            response = self.model.create(prompt=prompt, max_tokens=500)
            response_text = response['choices'][0]['message']['content']
            clean_response = response_text.strip()

            if not clean_response:
                print("Model returned an empty response.")
                return None

            return clean_response
        except Exception as e:
            print("Error generating SCD:", e)
            return None

    def train_model(self, dataset):
        """Placeholder for future functionality to fine-tune the model at an organizational level."""
        # This method could be expanded to fine-tune the AI model based on the organization's specific needs.
        # Placeholder function as OpenAI currently only supports fine-tuning for certain models.
        pass
