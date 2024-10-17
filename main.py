import streamlit as st
import tempfile
import os
from scd_generator import SCDGenerator  # Assuming you have this class defined in a separate file

# Initialize session state
if 'scd_generator' not in st.session_state:
    st.session_state.scd_generator = SCDGenerator()
if 'scds' not in st.session_state:
    st.session_state.scds = []

def main():
    st.title("SCD Generator")

    # Load the datasets
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
    user_prompt = st.text_input("Enter a prompt for SCD generation (e.g., 'Generate all the Security Control Definitions for aws s3')")

    # Select output format
    output_format = st.selectbox("Select output format", ["XLSX", "Markdown", "CSV"])

    # Generate SCD report button
    if st.button("Generate SCD Report"):
        if user_prompt:
            try:
                scd = st.session_state.scd_generator.generate_scd(user_prompt)
                st.session_state.scds.append(scd)
                st.text_area("Generated SCD:", scd, height=300)
            except Exception as e:
                st.error(f"Error generating SCD: {str(e)}")
        else:
            st.warning("Please enter a prompt for SCD generation.")

    # File name input for saving
    file_name = st.text_input("Enter file name for SCD (without extension)", "generated_scd")

    # Combined Save and Download SCDs
    if st.button("Save and Download SCDs"):
        if st.session_state.scds:
            # Determine file extension based on the format selected
            file_extension = "csv" if output_format == "CSV" else "md" if output_format == "Markdown" else "xlsx"
            output_file_path = f"{file_name}.{file_extension}"

            # Combine SCDs into one string
            combined_scd = "\n\n--\n\n".join(st.session_state.scds)

            try:
                # Save the SCDs
                st.session_state.scd_generator.save_scd(combined_scd, output_file_path, format=file_extension)

                # Open the file in binary mode to handle the download
                with open(output_file_path, "rb") as file:
                    st.download_button(
                        label=f"Download {output_format} File",
                        data=file,
                        file_name=output_file_path,
                        mime="text/markdown" if output_format == "Markdown" else "text/csv" if output_format == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                st.success(f"SCDs saved and ready for download as {output_file_path}")
                st.session_state.scds = []  # Clear the SCDs after saving and downloading
            except Exception as e:
                st.error(f"Error saving and downloading SCDs: {str(e)}")
        else:
            st.warning("No SCDs generated yet. Generate at least one SCD before saving and downloading.")

if __name__ == "__main__":
    main()
