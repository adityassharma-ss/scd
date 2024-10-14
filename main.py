prompt_template = PromptTemplate(
    input_variables=["dataset_summary", "user_prompt", "service", "control_id"],
    template="""
    You are a cloud security expert with access to a dataset of security controls. Based on this dataset, generate 10-12 detailed Security Control Definitions (SCDs) relevant to the following cloud service: {service}. 

    Please ensure that the control names reflect common security practices and that the descriptions and implementation details are comprehensive.

    Dataset summary: {dataset_summary}

    User request: {user_prompt}

    Provide your response in the following format:
    Control ID: {control_id}
    Control Name: [Name of the control]
    Description: [Brief description of the control]
    Implementation Details: [Detailed steps for implementing the control]
    Responsibility: [Who is responsible for implementing this control]
    Frequency: [How often should this control be reviewed/implemented]
    Evidence: [What evidence is required to prove this control is in place]

    Ensure your response is relevant to the user's request prompt and based on the information available in the datasets.
    """
)
