def save_scd(self, scd, output_file_path, format='md'):
    if format == 'md':
        with open(output_file_path, 'w') as f:
            f.write(scd)
    elif format == 'csv':
        # Split SCDs and prepare data for CSV
        scds = scd.split('\n\n---\n\n')
        csv_data = []
        
        for scd_entry in scds:
            entry_data = {}
            impl_details = []  # To hold multiple lines of implementation details
            
            for line in scd_entry.split('\n'):
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    entry_data[key.strip()] = value.strip()
                else:
                    # Check if line starts with numbering (e.g., "1.", "2.", etc.)
                    if re.match(r'^\d+\.', line.strip()): 
                        impl_details.append(line.strip())  # Collect all implementation details
                        
            # Add a new row for each line in Implementation Details
            for detail in impl_details:
                temp_entry = entry_data.copy()  # Copy the other fields
                temp_entry['Implementation Details'] = detail  # Add one implementation detail per row
                csv_data.append(temp_entry)

        df = pd.DataFrame(csv_data)
        df.to_csv(output_file_path, index=False)

    print(f"SCD saved to {output_file_path}")
