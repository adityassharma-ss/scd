import pandas as pd
from src.model.ai_model import AIModel

class SCDGenerator:
    def __init__(self):
        self.ai_model = AIModel()
        self.dataset = None

    def load_dataset(self, file_path):
        """Load and process the dataset"""
        self.dataset = pd.read_csv(file_path)
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

        return self.ai_model.generate_scd(user_prompt, service)

    def save_scd(self, scd, output_file_path, format='md'):
        """Save the generated SCD to a file"""
        if format == 'md':
            with open(output_file_path, 'w') as f:
                f.write(scd)
        elif format == 'csv':
            # Convert SCD to CSV format
            lines = scd.split('\n')
            csv_data = [line.split(': ', 1) for line in lines if ': ' in line]
            df = pd.DataFrame(csv_data, columns=['Field', 'Value'])
            df.to_csv(output_file_path, index=False)
        
        print(f"SCD saved to {output_file_path}")
