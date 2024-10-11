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
        self.ai_model.set_dataset_summary(summary)

    def generate_scd(self, user_prompt):
        """Generate SCD based on user prompt"""
        if self.dataset is None:
            return "Error: Dataset not loaded. Please load a dataset first."

        return self.ai_model.generate_scd(user_prompt)

    def save_scd(self, scd, output_file_path):
        """Save the generated SCD to a file"""
        with open(output_file_path, 'w') as f:
            f.write(scd)
        print(f"SCD saved to {output_file_path}")
