import streamlit as st
import pandas as pd
from scd_generator import SCDGenerator
from model import Model
from config import Config
from cost_estimator import CostEstimator
import tempfile

def main():
    st.title("Cloud Security Control Definition (SCD) and Cost Estimation")

    # Upload CSV file for dataset
    uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])
    
    if uploaded_file is not None:
        # Save uploaded file to a temporary location
        temp_input_file = tempfile.NamedTemporaryFile(delete=False)
        temp_input_file.write(uploaded_file.getvalue())
        temp_input_file.close()

        # Display the dataset in Streamlit for user to see
        df = pd.read_csv(temp_input_file.name)
        st.write("Dataset Preview:")
        st.dataframe(df)

        # Input prompt from user for the SCD generation
        user_prompt = st.text_input("Enter a prompt (e.g., 'Create S3 bucket')")

        # Optionally specify the output file name for the SCD report
        output_file_path = st.text_input("Enter the output file name for the SCD report", "scd_report.md")

        # Dropdown to select additional functionalities
        functionality = st.selectbox(
            "Choose an additional functionality",
            ("None", "Cost Estimation", "AI Model Prediction")
        )

        # Generate SCD report button
        if st.button("Generate SCD Report"):
            scd_generator = SCDGenerator()
            scd_generator.process_scd(temp_input_file.name, output_file_path, user_prompt)
            st.success(f"SCD report generated and saved to {output_file_path}")
            st.download_button("Download SCD report", open(output_file_path, "r").read(), file_name=output_file_path)

        # If the user selects "Cost Estimation", call the cost estimator
        if functionality == "Cost Estimation" and st.button("Estimate Cost"):
            cost_estimator = CostEstimator()
            estimated_cost = cost_estimator.estimate(df)  # Assuming it works on a dataframe
            st.write(f"Estimated cost: {estimated_cost}")

        # If the user selects "AI Model Prediction", call the model logic
        if functionality == "AI Model Prediction" and st.button("Run Model Prediction"):
            model = Model()
            model_result = model.predict(user_prompt, df)  # Assuming model takes prompt and dataframe
            st.write("Model Prediction Results:")
            st.write(model_result)

if __name__ == "__main__":
    main()
