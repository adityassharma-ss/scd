from src.data.io_handler import IOHandler
from src.model.ai_model import AIModel
import pandas as pd
import re

class SCDGenerator:
    def __init__(self):
        self.ai_model = AIModel()
        self.additional_controls = ["Tagging", "Naming Conventions", "Authentication", "Traffic Management"]

    def generate_scd(self, user_prompt):
        """Generate SCD based on user prompt"""
        service = "Unknown"  # You may want to implement a method to detect the service from the prompt
        return self.ai_model.generate_scd(user_prompt, service, self.additional_controls)

    def save_scd(self, scd, output_file_path, format='md'):
        scd_entries = re.split(r'\n\s*\n', scd.strip())
        
        if format == 'md':
            with open(output_file_path, 'w') as f:
                f.write(scd)
        elif format in ['csv', 'xlsx']:
            csv_data = []
            for scd_entry in scd_entries:
                entry_data = {}
                implementation_details = []
                for line in scd_entry.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if key == 'Implementation Details':
                            implementation_details.append(value)
                        else:
                            entry_data[key] = value
                    else:
                        if '-' in line:
                            implementation_details.append(line.strip())
                entry_data['Implementation Details'] = '|'.join(implementation_details)
                csv_data.append(entry_data)
            
            df = pd.DataFrame(csv_data)
            if format == 'csv':
                df.to_csv(output_file_path, index=False)
            else:  # xlsx
                df.to_excel(output_file_path, index=False)
        
        print(f"SCD saved to {output_file_path}")
