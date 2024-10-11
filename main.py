import streamlit as st
from src.output.scd_generator import SCDGenerator
import os
import tempfile

def main():
    st.title("Cloud Security Control Definition (SCD) App")

    # Initialize the SCD Generator
    if 'scd_generator' not in st.session_state:
        st.session_state.scd_generator = SCDGenerator()

    # Initialize session state for storing SCDs
    if 'scds' not in st.session_state:
        st.session_state.scds = []

    # Upload CSV files for dataset
    uploaded_files = st.file_uploader("Upload your datasets (CSV format)", type=["csv"], accept_multiple_files=True)

    if uploaded_files:
        temp_files = []
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_files.append(temp_file.name)

        # Load the dataset
        st.session_state.scd_generator.load_dataset(temp_files)
        st.success("Datasets loaded successfully!")

    user_prompt = st.text_input("Enter a prompt for SCD generation (e.g., 'Generate Security Control for S3 bucket')")

    output_format = st.selectbox("Select output format", ["Markdown", "CSV"])

    if st.button("Generate SCD Report"):
        if user_prompt:
            scd = st.session_state.scd_generator.generate_scd(user_prompt)
            st.session_state.scds.append(scd)
            st.text_area("Generated SCD:", scd, height=300)
        else:
            st.warning("Please enter a prompt for SCD generation.")

    file_name = st.text_input("Enter file name for SCD (without extension)", "generated_scd")

    if st.button("Save and Download SCDs"):
        if st.session_state.scds:
            file_extension = "md" if output_format == "Markdown" else "csv"
            output_file_path = f"{file_name}.{file_extension}"

            combined_scd = "\n\n---\n\n".join(st.session_state.scds)
            st.session_state.scd_generator.save_scd(combined_scd, output_file_path, format=file_extension)

            with open(output_file_path, "rb") as file:
                st.download_button(
                    label=f"Download {output_format} File",
                    data=file,
                    file_name=output_file_path,
                    mime="text/plain" if output_format == "Markdown" else "text/csv"
                )
        else:
            st.warning("No SCDs generated yet. Generate at least one SCD before saving.")

if __name__ == "__main__":
    main()
