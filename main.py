class SCDGenerator:
    # ... existing methods ...

    def generate_scd(self, user_prompt):
        """Generate SCD based on user prompt"""
        if self.dataset is None:
            return "Error: Dataset not loaded. Please load a dataset first."

        # Extract service from user prompt
        service = next((s for s in self.dataset['Cloud Service'].unique() if s.lower() in user_prompt.lower()), "Unknown")

        scd_list = self.ai_model.generate_scd(user_prompt, service)
        return scd_list

    def save_scd(self, scd_list, output_file_path, format='md'):
        """Save the generated SCD to a file"""
        if format == 'md':
            with open(output_file_path, 'w') as f:
                for scd in scd_list:
                    f.write(f"## Control ID: {scd.get('Control ID', 'N/A')}\n")
                    f.write(f"**Control Name**: {scd.get('Control Name', 'N/A')}\n")
                    f.write(f"**Implementation Details**: {scd.get('Implementation Details', 'N/A')}\n")
                    f.write(f"**Responsibility**: {scd.get('Responsibility', 'N/A')}\n")
                    f.write(f"**Frequency**: {scd.get('Frequency', 'N/A')}\n")
                    f.write(f"**Evidence**: {scd.get('Evidence', 'N/A')}\n")
                    f.write(f"**Description**: {scd.get('Description', 'N/A')}\n")
                    f.write("\n---\n")

        elif format == 'csv':
            # Flatten the data into rows for CSV
            df = pd.DataFrame(scd_list)
            df.to_csv(output_file_path, index=False)

        print(f"SCD saved to {output_file_path}")
