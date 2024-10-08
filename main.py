from src.model.ai_model import AIModel

class SCDGenerator:
    def __init__(self, model_name):
        # Initialize AIModel with the given model name (e.g., GPT-4)
        self.ai_model = AIModel()

    def generate_scds(self, cloud, service, control_name, description):
        """Generate security control definitions for a given row."""
        # Call the AI model's generate_scd function and pass in necessary arguments
        scd_output = self.ai_model.generate_scd(cloud, service, control_name, description)
        return scd_output
