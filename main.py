import pandas as pd
from ai_model import AIModel

class SCDGenerator:
    def __init__(self):
        self.ai_model = AIModel()

    def process_scd(self, input_file_path, output_file_path, control_request):
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
            # Check if the prompt is in the Control Description or Guidance
            control_description = row.get('Control Description', '').lower()
            guidance = row.get('Guidance', '').lower()
            prompt_lower = control_request.lower()

            if prompt_lower in control_description or prompt_lower in guidance:
                control_id = row.get('Control ID', f"CTRL-{index + 1:03d}")

                # Generate the detailed security control definition using AI model
                ai_response = self.ai_model.generate_scd(
                    cloud=row.get('Cloud Service', 'Unknown'),
                    service=row.get('Config Rule', 'Unknown'),  # Assuming Config Rule relates to service
                    control_name=row.get('Control Description', 'Unknown'),
                    description=row.get('Guidance', 'Unknown')
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

                # Debugging: Print the matched control information
                print(f"Matched Control: {control_id}, {row.get('Control Description')}")

        # Check if any data was added to output_data
        if not output_data:
            print("No controls matched the user prompt.")
            return None

        # Create a DataFrame from the output data
        output_df = pd.DataFrame(output_data, columns=[
            'Control ID',
            'Control Name',
            'Description',
            'Implementation Details',
            'Responsibility',
            'Frequency',
            'Evidence'
        ])

        # Write the output DataFrame to a CSV file
        output_df.to_csv(output_file_path, index=False)

        print(f"Output successfully written to {output_file_path}")
        return output_df
