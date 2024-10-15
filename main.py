import pandas as pd
import re
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font

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
        with open(output_file_path, 'a') as f:
            for control in output_data:
                f.write(f"## Cloud Service: {control['cloud_service']}\n")
                f.write(f"### Control ID: {control['control_id']}\n")
                f.write(f"### Control Description: {control['control_description']}\n")
                f.write("Implementation Details: \n")
                for detail in control['implementation_details']:
                    f.write(f"- {detail}\n")
                f.write(f"\n\n")
        print(f"SCD Report saved to {output_file_path}")

    @staticmethod
    def save_to_csv(data, file_path):
        """Save data to a CSV file, ensuring that implementation details are split into rows."""
        rows = []
        for row in data:
            implementation_details = re.split(r'(?<=\d)\.\s*', row['Implementation Details'])
            for detail in implementation_details:
                new_row = row.copy()
                new_row['Implementation Details'] = detail.strip()
                rows.append(new_row)
        
        df = pd.DataFrame(rows)
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")

    @staticmethod
    def save_to_xlsx(data, file_path):
        """Save data to an Excel file with bold headers."""
        rows = []
        for row in data:
            implementation_details = re.split(r'(?<=\d)\.\s*', row['Implementation Details'])
            for detail in implementation_details:
                new_row = row.copy()
                new_row['Implementation Details'] = detail.strip()
                rows.append(new_row)

        df = pd.DataFrame(rows)

        # Create a workbook and worksheet
        wb = Workbook()
        ws = wb.active

        # Append DataFrame to worksheet and bold the headers
        for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
            ws.append(row)
            if r_idx == 1:
                # Apply bold font to header row
                for cell in ws[r_idx]:
                    cell.font = Font(bold=True)

        # Save the Excel file
        wb.save(file_path)
        print(f"Data saved to {file_path}")
