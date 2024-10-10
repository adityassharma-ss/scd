import pandas as pd
from src.model.ai_model import AIModel

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
            if self._matches_prompt(row, control_request):
                # Prepare the SCD definition based on the row and user prompt
                scd_entry = {
                    'Control ID': row['Control ID'],
                    'Control Description': row['Control Description'],
                    'Guidance': row['Guidance'],
                    'Cloud Service': row['Cloud Service'],
                    'User Prompt Match': control_request  # Include prompt to track matched result
                }
                output_data.append(scd_entry)

        # Save the output to both Markdown and CSV
        self._save_output(output_data, output_file_path)

    def _matches_prompt(self, row, control_request):
        # Logic to determine if a row matches the control request (user prompt)
        control_description = row['Control Description'].lower()
        return control_request.lower() in control_description

    def _save_output(self, output_data, output_file_path):
        # Save as .md file
        md_output = f"{output_file_path}.md"
        with open(md_output, 'w') as md_file:
            for item in output_data:
                md_file.write(f"### Control ID: {item['Control ID']}\n")
                md_file.write(f"- Control Description: {item['Control Description']}\n")
                md_file.write(f"- Guidance: {item['Guidance']}\n")
                md_file.write(f"- Cloud Service: {item['Cloud Service']}\n\n")
        
        # Save as .csv file
        csv_output = f"{output_file_path}.csv"
        pd.DataFrame(output_data).to_csv(csv_output, index=False)
