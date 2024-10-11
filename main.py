import os
import streamlit as st
import pandas as pd
import tempfile
from src.output.scd_generator import SCDGenerator

def main():
    st.title("Cloud Security Control Definition (SCD) App")

    # Step 1: File Upload
    uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location for processing
        temp_input_file = tempfile.NamedTemporaryFile(delete=False)
        temp_input_file.write(uploaded_file.getvalue())
        temp_input_file.close()

        # Display the dataset for the user's review
        df = pd.read_csv(temp_input_file.name)
        st.write("Dataset Preview:")
        st.dataframe(df)

        # Step 2: User Prompt
        user_prompt = st.text_input(
            "Enter a prompt for SCD generation (e.g., 'Generate Security Control Definitions for creating S3 bucket')"
        )

        # Step 3: Output File Name
        output_file_name = st.text_input(
            "Enter the output file name for the SCD report (without extension)", "scd_report"
        )

        # Dropdown to select the output format (Markdown or CSV)
        output_format = st.selectbox("Choose the output format", ("Markdown", "CSV"))

        # Step 4: Specify the output directory and file path
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)  # Ensure the output directory exists

        output_file_extension = "md" if output_format.lower() == "markdown" else "csv"
        output_file_path = os.path.join(output_dir, f"{output_file_name}.{output_file_extension}")

        # Generate the SCD report when the button is clicked
        if st.button("Generate SCD Report"):
            scd_generator = SCDGenerator()
            try:
                # Process the SCD and save the report
                scd_generator.process_scd(temp_input_file.name, output_file_path, user_prompt, output_format.lower())

                st.success(f"SCD report generated and saved to {output_file_path}")

                # Step 5: File Download Button
                with open(output_file_path, "rb") as file:
                    st.download_button(
                        label="Download SCD Report",
                        data=file,
                        file_name=f"{output_file_name}.{output_file_extension}",
                        mime="text/markdown" if output_file_extension == "md" else "text/csv"
                    )

            except Exception as e:
                st.error(f"An error occurred while generating the report: {e}")

if __name__ == "__main__":
    main()
