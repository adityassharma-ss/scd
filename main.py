import pandas as pd
from src.model.ai_model import AIModel

class SCDGenerator:
    def __init__(self):
        self.ai_model = AIModel()

    def process_scd(self, input_file_path, output_file_path, control_request, output_format='csv'):
        """Process and generate security control definitions."""
        # Load the dataset
        df = pd.read_csv(input_file_path)

        # Initialize the output data list
        output_data = []

        # Debugging: Print the incoming prompt and dataset
        print(f"User Prompt: {control_request}")
        print("Dataset Preview:")
        print(df.head())  # Print the first few rows of the dataset for inspection

        # Check for expected columns in the dataset
        expected_columns = ['Control ID', 'Control Description', 'Guidance', 'Cloud Service']
        for col in expected_columns:
            if col not in df.columns:
                print(f"Warning: Missing expected column '{col}' in the dataset.")
                return None

        # Analyzing user prompt and filtering dataset accordingly
        for index, row in df.iterrows():
            control_description = row.get('Control Description', '').lower()
            cloud_service = row.get('Cloud Service', '').lower()
            guidance = row.get('Guidance', '').lower()
            prompt_lower = control_request.lower()

            if prompt_lower in control_description or prompt_lower in cloud_service or prompt_lower in guidance:
                control_id = row.get("Control ID", f"CTRL-{index + 1:03d}")

                # Generate the detailed security control definition using AI model
                ai_response = self.ai_model.generate_scd(
                    cloud=row.get('Cloud Service', 'Unknown'),
                    service=row.get('Config Rule', 'Unknown'),  # Assuming Config Rule relates to service
                    control_name=row.get('Control Description', 'Unknown'),
                    description=row.get('Guidance', 'Unknown'),
                    user_prompt=control_request
                )

                # Append to output data
                output_data.append([
                    control_id,
                    row.get('Control Description', f"Control for {index + 1}"),
                    row.get('Guidance', f"Description for control {index + 1}"),
                    ai_response if ai_response else "No response generated",
                    "Customer",  # Assuming responsibility is static, modify as needed
                    "Continuous",  # Assuming frequency is static, modify as needed
                    "Evidence required."
                ])

        if not output_data:
            print("No controls matched the user prompt.")
            return None

        # Save output to CSV or Markdown based on user preference
        if output_format == 'csv':
            self.save_to_csv(output_data, output_file_path)
        elif output_format == 'md':
            self.save_to_markdown(output_data, output_file_path)

    def save_to_csv(self, output_data, output_file_path):
        """Save the generated SCD to a CSV file."""
        output_df = pd.DataFrame(output_data, columns=[
            'Control ID', 'Control Name', 'Description', 'Implementation Details',
            'Responsibility', 'Frequency', 'Evidence'
        ])
        output_df.to_csv(output_file_path, index=False)
        print(f"Output successfully written to {output_file_path}")

    def save_to_markdown(self, output_data, output_file_path):
        """Save the generated SCD to a Markdown file."""
        with open(output_file_path, 'w') as f:
            for control in output_data:
                f.write(f"## Cloud Service: {control[1]}\n")
                f.write(f"### Control ID: {control[0]}\n")
                f.write(f"### Control Description: {control[2]}\n")
                f.write(f"{control[3]}\n\n")
        print(f"SCD Report saved to {output_file_path}")
