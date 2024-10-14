class AIModel:
    def __init__(self, model, dataset_summary, control_ids):
        self.model = model
        self.dataset_summary = dataset_summary
        self.control_ids = control_ids

    def generate_scd(self, user_prompt, service):
        """Generate multiple SCDs based on user prompt, dataset, and service."""
        control_ids = self.control_ids.get(service, [])
        
        if not control_ids:
            return f"No control IDs found for service: {service}"

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

        chain = LLMChain(llm=self.model, prompt=prompt_template)

        scd_responses = []
        for control_id in control_ids:
            response = chain.invoke({
                "dataset_summary": self.dataset_summary,
                "user_prompt": user_prompt,
                "service": service,
                "control_id": control_id
            })

            if response:
                scd_data = self._parse_scd_response(response)
                if scd_data:
                    scd_responses.append(scd_data)
            else:
                print(f"Warning: No response received for control ID: {control_id}")

        return scd_responses

    def _parse_scd_response(self, response):
        """Parse the SCD response into a structured dictionary."""
        if not response:
            print("Error: Received empty response for SCD parsing.")
            return None

        lines = response.strip().split("\n")  # Trim whitespace and split lines
        scd_data = {}

        for line in lines:
            if ": " in line:
                key, value = line.split(": ", 1)
                scd_data[key.strip()] = value.strip()
        
        return scd_data

    def update_files(self, scd_responses):
        """Update Markdown and CSV files with SCD data."""
        markdown_content = "# Security Control Definitions\n\n"
        csv_rows = []

        for scd in scd_responses:
            # Prepare Markdown content
            markdown_content += f"## Control ID: {scd.get('Control ID')}\n"
            for key, value in scd.items():
                markdown_content += f"- **{key}**: {value}\n"
            markdown_content += "\n"

            # Prepare CSV row
            csv_row = [scd.get('Control ID'), scd.get('Control Name'), scd.get('Implementation Details'),
                        scd.get('Responsibility'), scd.get('Frequency'), scd.get('Evidence'), 
                        scd.get('Description')]
            csv_rows.append(csv_row)

        # Write to Markdown file
        with open("scd_definitions.md", "w") as md_file:
            md_file.write(markdown_content)

        # Write to CSV file
        with open("scd_definitions.csv", "w", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Control ID', 'Control Name', 'Implementation Details',
                             'Responsibility', 'Frequency', 'Evidence', 'Description'])
            writer.writerows(csv_rows)
