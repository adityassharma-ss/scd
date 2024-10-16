def generate_scd(self, user_prompt, service, additional_controls):
        """Generate Security Control Definitions(SCDs) based on user prompt, datasets, datasets information and cloud service"""
        control_ids = self.control_ids.get(service, [f"SCD-{i:03d}" for i in range(1, 16)])
        
        # Randomly select one example
        few_shot_example = random.choice(self.few_shot_examples)
        few_shot_example_str = self.format_example(few_shot_example)

        prompt_template = PromptTemplate(
            input_variables=["dataset_summary", "user_prompt", "service", "control_ids", "few_shot_example", "additional_controls"],
            template="""
            You are a cloud security expert with access to a dataset of security controls definitions & best practices. Based on this dataset, generate between 8 to 15 detailed Security Control Definitions (SCDs) for different Control Names relevant to the cloud service mentioned in the user prompt.

            Dataset summary: {dataset_summary}

            Based on this dataset and the following user request, generate detailed Security Control Definitions (SCDs) for the service: {service}

            User request: {user_prompt}

            Here's an example of a well-formatted SCD:

            {few_shot_example}

            For each SCD, provide your response in the same format as the example above. Ensure each SCD is unique and relevant to the user's request prompt. Use the information available in the datasets to inform your responses. Aim for consistency in naming conventions and level of detail across all SCDs.

            In addition to the general security controls, make sure to include SCDs that specifically address the following control areas: {additional_controls}

            Control IDs to use: {control_ids}
            """
        )

        chain = prompt_template | self.model | StrOutputParser()
        
        response = chain.invoke({
            "dataset_summary": self.dataset_summary,
            "user_prompt": user_prompt,
            "service": service,
            "control_ids": ", ".join(control_ids),
            "few_shot_example": few_shot_example_str,
            "additional_controls": ", ".join(additional_controls)
        })

        # Validate and potentially regenerate
        validated_scds = self.validate_scds(response)
        if len(validated_scds) < 8:
            # If we don't have enough valid SCDs, try regenerating
            response = chain.invoke({
                "dataset_summary": self.dataset_summary,
                "user_prompt": f"{user_prompt} Please ensure to generate at least 8 valid SCDs.",
                "service": service,
                "control_ids": ", ".join(control_ids),
                "few_shot_example": few_shot_example_str,
                "additional_controls": ", ".join(additional_controls)
            })
            validated_scds = self.validate_scds(response)

        return "\n\n".join(validated_scds)

    def format_example(self, example):
        formatted = f"Control ID: {example['Control ID']}\n"
        formatted += f"Control Name: {example['Control Name']}\n"
        formatted += f"Description: {example['Description']}\n"
        formatted += "Implementation Details:\n"
        for detail in example['Implementation Details']:
            formatted += f"- {detail}\n"
        formatted += f"Responsibility: {example['Responsibility']}\n"
        formatted += f"Review Frequency: {example['Review Frequency']}\n"
        formatted += f"Evidence Source: {example['Evidence Source']}"
        return formatted

    def validate_scds(self, response):
        scd_pattern = re.compile(r'Control ID:.*?(?=Control ID:|$)', re.DOTALL)
        scds = scd_pattern.findall(response)
        
        validated_scds = []
        for scd in scds:
            if all(field in scd for field in ['Control ID:', 'Control Name:', 'Description:', 'Implementation Details:', 'Responsibility:', 'Review Frequency:', 'Evidence Source:']):
                validated_scds.append(scd.strip())
        
        return validated_scds
