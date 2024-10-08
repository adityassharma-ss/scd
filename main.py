from src.model.ai_model import AIModel
from src.data.io_handler import IOHandler

class SCDGenerator:
    def __init__(self):
        self.ai_model = AIModel()

    def generate_scds(self, cloud, service, control_name, description):
        """Generate security control definitions for the entire dataset."""
        try:
            scd_output = self.ai_model.generate_scd(cloud, service, control_name, description)
            return scd_output
        except Exception as e:
            print(f"Error in SCD generation: {e}")
            return None

    def process_scd(self, input_file_path, output_file_path):
        """Processing method: load input, generate SCDs, save output"""
        try:
            data = IOHandler.load_csv(input_file_path)
            scd_outputs = []
            for _, row in data.iterrows():
                scd_output = self.generate_scds(row['Cloud'], row['Service'], row['Control Name'], row['Description'])
                scd_outputs.append({
                    'cloud': row['Cloud'],
                    'service': row['Service'],
                    'control_name': row['Control Name'],
                    'scd_output': scd_output
                })
            IOHandler.save_output(scd_outputs, output_file_path)
        except Exception as e:
            print(f"Error processing SCD: {e}")
