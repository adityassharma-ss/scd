from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from src.utils.config import Config

class AIModel:
    def __init__(self):
        self.model = OpenAI(api_key=Config().get_openai_api_key(), temperature=0.7)
        self.dataset_summary = ""
        self.control_ids = {}

    def set_dataset_info(self, summary, control_ids):
        """Set the dataset summary and control IDs for the model to use."""
        self.dataset_summary = summary
        self.control_ids = control_ids

    def generate_scds(self, user_prompt, service):
        """Generate multiple SCDs based on user prompt, dataset, and service."""
        control_ids = self.control_ids.get(service, [])
        
        # Check if we have relevant control IDs for the given service
        if not control_ids:
            return f"No control IDs found for service: {service}"

        # Prepare prompt template
        prompt_template = PromptTemplate(
            input_variables=["dataset_summary", "user_prompt", "service", "control_id"],
            template="""
            You are a cloud security expert with access to a dataset of security controls. You are trained upon the dataset to setup & implement security controls.

            Dataset summary: {dataset_summary}

            Based on this dataset and the following user request, generate a detailed Security Control Definition (SCD) for the service: {service}.

            User request: {user_prompt}

            Provide your response in the following format:

            Control ID: {control_id}
            Control Name: [Name of the control]
            Implementation Details: [Detailed steps for implementing the control]
            Responsibility: [Who is responsible for implementing this control]
            Frequency: [How often should this control be reviewed/implemented]
            Evidence: [What evidence is required to prove this control is in place]
            Description: [Brief description of the control]

            Ensure your response is relevant to the user's request prompt and based on the information available in the datasets.
            """
        )

        # Create an LLM chain
        chain = LLMChain(llm=self.model, prompt=prompt_template)

        # Iterate through all control IDs and generate corresponding SCDs
        scd_responses = []
        for control_id in control_ids:
            response = chain.run({
                "dataset_summary": self.dataset_summary,
                "user_prompt": user_prompt,
                "service": service,
                "control_id": control_id
            })
            scd_responses.append(response)

        # Return the list of SCDs generated for the given service
        return scd_responses
