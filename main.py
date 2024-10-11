
class IOHandler:
    @staticmethod
    def save_to_csv(data, file_path):
        """Save data to a CSV file, ensuring that implementation details are split into rows."""
        rows = []
        for row in data:
            # Use regex to split on number patterns (e.g., "1.", "2.", "3.")
            implementation_details = re.split(r'(?<=\d)\.\s*', row['Implementation Details'])  # Split by digits followed by a period
            for detail in implementation_details:
                new_row = row.copy()  # Copy the row to preserve the rest of the columns
                new_row['Implementation Details'] = detail.strip()  # Set the current implementation detail
                rows.append(new_row)

        # Convert the processed rows into a DataFrame and save as CSV
        df = pd.DataFrame(rows)
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")

    @staticmethod
    def save_to_md(data, file_path):
        """Save data to a Markdown file, ensuring that implementation details are split."""
        with open(file_path, 'w') as md_file:
            for row in data:
                md_file.write(f"## {row['Control ID']} - {row['Cloud Service']}\n")
                md_file.write(f"**Category**: {row['Category']}\n")
                md_file.write(f"**Control Description**: {row['Control Description']}\n")
                
                # Split implementation details using regex
                implementation_details = re.split(r'(?<=\d)\.\s*', row['Implementation Details'])
                md_file.write("### Implementation Details:\n")
                for detail in implementation_details:
                    md_file.write(f"- {detail.strip()}\n")
                
                md_file.write("\n---\n")
        print(f"Data saved to {file_path}")
