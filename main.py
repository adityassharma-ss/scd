from src.model.ai_model import AIModel
from src.data.io_handler import IOHandler

class SCDGenerator:
    def __init__(self):
        self.ai_model = AIModel()

    def generate_scds(self, cloud_service, control_id, control_description, config_rule, guidance):
        """Generate security control definitions for a specific control."""
        try:
            scd_output = self.ai_model.generate_scd(cloud_service, control_id, control_description, config_rule, guidance)
            return scd_output
        except Exception as e:
            print(f"Error in SCD generation: {e}")
            return None

    def process_scd(self, input_file_path, output_file_path, user_prompt):
        """Process method: load input, generate SCDs based on user prompt, save output."""
        try:
            data = IOHandler.load_csv(input_file_path)
            scd_outputs = []

            # Filter dataset based on user prompt
            filtered_data = data[data['Control Description'].str.contains(user_prompt, case=False)]

            for index, row in filtered_data.iterrows():
                scd_output = self.generate_scds(row['Cloud Service'], row['Control ID'], row['Control Description'], row['Config Rule'], row['Guidance'])
                scd_outputs.append({
                    'cloud_service': row['Cloud Service'],
                    'control_id': row['Control ID'],
                    'control_description': row['Control Description'],
                    'scd_output': scd_output
                })

            IOHandler.save_output(scd_outputs, output_file_path)

        except Exception as e:
            print(f"Error processing SCD: {e}")
