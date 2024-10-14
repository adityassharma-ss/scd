import pandas as pd
import re
from src.model.ai_model import AIModel
from src.data.io_handler import IOHandler

class SCDGenerator:
    """Load and process the dataset"""

    def __init__(self):
        self.ai_model = AIModel()
        self.dataset = None

    def load_datasets(self, file_paths):
        """Load datasets from provided file paths."""
        self.dataset = IOHandler.load_csv(file_paths)
        self.summarize_dataset()

    def summarize_dataset(self):
        """Create a summary of the dataset for the model."""
        services = self.dataset['Cloud Service'].unique()
        controls = self.dataset['Control Description'].unique()
        summary = f"Dataset contains information on {len(services)} cloud services and {len(controls)} controls."
        control_ids = {}

        for idx, row in self.dataset.iterrows():
            service = row['Cloud Service']
            control_id = row.get('Control ID', f"SCD-{len(control_ids) + 1:03d}")
            if service not in control_ids:
                control_ids[service] = [control_id]  # List to hold multiple IDs
            else:
                control_ids[service].append(control_id)

        self.ai_model.set_dataset_info(summary, control_ids)

    def generate_scd(self, user_prompt):
        """Generate SCD based on user prompt."""
        if self.dataset is None:
            return "Error: Dataset not loaded. Please load a dataset first."

        service = next((s for s in self.dataset['Cloud Service'].unique() if s.lower() in user_prompt.lower()), "Unknown")
        return self.ai_model.generate_scd(user_prompt, service)

    def save_scd(self, scd, output_file_path, format='md'):
        """Save the generated SCD to an output file."""
        if format == 'md':
            with open(output_file_path, 'w') as f:
                f.write(scd)
        elif format == 'csv':
            # Convert SCD to CSV format
            scds = scd.split('\n\n---\n\n')
            csv_data = []
            for scd_entry in scds:
                entry_data = {}
                impl_details = []  # To hold multiple lines of implementation details
                for line in scd_entry.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        entry_data[key.strip()] = value.strip()
                    else:
                        if re.match(r'^\d+\.', line.strip()):  # Check if line starts with numbering
                            impl_details.append(line.strip())
                
                # Add a new row for each line in Implementation Details
                for detail in impl_details:
                    temp_entry = entry_data.copy()  # Copy the other fields
                    temp_entry['Implementation Details'] = detail  # Add one implementation detail per row
                    csv_data.append(temp_entry)

            df = pd.DataFrame(csv_data)
            df.to_csv(output_file_path, index=False)
            print(f"SCD saved to {output_file_path}")
