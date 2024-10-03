# app/frontend.py

import streamlit as st
from app.langchain_pipeline import generate_policy_with_langchain

st.title("Generative AI Cloud Security Policy Generator")

# Input fields
service_name = st.text_input("Cloud Service Name", "e.g., S3, EC2, RDS")
security_requirement = st.text_input("Security Requirement", "e.g., Encrypt data at rest")

if st.button("Generate Policy"):
    if service_name and security_requirement:
        # Generate policy using LangChain
        result = generate_policy_with_langchain(service_name, security_requirement)
        st.subheader("Generated Policy and Best Practice")
        st.write(result)
    else:
        st.warning("Please provide both service name and security requirement.")
