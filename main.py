class AIModel:
    # ... existing methods ...

    def generate_scd(self, user_prompt, service):
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
            """
        )

        # Create an LLM chain
        chain = LLMChain(llm=self.model, prompt=prompt_template)

        # Iterate through all control IDs and generate corresponding SCDs
        scd_responses = []
        for control_id in control_ids:
            response = chain.invoke({
                "dataset_summary": self.dataset_summary,
                "user_prompt": user_prompt,
                "service": service,
                "control_id": control_id
            })
            # Assuming response is a string formatted as expected
            scd_data = self._parse_scd_response(response)
            if scd_data:
                scd_responses.append(scd_data)

        return scd_responses

    def _parse_scd_response(self, response):
        """Parse the SCD response into a structured dictionary."""
        lines = response.split("\n")
        scd_data = {}
        
        for line in lines:
            if ": " in line:
                key, value = line.split(": ", 1)
                scd_data[key.strip()] = value.strip()
        
        return scd_data
