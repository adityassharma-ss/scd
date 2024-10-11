from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from src.utils.config import Config

class AIModel:
    def __init__(self):
        self.model = ChatOpenAI(api_key=Config().get_openai_api_key(), temperature=0.7)
        self.dataset_summary = ""
        self.control_ids = {}

    def set_dataset_info(self, summary, control_ids):
        """Set the dataset summary and control IDs for the model to use"""
        self.dataset_summary = summary
        self.control_ids = control_ids

    def generate_scd(self, user_prompt, service):
        """Generate SCD based on user prompt, dataset summary, and service"""
        control_id = self.control_ids.get(service, "SCD-XXX")
        prompt_template = PromptTemplate(
            input_variables=["dataset_summary", "user_prompt", "service", "control_id"],
            template="""
You are a cloud security expert with access to a dataset of security controls.

Dataset summary: {dataset_summary}

Based on this dataset and the following user request, generate a detailed Security Control Definition (SCD) for the following cloud service: {service}

User request: {user_prompt}

Provide your response in the following format:

Control ID: {control_id}
Control Name: [Name of the control]
Description: [Brief description of the control]
Implementation Details: 
1. [First detailed step for implementing the control]
2. [Second step...]
...
Responsibility: [Who is responsible for implementing this control]
Frequency: [How often should this control be reviewed/implemented]
Evidence: [What evidence is required to prove this control is in place]

Ensure your response is relevant to the user's request and based on the information available in the dataset.
"""
        )

        chain = LLMChain(llm=self.model, prompt=prompt_template)
        response = chain.invoke({
            "dataset_summary": self.dataset_summary,
            "user_prompt": user_prompt,
            "service": service,
            "control_id": control_id
        })
        return response
