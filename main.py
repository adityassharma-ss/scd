import pandas as pd

class IOHandler:
    @staticmethod
    def load_csv(file_path):
        """Loads cloud control data from a CSV file."""
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")

    @staticmethod
    def save_output(output_data, output_file_path):
        """Saves the generated SCD to an output Markdown file."""
        with open(output_file_path, 'w') as f:
            for control in output_data:
                f.write(f"## Cloud Service: {control['cloud_service']}\n")
                f.write(f"### Control ID: {control['control_id']}\n")
                f.write(f"### Control Description: {control['control_description']}\n")
                f.write(f"{control['scd_output']}\n\n")
        print(f"SCD Report saved to {output_file_path}")
