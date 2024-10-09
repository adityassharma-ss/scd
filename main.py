
import pandas as pd

class SCDGenerator:
    def process_scd(self, input_file_path, output_file_path, control_request):
        # Load the dataset
        df = pd.read_csv(input_file_path)

        # Initialize the output data list
        output_data = []

        # Debugging: Print the incoming prompt and dataset
        print(f"User Prompt: {control_request}")
        print("Dataset Preview:")
        print(df.head())  # Print the first few rows of the dataset for inspection

        # Analyzing user prompt and filtering dataset accordingly
        for index, row in df.iterrows():
            # Check if the prompt is in the Control Name or Description
            control_name = row.get('Control Name', '').lower()
            description = row.get('Description', '').lower()
            prompt_lower = control_request.lower()

            if prompt_lower in control_name or prompt_lower in description:
                control_id = f"CTRL-{index + 1:03}"
                output_data.append([
                    control_id,
                    row.get('Control Name', f"Control for {index + 1}"),
                    row.get('Description', f"Description for control {index + 1}"),
                    row.get('Implementation Details', "Implement according to best practices."),
                    row.get('Responsibility', "Customer"),
                    row.get('Frequency', "Continuous"),
                    "Evidence required."
                ])
                # Debugging: Print the matched control information
                print(f"Matched Control: {control_id}, {row.get('Control Name')}")

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

        # Debugging: Check the output DataFrame
        print("Output DataFrame:")
        print(output_df)

        return output_df  # Return the DataFrame if needed for further processing
