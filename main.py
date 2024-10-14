import pandas as pd
import re
from src.model.ai_model import AIModel
from src.data.io_handler import IOHandler

class SCDGenerator:
    def __init__(self):
        self.ai_model = AIModel()
        self.dataset = None
        self.generated_scds = []  # To keep track of all generated SCDs

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

        # Extract service from user prompt (this is a simple approach and might need refinement)
        service = next((s for s in self.dataset['Cloud Service'].unique() if s.lower() in user_prompt.lower()), "Unknown")

        scd = self.ai_model.generate_scd(user_prompt, service)
        
        # Check for duplicates before adding the new SCD
        if scd not in self.generated_scds:
            self.generated_scds.append(scd)  # Keep track of generated SCDs

        return scd

    def save_scd(self, output_file_path, format='md'):
        """Save the generated SCDs to a file"""

        if format == 'md':
            with open(output_file_path, 'w') as f:
                # Save all SCDs into the Markdown file, joined by "---" as a separator
                combined_scds = "\n\n---\n\n".join(self.generated_scds)
                f.write(combined_scds)

        elif format == 'csv':
            # Convert the SCDs into CSV format
            csv_data = []
            for scd in self.generated_scds:
                scd_entries = scd.split('\n\n---\n\n')
                for scd_entry in scd_entries:
                    entry_data = {}
                    for line in scd_entry.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            entry_data[key.strip()] = value.strip()
                        else:
                            # Check if line starts with numbering (e.g., "1.", "2.", etc.)
                            if re.match(r'^\d+\.', line.strip()):
                                if 'Implementation Details' not in entry_data:
                                    entry_data['Implementation Details'] = line.strip()
                                else:
                                    entry_data['Implementation Details'] += ' ' + line.strip()

                    csv_data.append(entry_data)

            # Save all the CSV data at once
            df = pd.DataFrame(csv_data)
            df.to_csv(output_file_path, index=False)

            print(f"SCD saved to {output_file_path}")
