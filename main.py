import streamlit as st
import pandas as pd
import tempfile
from src.output.scd_generator import SCDGenerator
from src.utils.config import Config

def main():
    st.title("Cloud Security Control Definition (SCD) App")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])
    
    if uploaded_file is not None:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_input_file = temp_file.name
        
        # Display the dataset
        df = pd.read_csv(temp_input_file)
        st.write("Dataset Preview:")
        st.dataframe(df.head())
        
        # User input for control request
        control_request = st.text_input("Enter your control request:")
        
        if st.button("Generate SCD"):
            scd_generator = SCDGenerator()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as output_file:
                output_file_path = output_file.name
            
            result = scd_generator.process_scd(temp_input_file, output_file_path, control_request)
            
            if result is not None:
                st.success("SCD generated successfully!")
                st.write("Generated SCD:")
                st.dataframe(result)
                
                # Offer download of the generated CSV
                st.download_button(
                    label="Download SCD as CSV",
                    data=result.to_csv(index=False).encode('utf-8'),
                    file_name="generated_scd.csv",
                    mime="text/csv"
                )
            else:
                st.error("Failed to generate SCD. Please check the logs for more information.")

if __name__ == "__main__":
    main()
