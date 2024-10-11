import streamlit as st
import tempfile
from src.output.scd_generator import SCDGenerator

def main():
    st.title("Cloud Security Control Definition (SCD) App")

    # Initialize the SCD Generator
    scd_generator = SCDGenerator()

    # Upload CSV file for dataset
    uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])

    if uploaded_file is not None:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name

        # Load the dataset
        scd_generator.load_dataset(temp_file_path)
        st.success("Dataset loaded successfully!")

        # Input prompt from user for the SCD generation
        user_prompt = st.text_input("Enter a prompt for SCD generation (e.g., 'Generate Security Control for S3 bucket encryption')")

        # Select output format
        output_format = st.selectbox("Select output format", ["Markdown", "CSV"])

        # Generate SCD report button
        if st.button("Generate SCD Report"):
            if user_prompt:
                scd = scd_generator.generate_scd(user_prompt)
                st.text_area("Generated SCD:", scd, height=300)

                # Option to save the SCD
                if st.button("Save SCD to File"):
                    file_extension = "md" if output_format == "Markdown" else "csv"
                    output_file_path = f"generated_scd.{file_extension}"
                    scd_generator.save_scd(scd, output_file_path, format=file_extension)
                    st.success(f"SCD saved to {output_file_path}")
                    
                    with open(output_file_path, "rb") as file:
                        st.download_button(
                            label="Download SCD",
                            data=file,
                            file_name=output_file_path,
                            mime="text/plain" if output_format == "Markdown" else "text/csv"
                        )
            else:
                st.warning("Please enter a prompt for SCD generation.")

if __name__ == "__main__":
    main()
