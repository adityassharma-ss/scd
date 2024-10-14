# main.py
import streamlit as st
import tempfile
import os
from src.output.scd_generator import SCDGenerator

def main():
    st.title("Cloud Security Control Definition (SCD) Generator")

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

        # Load datasets into the SCD generator
        st.session_state.scd_generator.load_datasets(temp_file_paths)

        # Remove temporary files after loading
        for temp_file_path in temp_file_paths:
            os.remove(temp_file_path)

        st.success("Datasets loaded successfully!")

    # User input for generating SCDs
    user_prompt = st.text_area("Enter your request for generating Security Control Definitions (SCD):")
    if st.button("Generate SCD"):
        if user_prompt:
            scd = st.session_state.scd_generator.generate_scd(user_prompt)
            st.session_state.scds.append(scd)
            st.success("SCD generated successfully!")

            # Display generated SCD
            st.subheader("Generated SCD:")
            st.write(scd)

            # Option to save the SCD
            if st.button("Save SCD"):
                output_format = st.selectbox("Select output format", ["Markdown", "CSV"])
                output_file = st.text_input("Enter output file name", "scd_output")

                if st.button("Download"):
                    if output_format == "Markdown":
                        output_file_path = f"{output_file}.md"
                        st.session_state.scd_generator.save_scd(scd, output_file_path, format='md')
                        with open(output_file_path, "r") as f:
                            st.download_button("Download Markdown", f, file_name=output_file_path)
                    elif output_format == "CSV":
                        output_file_path = f"{output_file}.csv"
                        st.session_state.scd_generator.save_scd(scd, output_file_path, format='csv')
                        with open(output_file_path, "r") as f:
                            st.download_button("Download CSV", f, file_name=output_file_path)

if __name__ == "__main__":
    main()
