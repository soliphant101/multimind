import streamlit as st

st.set_page_config(layout="wide")
st.title("MultiMind: Compare AI Models")

prompt = st.text_area("Enter your prompt:", height=150)

if st.button("Submit"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Model 1 (Placeholder)")
        st.code("Response from AI model 1...")

    with col2:
        st.subheader("Model 2 (Placeholder)")
        st.code("Response from AI model 2...")

    with col3:
        st.subheader("Model 3 (Placeholder)")
        st.code("Response from AI model 3...")
