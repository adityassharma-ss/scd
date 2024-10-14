from langchain.openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from src.utils.config import Config

class AIModel:
    def __init__(self):
        self.model = ChatOpenAI(api_key=Config().get_openai_api_key(), temperature=0.8)
        self.dataset_summary = ""
        self.control_ids = {}

    def set_dataset_info(self, summary, control_ids):
        """Set the dataset summary and control IDs for the model to use."""
        self.dataset_summary = summary
        self.control_ids = control_ids

    def generate_scd(self, user_prompt, service):
        """Generate Security Control Definitions (SCDs) based on user prompt and datasets."""
        control_ids = self.control_ids.get(service, ["SCD-XOOX"] * 12)  # Ensures we have 12 SCDs

        prompt_template = PromptTemplate(
            input_variables=["dataset_summary", "user_prompt", "service", "control_ids"],
            template="""
You are a cloud security expert with access to a dataset of security controls definitions & best practices. Based on this dataset, generate multiple detailed Security Control Definitions (SCDs) for the service: {service}

Dataset summary: {dataset_summary}

User request: {user_prompt}

Control IDs: {control_ids}

Please provide the SCDs in the following format:
- Control ID: {control_id}
- Control Name: [Name of the control]
- Description: [Brief description of the Control Name]
- Implementation Details: [Detailed steps for implementing the control]
- Responsibility: [Who is responsible for implementing this control? Either Customer or shared between CloudProvider & Customer]
- Frequency: [How often should this control be reviewed? Continuous / Annual / Quarterly / Monthly]
- Evidence: [What evidence is required to prove this control is in place]
"""
        )

        chain = LLMChain(llm=self.model, prompt=prompt_template, output_parser=StrOutputParser())
        
        # Generate the SCDs for each control ID
        responses = []
        for control_id in control_ids:
            response = chain.invoke({
                "dataset_summary": self.dataset_summary,
                "user_prompt": user_prompt,
                "service": service,
                "control_id": control_id
            })
            responses.append(response)
        
        return "\n\n---\n\n".join(responses)  # Join responses for final output
