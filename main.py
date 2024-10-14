import streamlit as st
import tempfile
from src.output.scd_generator import SCDGenerator
import os

def main():
    st.title("Cloud Security Control Definition (SCD) App")

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

        st.session_state.scd_generator.load_datasets(temp_file_paths)
        st.success("Datasets loaded successfully!")

    # User input prompt for SCD generation
    user_prompt = st.text_input("Enter a prompt for SCD generation (e.g., 'Generate Security Control for S3 bucket')")

    # Select output format
    output_format = st.selectbox("Select output format", ["Markdown", "CSV"])

    # Generate SCD report button
    if st.button("Generate SCD Report"):
        if user_prompt:
            scd = st.session_state.scd_generator.generate_scd(user_prompt)
            
            # Ensure the generated SCD is a string before appending
            if isinstance(scd, list):
                scd = "\n\n".join(map(str, scd))  # Flatten list into a string

            st.session_state.scds.append(scd)
            st.text_area("Generated SCD:", scd, height=300)
        else:
            st.warning("Please enter a prompt for SCD generation.")

    # File name input for saving
    file_name = st.text_input("Enter file name for SCD (without extension)", "generated_scd")

    # Save and download SCDs
    if st.button("Save and Download SCDs"):
        if st.session_state.scds:
            file_extension = "md" if output_format == "Markdown" else "csv"
            output_file_path = f"{file_name}.{file_extension}"

            # Ensure each SCD is a string before joining
            scds = []
            for scd in st.session_state.scds:
                if isinstance(scd, list):
                    scd_str = "\n\n".join(map(str, scd))  # Flatten list into a string
                    scds.append(scd_str)
                else:
                    scds.append(str(scd))

            # Join all the SCDs
            combined_scd = "\n\n---\n\n".join(scds)

            st.session_state.scd_generator.save_scd(combined_scd, output_file_path, format=file_extension)

            # Download button for the saved file
            with open(output_file_path, "rb") as file:
                st.download_button(
                    label=f"Download {output_format} File",
                    data=file,
                    file_name=output_file_path,
                    mime="text/plain" if output_format == "Markdown" else "text/csv"
                )

            st.success(f"SCDs saved and ready for download as {output_file_path}")
        else:
            st.warning("No SCDs generated yet. Generate at least one SCD before saving.")

if __name__ == "__main__":
    main()
