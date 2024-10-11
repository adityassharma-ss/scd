
import streamlit as st
import pandas as pd
import io
from src.output.scd_generator import SCDGenerator  # Assuming you have this implemented elsewhere

def main():
    st.title("Cloud Security Control Definition (SCD) App")

    # Step 1: File Upload
    uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])

    if uploaded_file is not None:
        # Display the dataset for the user's review
        df = pd.read_csv(uploaded_file)
        st.write("Dataset Preview:")
        st.dataframe(df)

        # Step 2: User Prompt
        user_prompt = st.text_input(
            "Enter a prompt for SCD generation (e.g., 'Generate Security Control Definitions for creating S3 bucket')"
        )

        # Dropdown to select the output format (Markdown or CSV)
        output_format = st.selectbox("Choose the output format", ("Markdown", "CSV"))

        # Step 3: Generate the SCD report when the button is clicked
        if st.button("Generate SCD Report"):
            scd_generator = SCDGenerator()

            try:
                # Process the SCD with user prompt and generate content in-memory
                output_data = scd_generator.process_scd(df, user_prompt)

                # Step 4: Prepare the output for download
                if output_format.lower() == "markdown":
                    # Convert output to Markdown format
                    output_buffer = io.StringIO(output_data)
                    st.download_button(
                        label="Download SCD Report",
                        data=output_buffer.getvalue(),
                        file_name="scd_report.md",
                        mime="text/markdown"
                    )
                else:
                    # Convert output to CSV format
                    output_buffer = io.StringIO()
                    output_data.to_csv(output_buffer, index=False)
                    st.download_button(
                        label="Download SCD Report",
                        data=output_buffer.getvalue(),
                        file_name="scd_report.csv",
                        mime="text/csv"
                    )

                st.success(f"SCD report generated successfully.")
            
            except Exception as e:
                st.error(f"An error occurred while generating the report: {e}")

if __name__ == "__main__":
    main()
