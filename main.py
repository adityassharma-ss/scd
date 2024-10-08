from src.output.scd_generator import SCDGenerator
from src.data.io_handler import IOHandler
from src.cost.cost_estimator import CostEstimator
import argparse

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate SCD using GenAI with system and user prompts")
    parser.add_argument("--input", help="Path to input CSV file", required=True)
    parser.add_argument("--output", help="Path to output Markdown file", required=True)
    parser.add_argument("--model", help="OpenAI Model to use (GPT-4 or GPT-3.5)", default="gpt-4")
    
    args = parser.parse_args()

    # Load CSV data
    data = IOHandler.load_csv(args.input)

    # Initialize SCD Generator
    scd_generator = SCDGenerator()

    # Display available cloud services and control names to the user
    print("Select the SCD you want to generate:")
    for idx, row in data.iterrows():
        print(f"{idx + 1}. Cloud: {row['Cloud']}, Service: {row['Service']}, Control: {row['Control Name']}")

    # Ask for user input to select the service/control
    try:
        choice = int(input("\nEnter the number corresponding to the service/control for SCD generation: ")) - 1
        if choice < 0 or choice >= len(data):
            print("Invalid selection. Please select a valid choice.")
            return
        
        # Retrieve the specific row based on user choice
        selected_row = data.iloc[choice]

        # Generate SCD for the selected row
        scd_output = scd_generator.generate_scds(
            selected_row["Cloud"], selected_row["Service"], selected_row["Control Name"], selected_row["Description"]
        )

        # Save output to the Markdown file
        output_data = [{
            'cloud': selected_row["Cloud"],
            'service': selected_row["Service"],
            'control_name': selected_row["Control Name"],
            'scd_output': scd_output
        }]
        IOHandler.save_output(output_data, args.output)

        print(f"\nSCD for {selected_row['Service']} has been generated and saved to {args.output}")

    except ValueError:
        print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
