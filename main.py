import streamlit as st
import tempfile
import os
from src.output.scd_generator import SCDGenerator

def main():
    st.title("Cloud Security Control Definition (SCDs) App")

    # Initialize the SCD Generator
    if 'scd_generator' not in st.session_state:
        st.session_state.scd_generator = SCDGenerator()

    # Initialize session state for storing SCDs
    if 'scds' not in st.session_state:
        st.session_state.scds = []

    # Upload CSV file for dataset
    uploaded_files = st.file_uploader("Upload your dataset (CSV format)", type=["csv"], accept_multiple_files=True)

    if uploaded_files:
        # Save uploaded files to a temporary location
        temp_file_paths = []
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_file_paths.append(temp_file.name)

        # Load the datasets
        st.session_state.scd_generator.load_datasets(temp_file_paths)
        st.success("Datasets loaded successfully!")

    # User input prompt for SCD generation
    user_prompt = st.text_input("Enter a prompt for SCD generation (e.g., 'Generate all the Security Control Definitions for aws s3')")
    
    # Select output format
    output_format = st.selectbox("Select output format", ["XLSX", "Markdown", "CSV"])

    # Generate SCD report button
    if st.button("Generate SCD Report"):
        if user_prompt:
            scd = st.session_state.scd_generator.generate_scd(user_prompt)
            st.session_state.scds.append(scd)
            st.text_area("Generated SCD:", scd, height=300)
        else:
            st.warning("Please enter a prompt for SCD generation.")

    # File name input for saving
    file_name = st.text_input("Enter file name for SCD (without extension)", "generated_scd")

    # Save and Download SCDs
    if st.button("Save and Download SCDs"):
        if st.session_state.scds:
            # Combine SCDs into one string
            combined_scd = "\n\n".join(st.session_state.scds)
            
            # Determine file extension based on the format selected
            file_extension = ".csv" if output_format == "CSV" else ".xlsx" if output_format == "XLSX" else ".md"
            output_file_path = f"{file_name}{file_extension}"
            
            # Save the SCDs to a file
            st.session_state.scd_generator.save_scd(combined_scd, output_file_path, format=file_extension)

            # Open the file in binary mode to handle the download
            with open(output_file_path, "rb") as file:
                st.download_button(
                    label=f"Download {output_format} File",
                    data=file,
                    file_name=output_file_path,
                    mime="text/csv" if output_format == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if output_format == "XLSX" else "text/markdown"
                )
            
            st.success(f"SCDs saved and ready for download as {output_file_path}")
            st.session_state.scds = []  # Clear the SCDs after saving and downloading
        else:
            st.warning("No SCDs generated yet. Generate at least one SCD before saving.")

if __name__ == "__main__":
    main()
