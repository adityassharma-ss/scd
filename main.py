from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from src.utils.config import Config

class AIModel:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=Config().get_openai_api_key(),
            temperature=0.7,
            model_name="gpt-3.5-turbo"
        )
        
    def generate_scd(self, cloud, service, control_name, description, user_prompt):
        prompt = ChatPromptTemplate.from_template(
            """You are a cloud security expert. Generate a detailed security control definition based on the following:
            Cloud: {cloud}
            Service: {service}
            Control Name: {control_name}
            Description: {description}
            User Prompt: {user_prompt}
            
            Provide the Implementation Details, Responsibility, Frequency, and Evidence required.
            Format your response as follows:
            Implementation Details: [Your detailed implementation steps]
            Responsibility: [Who is responsible]
            Frequency: [How often this control should be checked/implemented]
            Evidence: [What evidence is required to prove compliance]
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            response = chain.run(cloud=cloud, service=service, control_name=control_name, 
                                 description=description, user_prompt=user_prompt)
            return response.strip()
        except Exception as e:
            print(f"Error generating SCD: {e}")
            return None
