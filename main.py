def save_scd(self, scd, output_file_path, format='md'):
    """Save the generated SCD to a file"""
    if format == 'md':
        with open(output_file_path, 'w') as f:
            f.write(scd)
    elif format == 'csv':
        # Split SCD entries and process for CSV
        scds = scd.split("\n\n---\n\n")
        csv_data = []
        
        for scd_entry in scds:
            entry_data = {}
            lines = scd_entry.split('\n')
            
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    entry_data[key.strip()] = value.strip()

            # Ensure that implementation details are in a single row
            if 'Implementation Details' in entry_data:
                details = entry_data['Implementation Details'].split(',')  # Assuming details are comma-separated
                entry_data['Implementation Details'] = details  # Store as a list for row-wise filling
                
            csv_data.append(entry_data)

        # Convert to a dataframe
        df = pd.DataFrame(csv_data)
        
        # Ensure each row contains one implementation detail
        df = df.explode('Implementation Details')
        
        # Save to CSV
        df.to_csv(output_file_path, index=False)

    print(f"SCD saved to {output_file_path}")
