import pandas as pd
from src.model.ai_model import AIModel

class SCDGenerator:
    def __init__(self):
        self.ai_model = AIModel()

    def process_scd(self, input_file_path, output_file_path, control_request):
        df = pd.read_csv(input_file_path)
        
        print(f"User Prompt: {control_request}")
        print("Dataset Preview:")
        print(df.head())
        
        expected_columns = ['Control ID', 'Control Description', 'Guidance', 'Cloud Service']
        for col in expected_columns:
            if col not in df.columns:
                print(f"Warning: Missing expected column '{col}' in the dataset.")
                return None
        
        output_data = []
        
        for index, row in df.iterrows():
            control_description = row.get('Control Description', '').lower()
            cloud_service = row.get('Cloud Service', '').lower()
            guidance = row.get('Guidance', '').lower()
            prompt_lower = control_request.lower()
            
            if prompt_lower in control_description or prompt_lower in guidance or prompt_lower in cloud_service:
                control_id = row.get('Control ID', f"CTRL-{index + 1:03d}")
                
                ai_response = self.ai_model.generate_scd(
                    cloud=row.get('Cloud Service', 'Unknown'),
                    service=row.get('Config Rule', 'Unknown'),
                    control_name=row.get('Control Description', 'Unknown'),
                    description=row.get('Guidance', 'Unknown'),
                    user_prompt=control_request
                )
                
                if ai_response:
                    parts = ai_response.split('\n')
                    implementation_details = next((p.split(': ', 1)[1] for p in parts if p.startswith('Implementation Details:')), '')
                    responsibility = next((p.split(': ', 1)[1] for p in parts if p.startswith('Responsibility:')), 'Customer')
                    frequency = next((p.split(': ', 1)[1] for p in parts if p.startswith('Frequency:')), 'Continuous')
                    evidence = next((p.split(': ', 1)[1] for p in parts if p.startswith('Evidence:')), 'Evidence required.')
                    
                    output_data.append([
                        control_id,
                        row.get('Control Description', f"Control for {index + 1}"),
                        row.get('Guidance', f"Description for control {index + 1}"),
                        implementation_details,
                        responsibility,
                        frequency,
                        evidence
                    ])
                    
                    print(f"Matched Control: {control_id}, {row.get('Control Description')}")
        
        if not output_data:
            print("No controls matched the user prompt.")
            return None
        
        output_df = pd.DataFrame(output_data, columns=[
            'Control ID', 'Control Name', 'Description', 'Implementation Details',
            'Responsibility', 'Frequency', 'Evidence'
        ])
        
        output_df.to_csv(output_file_path, index=False)
        print(f"Output successfully written to {output_file_path}")
        
        return output_df
