import pandas as pd
import re
from src.data.io_handler import IOHandler

class SCDGenerator:

    def __init__(self):
        self.ai_model = AIModel()
        self.dataset = None

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
        for _, row in self.dataset.iterrows():
            service = row['Cloud Service']
            control_id = row.get('Control ID', f"SCD-{len(control_ids) + 1:03d}")
            if service not in control_ids:
                control_ids[service] = control_id
        self.ai_model.set_dataset_info(summary, control_ids)

    def generate_scd(self, user_prompt):
        """Generate SCD based on user prompt"""
        if self.dataset is None:
            return "Error: Dataset not loaded. Please load a dataset first."
        
        service = next((s for s in self.dataset['Cloud Service'].unique() if s.lower() in user_prompt.lower()), None)
        return self.ai_model.generate_scd(user_prompt, service)

    def save_scd(self, scd, output_file_path, format='md'):
        """Save SCD to the selected file format"""
        if format == 'md':
            with open(output_file_path, 'a') as f:
                f.write(scd)
        elif format == 'csv':
            scd_entries = scd.strip().split('\n\n')
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
            
            IOHandler.save_to_csv(csv_data, output_file_path)
        elif format == 'xlsx':
            scd_entries = scd.strip().split('\n\n')
            xlsx_data = []
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
                xlsx_data.append(entry_data)
            
            IOHandler.save_to_xlsx(xlsx_data, output_file_path)
        
        print(f"SCD saved to {output_file_path}")
