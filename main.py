from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from src.utils.config import Config

class AIModel:
    def __init__(self):
        self.model = ChatOpenAI(api_key=Config().get_openai_api_key(), temperature=0.7)
        self.dataset_summary = ""

    def set_dataset_summary(self, summary):
        """Set the dataset summary for the model to use"""
        self.dataset_summary = summary

    def generate_scd(self, user_prompt):
        """Generate SCD based on user prompt and dataset summary"""
        prompt_template = PromptTemplate(
            input_variables=["dataset_summary", "user_prompt"],
            template="""
            You are a cloud security expert with access to a dataset of security controls.

            Dataset summary: {dataset_summary}

            Based on this dataset and the following user request, generate a detailed Security Control Definition (SCD):

            User request: {user_prompt}

            Provide your response in the following format:
            1. Control ID: [Provide a suitable ID]
            2. Control Name: [Name of the control]
            3. Description: [Brief description of the control]
            4. Implementation Details: [Detailed steps for implementing the control]
            5. Responsibility: [Who is responsible for implementing this control]
            6. Frequency: [How often should this control be reviewed/implemented]
            7. Evidence: [What evidence is required to prove this control is in place]

            Ensure your response is relevant to the user's request and based on the information available in the dataset.
            """
        )

        chain = LLMChain(llm=self.model, prompt=prompt_template)
        response = chain.run(dataset_summary=self.dataset_summary, user_prompt=user_prompt)

        return response
