import pandas as pd

class IOHandler:
    @staticmethod
    def load_csv(file_paths):
        """Loads cloud control data from multiple dataset files."""
        dataframes = []
        for file_path in file_paths:
            try:
                df = pd.read_csv(file_path)
                dataframes.append(df)
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {file_path}")

        # Combine all datasets into one
        if dataframes:
            return pd.concat(dataframes, ignore_index=True)
        return None

    @staticmethod
    def save_output(output_data, output_file_path):
        """Saves the generated SCD to an output file."""
        with open(output_file_path, 'w') as f:
            for control in output_data:
                f.write(f"## Cloud Service: {control['cloud_service']}\n")
                f.write(f"### Control ID: {control['control_id']}\n")
                f.write(f"### Control Description: {control['control_description']}\n")
                f.write(f"Implementation Details:\n")
                for detail in control['implementation_details']:
                    f.write(f"- {detail}\n")
                f.write(f"\n\n")
        print(f"SCD Report saved to {output_file_path}")
