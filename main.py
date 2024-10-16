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
        """Generate Security Control Definitions(SCDs) based on user prompt, datasets, datasets information and cloud service"""
        control_ids = self.control_ids.get(service, [f"SCD-{i:03d}" for i in range(1, 16)])
        
        prompt_template = PromptTemplate(
            input_variables=["dataset_summary", "user_prompt", "service", "control_ids"],
            template="""
            You are a cloud security expert with access to a dataset of security controls definitions & best practices. Based on this dataset, generate between 8 to 15 detailed Security Control Definitions (SCDs) for different Control Names relevant to the cloud service mentioned in the user prompt.

            Dataset summary: {dataset_summary}

            Based on this dataset and the following user request, generate detailed Security Control Definitions (SCDs) for the service: {service}

            User request: {user_prompt}

            For each SCD, provide your response in the following format:
            Control ID: [Use the provided Control ID]
            Control Name: [Provide a clear, concise name for the control]
            Description: [Provide a brief, accurate description of the Control Name]
            Implementation Details: [Provide detailed, actionable steps for implementing the control]
            Responsibility: [Specify who is responsible: "Customer", "Cloud Provider", or "Shared"]
            Review Frequency: [Specify one of: Continuous / Annual Review / Quarterly Review / Monthly Review / As-Needed]
            Evidence Source: [Specify what evidence is required to prove this control is in place]

            Ensure each SCD is unique and relevant to the user's request prompt. Use the information available in the datasets to inform your responses. Aim for consistency in naming conventions and level of detail across all SCDs.

            Control IDs to use: {control_ids}
            """
        )

        chain = prompt_template | self.model | StrOutputParser()
        
        response = chain.invoke({
            "dataset_summary": self.dataset_summary,
            "user_prompt": user_prompt,
            "service": service,
            "control_ids": ", ".join(control_ids)
        })

        return response
