from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from src.utils.config import Config

class AIModel:
    def __init__(self):
        # Initialize the OpenAI model with LangChain and temperature control for creativity
        self.model = ChatOpenAI(api_key=Config().get_openai_api_key(), temperature=0.7)
    
    def generate_scd(self, cloud, service, control_name, description, user_prompt):
        """Generate Security Control Definitions using the AI model based on user input."""
        
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
            # Debugging: Show the prompt being sent to the model
            print(f"Prompt sent to the model:\n{prompt}")
            messages = [{"role": "user", "content": prompt}]
            
            # Call the AI model to generate a response
            response = self.model.invoke(messages)
            response_text = response.content
            
            # Clean the response
            clean_response = response_text.strip()
            if not clean_response:
                print("Model returned an empty response.")
                return None
            
            return clean_response
        
        except Exception as e:
            print(f"Error generating SCD: {e}")
            return None
