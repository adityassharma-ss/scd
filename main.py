import streamlit as st
import tempfile
import os
from src.output.scd_generator import SCDGenerator
from src.model.model_trainer import ModelTrainer

def main():
    st.title("Security Control Definitions (SCDs) App")

    # Initialize the model trainer
    model_trainer = ModelTrainer()

    # Check if the model is already trained
    try:
        model_trainer.load_trained_model()
        st.success("Model loaded successfully!")
    except FileNotFoundError:
        st.warning("Model not trained. Training now...")
        model_trainer.train()
        st.success("Model trained successfully!")

    # Initialize the SCD generator
    if 'scd_generator' not in st.session_state:
        st.session_state.scd_generator = SCDGenerator()

    if 'scds' not in st.session_state:
        st.session_state.scds = []

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
            combined_scd = "\n\n---\n\n".join(st.session_state.scds)

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
                st.session_state.scds = []
            except Exception as e:
                st.error(f"Error saving and downloading SCDs: {str(e)}")
        else:
            st.warning("No SCDs generated yet. Generate at least one SCD before saving and downloading.")

if __name__ == "__main__":
    main()
