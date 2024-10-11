import pandas as pd

def save_scd(scd_text, output_file_path):
    """Save the generated SCD to a CSV file, ensuring that each implementation detail fills its own row."""

    # Split the SCD text by double newlines to separate sections
    scd_sections = scd_text.split('\n\n')
    rows = []

    # Parse each section into a structured format
    for section in scd_sections:
        lines = section.split('\n')
        entry_data = {}
        
        # Extracting control fields
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                entry_data[key.strip()] = value.strip()
        
        # Check for Implementation Details and split them
        if 'Implementation Details' in entry_data:
            implementation_details = entry_data['Implementation Details'].split(',')  # Split by commas
            for detail in implementation_details:
                # Create a row for each implementation detail
                rows.append({
                    'Control Name': entry_data.get('Control Name', ''),
                    'Control ID': entry_data.get('Control ID', ''),
                    'Implementation Detail': detail.strip()  # Save each detail
                })
        else:
            # If no implementation details, just save the row with empty details
            rows.append({
                'Control Name': entry_data.get('Control Name', ''),
                'Control ID': entry_data.get('Control ID', ''),
                'Implementation Detail': ''
            })
    
    # Create DataFrame from the rows list
    df = pd.DataFrame(rows)

    # Save the DataFrame to CSV
    df.to_csv(output_file_path, index=False)
    print(f"SCD saved to {output_file_path}")

# Example usage (can be replaced with any model-generated text)
scd_example = """
Control Name: Some Control
Control ID: CTRL-001
Implementation Details: Detail 1, Detail 2, Detail 3

Control Name: Another Control
Control ID: CTRL-002
Implementation Details: Another Detail 1, Another Detail 2
"""

output_file_path = '/mnt/data/output_scd.csv'
save_scd(scd_example, output_file_path)
