import streamlit as st
import pandas as pd
import tempfile
from src.output.scd_generator import SCDGenerator
from src.model.ai_model import AIModel

def main():
    st.title("Cloud Security Control Definition (SCD) App")

    # Upload CSV file for dataset
    uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])

    if uploaded_file is not None:
        # Save uploaded file to a temporary location
        temp_input_file = tempfile.NamedTemporaryFile(delete=False)
        temp_input_file.write(uploaded_file.getvalue())
        temp_input_file.close()

        # Display the dataset in Streamlit for user to see
        df = pd.read_csv(temp_input_file.name)
        st.write("Dataset Preview:")
        st.dataframe(df)

        # Input prompt from user for the SCD generation
        user_prompt = st.text_input("Enter a prompt for SCD generation (e.g., 'Generate Security Control Definitions for creating S3 bucket')")

        # Optionally specify the output file name for the SCD report
        output_file_path = st.text_input("Enter the output file name for the SCD report", "scd_report.md")

        # Dropdown to select output format (Markdown or CSV)
        output_format = st.selectbox("Choose the output format", ("Markdown", "CSV"))

        # Generate SCD report button
        if st.button("Generate SCD Report"):
            scd_generator = SCDGenerator()
            scd_generator.process_scd(temp_input_file.name, output_file_path, user_prompt, output_format.lower())
            st.success(f"SCD report generated and saved to {output_file_path}")
            st.download_button("Download SCD report", open(output_file_path, "r").read(), file_name=output_file_path)

if __name__ == "__main__":
    main()
