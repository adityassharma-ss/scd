from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.utils.config import Config
from src.model.model_trainer import ModelTrainer
import json
import random
import re
import os

class AIModel:
    def __init__(self):
        self.config = Config()
        self.model = ChatOpenAI(api_key=self.config.get_openai_api_key(), temperature=0.7)
        self.model_trainer = ModelTrainer()
        self.vector_store = self.model_trainer.get_vector_store()
        self.scd_templates = self.load_template()

    def load_template(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, 'templates', 'scdTemplate.json')
        with open(template_path, 'r') as f:
            return json.load(f)['scd_examples']

    def generate_scd(self, user_prompt, service, additional_controls):
        # Query the vector store for relevant controls
        relevant_controls = self.vector_store.similarity_search(user_prompt, k=5)
        control_descriptions = [doc.page_content for doc in relevant_controls]
        
        control_ids = [f"SCD-{i:03d}" for i in range(1, 16)]
        template_str = self.format_template(random.choice(self.scd_templates))

        prompt_template = PromptTemplate(
            input_variables=["control_descriptions", "user_prompt", "service", "control_ids", "scd_template", "additional_controls"],
            template="""
            You are a cloud security expert. Based on the following control descriptions and the user's request, generate between 10 to 15 detailed Security Control Definitions (SCDs) for different Control Names relevant to the cloud service mentioned in the user prompt.

            Control descriptions:
            {control_descriptions}

            Based on these descriptions and the following user request, generate detailed Security Control Definitions (SCDs) for the service: {service}

            User request: {user_prompt}

            Here's an example template for a well-formatted SCD:

            {scd_template}

            For each SCD, provide your response in the same format as the template above. Ensure each SCD is unique and relevant to the user's request prompt. Use the information available in the control descriptions to inform your responses. Aim for consistency in naming conventions and level of detail across all SCDs.

            In addition to the general security controls, make sure to include SCDs that specifically address the following control areas: {additional_controls}

            Control IDs to use: {control_ids}
            """
        )

        chain = prompt_template | self.model | StrOutputParser()

        response = chain.invoke({
            "control_descriptions": "\n".join(control_descriptions),
            "user_prompt": user_prompt,
            "service": service,
            "control_ids": ", ".join(control_ids),
            "scd_template": template_str,
            "additional_controls": ", ".join(additional_controls)
        })

        validated_scds = self.validate_scds(response)
        if len(validated_scds) < 10:
            response = chain.invoke({
                "control_descriptions": "\n".join(control_descriptions),
                "user_prompt": f"{user_prompt} Please ensure to generate at least 10 valid SCDs.",
                "service": service,
                "control_ids": ", ".join(control_ids),
                "scd_template": template_str,
                "additional_controls": ", ".join(additional_controls)
            })
            validated_scds = self.validate_scds(response)

        return "\n\n".join(validated_scds)

    # The rest of the methods (format_template, validate_scds) remain the same
