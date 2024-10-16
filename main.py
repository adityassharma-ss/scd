import streamlit as st
import tempfile
import openai
from src.cost.cost_estimator import CostEstimator
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
        temp_file_paths = []
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_file_paths.append(temp_file.name)

        # Load the datasets
        st.session_state.scd_generator.load_datasets(temp_file_paths)
        st.success("Datasets loaded successfully!")

    # User input prompt for SCD generation
    user_prompt = st.text_input("Enter a prompt for SCD generation (e.g., 'Generate all the Security Control Definition'):")

    # Select output format after the SCD generation
    output_format = st.selectbox("Select output format", ["Markdown", "CSV", "XLSX"])

    # Estimate cost before generating SCD
    cost_estimator = CostEstimator()
    cost_info = cost_estimator.estimate_cost(user_prompt, model="gpt-4")

    if 'error' in cost_info:
        st.warning(f"Error estimating cost: {cost_info['error']}")
    else:
        st.info(f"Estimated cost: ${cost_info['total_cost']:.4f} for {cost_info['prompt_tokens']} prompt tokens "
                f"and {cost_info['completion_tokens']} completion tokens.")

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

    # Download button will only appear if SCDs have been generated
    if st.session_state.scds:
        combined_scd = "\n\n--\n\n".join(st.session_state.scds)
        file_extension = "csv" if output_format == "CSV" else "md" if output_format == "Markdown" else "xlsx"
        output_file_path = f"{file_name}.{file_extension}"

        st.download_button(
            label=f"Download {output_format} File",
            data=combined_scd.encode('utf-8'),
            file_name=output_file_path,
            mime="text/markdown" if output_format == "Markdown" else "text/csv" if output_format == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.success(f"SCDs saved and ready for download as {output_file_path}")

        # Clear session state after download
        st.session_state.scds = []

if __name__ == "__main__":
    main()
