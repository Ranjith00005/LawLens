import streamlit as st
import requests

# API base URL
API_BASE_URL = "http://localhost:9001"

# Streamlit UI
st.set_page_config(page_title="LawLens⚖️", layout="centered")
st.title("⚖️ LawLens - Legal Research Assistant")
st.markdown("Upload legal documents and get AI-powered legal insights!")

# File Upload
uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

# Query Input
query = st.text_area("Enter your legal query:")

# Option Selection
option = st.selectbox("Select a Service:", [
    "Legal Advisory",
    "Legal Report Generation",
    "Case Outcome Prediction"
])

# Submit Button
if st.button("Get Response"):
    if not uploaded_files:
        st.warning("Please upload at least one PDF file.")
    elif not query:
        st.warning("Please enter a legal query.")
    else:
        # Prepare file payload
        files = [("files", (file.name, file, "application/pdf")) for file in uploaded_files]
        data = {"query": query}
        endpoint = ""
        
        # Determine endpoint based on option
        if option == "Legal Advisory":
            endpoint = "/legal-advisory/"
        elif option == "Legal Report Generation":
            endpoint = "/report-generator/"
        elif option == "Case Outcome Prediction":
            endpoint = "/case-outcome-prediction/"
        
        response = requests.post(f"{API_BASE_URL}{endpoint}", data=data, files=files)
        
        if response.status_code == 200:
            result = response.json()
            st.success("✅ Response Received!")
            for key, value in result.items():
                st.markdown(f"**{key.replace('_', ' ').title()}**")
                st.write(value)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
