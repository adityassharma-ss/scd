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
        self.model = ChatOpenAI(api_key=self.config.get_openai_api_key(), temperature=0.8)
        self.model_trainer = ModelTrainer()
        try:
            self.vector_store = self.model_trainer.get_vector_store()
        except Exception as e:
            print(f"Error Loading Vector Store: {str(e)}")
            self.vector_store = None
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

Control descriptions: {control_descriptions}

Based on these descriptions and the following user request, generate detailed Security Control Definitions (SCDs) for the service: {service}

User request: {user_prompt}

Provide your response in the following format:

Control ID: {{control_id}}
Control Name: [Name of the control]
Description: [Brief description of the Control Name]
Implementation Details: [Detailed steps for implementing the control]
Responsibility: [Who is responsible for implementing this control? Either, Is it Customer or is it shared between CloudProvider & Customer]
Frequency: [How often should this control be reviewed/implemented? Choose between Continuous / Annual Review / Quarterly Review / Monthly Review]
Evidence: [What evidence is required to prove this control is in place]

Here's an example template for a well-formatted SCD:

{scd_template}

For each SCD, provide your response in the same format as the template above. Ensure each SCD is unique and relevant to the user's request. Use the information available in the control descriptions to inform your responses. Aim for consistency in naming conventions and level of detail across SCDs.

In addition to the general security controls, make sure to include SCDs that specifically address the following control areas:

{additional_controls}

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

    def format_template(self, template):
        formatted = f"Control ID: {template['Control ID']}\n"
        formatted += f"Control Name: {template['Control Name']}\n"
        formatted += f"Description: {template['Description']}\n"
        formatted += "Implementation Details:\n"
        for detail in template['Implementation Details']:
            formatted += f"- {detail}\n"
        formatted += f"Responsibility: {template['Responsibility']}\n"
        formatted += f"Review Frequency: {template['Review Frequency']}\n"
        formatted += f"Evidence Source: {template['Evidence Source']}"
        return formatted

    def validate_scds(self, response):
        scd_pattern = re.compile(r'Control ID:.*?(?=Control ID:|$)', re.DOTALL)
        scds = scd_pattern.findall(response)
        validated_scds = []
        for scd in scds:
            if all(field in scd for field in ['Control ID:', 'Control Name:', 'Description:', 'Implementation Details:', 'Responsibility:', 'Frequency:', 'Evidence:']):
                validated_scds.append(scd.strip())
        return validated_scds
