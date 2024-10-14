import pandas as pd
import re

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
                f.write(f"Implementation Details: \n")
                for detail in control['implementation_details']:
                    f.write(f"- {detail}\n")
                f.write(f"\n\n")
        print(f"SCD Report saved to {output_file_path}")

    @staticmethod
    def save_to_csv(data, file_path):
        """Save data to a CSV file, ensuring that implementation details are split into rows."""
        rows = []
        for row in data:
            # Use regex to split on number patterns (e.g., "1.", "2.", "3.")
            implementation_details = re.split(r'(?<=\d)\.\s*', row['Implementation Details'])  # Split by digits followed by a period
            for detail in implementation_details:
                new_row = row.copy()
                new_row['Implementation Details'] = detail.strip()
                rows.append(new_row)

        df = pd.DataFrame(rows)
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")

    @staticmethod
    def save_to_md(data, file_path):
        """Save data to a Markdown file, ensuring that implementation details are split."""
        with open(file_path, 'w') as md_file:
            for row in data:
                md_file.write(f"## {row['Control ID']} {row['Cloud Service']}\n")
                md_file.write(f"**Category**: {row['Category']}\n")
                md_file.write(f"**Control Description**: {row['Control Description']}\n")
                implementation_details = re.split(r'(?<=\d)\.\s*', row['Implementation Details'])
                md_file.write("### Implementation Details: \n")
                for detail in implementation_details:
                    md_file.write(f"- {detail.strip()}\n")
                md_file.write("\n---\n")
        print(f"Data saved to {file_path}")
