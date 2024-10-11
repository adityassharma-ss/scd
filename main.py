# Updated ai_model.py

import openai
import pandas as pd
from langchain_openai import ChatOpenAI
from src.utils.config import Config

class AIModel:

    def __init__(self):
        # Initialize the OpenAI model
        self.model = ChatOpenAI(api_key=Config().get_openai_api_key(), temperature=0.7)

    def generate_scd(self, cloud, service, control_name, description, user_prompt):
        """Generate a security control definition using AI model based on user input."""
        prompt = (
            f"You are a cloud security expert. Generate a detailed security control definition based on the following:\n"
            f"Cloud: {cloud}\n"
            f"Service: {service}\n"
            f"Control Name: {control_name}\n"
            f"Description: {description}\n"
            f"User Prompt: {user_prompt}\n"
            f"Provide the Implementation Details, Responsibility, Frequency, and Evidence required.\n"
        )
        
        try:
            print(f"Prompt sent to the model:\n{prompt}")  # Debugging: show the prompt
            messages = [{"role": "user", "content": prompt}]
            response = self.model.invoke(messages)
            response_text = response['content']
            clean_response = response_text.strip()

            if not clean_response:
                print("Model returned an empty response.")
            return clean_response

        except Exception as e:
            print("Error generating SCD:", e)
            return None

    def train_model(self, training_data_path):
        """Placeholder for a custom fine-tuning model function."""
        # For now, we'll assume we pass a dataset (CSV or other format)
        df = pd.read_csv(training_data_path)
        print(f"Training data loaded: {df.head()}")
        # Use the data to fine-tune the model.
        # This could involve calling APIs or building your custom AI model.
        pass
