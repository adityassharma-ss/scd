import pandas as pd

def save_scd(scd_text, output_file_path):
    """Save the generated SCD to a CSV file where each implementation detail is in a different row."""
    
    # Splitting SCD into sections
    scd_sections = scd_text.split('\n\n')
    implementation_details_list = []

    # Extract Implementation Details and other fields
    for section in scd_sections:
        lines = section.split('\n')
        entry_data = {}
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                entry_data[key.strip()] = value.strip()
        
        # If there are implementation details, split them into multiple rows
        if 'Implementation Details' in entry_data:
            implementation_details = entry_data['Implementation Details'].split(',')  # Assuming they're comma-separated
            for detail in implementation_details:
                # Each detail gets its own row
                implementation_details_list.append({
                    'Control Name': entry_data.get('Control Name', ''),
                    'Control ID': entry_data.get('Control ID', ''),
                    'Implementation Detail': detail.strip()
                })
    
    # Convert to a pandas DataFrame
    df = pd.DataFrame(implementation_details_list)

    # Save DataFrame to CSV
    df.to_csv(output_file_path, index=False)
    print(f"SCD saved to {output_file_path}")

# Example usage
scd_example = """
Control Name: Secure EC2 Access
Control ID: EC2-001
Implementation Details: Enable MFA for EC2 access, Use IAM roles instead of root access, Ensure instance profiles are properly configured

Control Name: EC2 Network Security
Control ID: EC2-002
Implementation Details: Implement VPC security groups, Use NACLs for additional filtering, Ensure proper subnet isolation
"""

output_file_path = '/mnt/data/output_scd.csv'
save_scd(scd_example, output_file_path)
