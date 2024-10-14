def generate_scd(self, user_prompt):
    """Generate multiple SCDs based on user prompt"""
    if self.dataset is None:
        return "Error: Dataset not loaded. Please load a dataset first."

    # Extract service from user prompt (this is a simple approach and might need refinement)
    service = next((s for s in self.dataset['Cloud Service'].unique() if s.lower() in user_prompt.lower()), "Unknown")

    # Request multiple SCDs from the AI model
    scds = []
    for i in range(10):  # Change this number to generate the desired amount of SCDs
        control_id = f"{service[:3].upper()}-{i + 1}"  # Use the first three letters of the service for ID
        scd = self.ai_model.generate_scd(user_prompt, service, control_id)
        scds.append(scd)
    
    return "\n\n---\n\n".join(scds)  # Combine the SCDs for consistent output
