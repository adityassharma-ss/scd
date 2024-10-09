import pandas as pd

class SCDGenerator:
    def process_scd(self, input_file_path, output_file_path, control_request):
        # Load the dataset
        df = pd.read_csv(input_file_path)

        # Initialize the output data list
        output_data = []

        # Analyzing user prompt and filtering dataset accordingly
        for index, row in df.iterrows():
            # Analyze the prompt for keywords (you can refine this based on your requirements)
            if control_request.lower() in row.get('Control Name', '').lower() or \
               control_request.lower() in row.get('Description', '').lower():
                
                control_name = row.get('Control Name', f"Control for {index + 1}")
                description = row.get('Description', f"Description for control {index + 1}")
                implementation_details = row.get('Implementation Details', "Implement according to best practices.")
                responsibility = row.get('Responsibility', "Customer")
                frequency = row.get('Frequency', "Continuous")

                # Generate Control ID based on the index or specific logic
                control_id = f"CTRL-{index + 1:03}"

                # Add the generated control details to the output data
                output_data.append([
                    control_id,
                    control_name,
                    description,
                    implementation_details,
                    responsibility,
                    frequency,
                    "Evidence required."  # This could also be dynamic if needed
                ])

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

        return output_df  # Return the DataFrame if needed for further processing
