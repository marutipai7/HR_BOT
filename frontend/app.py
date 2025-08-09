import streamlit as st
import requests

st.set_page_config(page_title="HR Resource Query Chatbot", page_icon="💼")

st.title("💼 HR Resource Query Chatbot")

backend_url = "http://127.0.0.1:8000/chat"

query = st.text_input("Enter your HR query:", placeholder="e.g., Find Python developers with 3+ years experience")

if st.button("Search"):
    if query.strip():
        with st.spinner("Searching..."):
            response = requests.post(backend_url, json={"query": query})
            if response.status_code == 200:
                st.markdown(response.json()["response"])
            else:
                st.error("Error connecting to backend")
