
from src.data.io_handler import IOHandler
from src.model.ai_model import AIModel
import pandas as pd
import re

class SCDGenerator:
    def __init__(self):
        self.ai_model = AIModel()
        self.dataset = None
        self.additional_controls = ["Tagging", "Naming Conventions", "Authentication", "Traffic Management"]

    def load_datasets(self, file_paths):
        """Load and process the dataset"""
        self.dataset = IOHandler.load_csv(file_paths)
        self._summarize_dataset()

    def _summarize_dataset(self):
        """Create a summary of the dataset for the model"""
        services = self.dataset['Cloud Service'].unique()
        controls = self.dataset['Control Description'].unique()
        summary = f"Dataset contains information on {len(services)} cloud services and {len(controls)} controls."

        control_ids = {}
        for service in services:
            service_controls = self.dataset[self.dataset['Cloud Service'] == service]
            control_ids[service] = service_controls['Control ID'].tolist()

        self.ai_model.set_dataset_info(summary, control_ids)

    def generate_scd(self, user_prompt):
        """Generate SCD based on user prompt"""
        if self.dataset is None:
            return "Error: Dataset not loaded. Please load a dataset first."

        service = next((s for s in self.dataset['Cloud Service'].unique() if s.lower() in user_prompt.lower()), "Unknown")
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
                    if ': ' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if key == 'Implementation Details':
                            implementation_details.append(value)
                        else:
                            entry_data[key] = value
                
                if implementation_details:
                    entry_data['Implementation Details'] = ' | '.join(implementation_details)
                else:
                    entry_data['Implementation Details'] = ''
                
                csv_data.append(entry_data)
            
            df = pd.DataFrame(csv_data)
            if format == 'csv':
                df.to_csv(output_file_path, index=False)
            else:  # xlsx
                df.to_excel(output_file_path, index=False)
        
        print(f"SCD saved to {output_file_path}")
