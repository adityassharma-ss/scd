import streamlit as st
from src.output.scd_generator import SCDGenerator
from src.data.io_handler import IOHandler
import tempfile

def main():
    st.title("Cloud Security Control Definition Generator")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload the dataset (CSV)", type=["csv"])
    
    if uploaded_file is not None:
        # Create a temporary file to save the uploaded dataset
        temp_input_file = tempfile.NamedTemporaryFile(delete=False)
        temp_input_file.write(uploaded_file.getvalue())
        temp_input_file.close()

        # Load the dataset
        data = IOHandler.load_csv(temp_input_file.name)
        st.write("Dataset loaded successfully:")
        st.dataframe(data)

        # Input prompt from user
        user_prompt = st.text_input("Enter a prompt for SCD generation (e.g., 'S3 bucket')")

        # Output file name
        output_file_path = st.text_input("Enter the output file name", "output_scd_report.md")

        # Generate button
        if st.button("Generate SCD"):
            scd_generator = SCDGenerator()

            # Process SCDs and use temp_input_file.name for input file path
            scd_generator.process_scd(temp_input_file.name, output_file_path, user_prompt)

            st.success(f"SCD report generated and saved to {output_file_path}")

if __name__ == "__main__":
    main()
