import streamlit as st
import requests


st.set_page_config(layout="wide")
st.title("MultiMind: Compare AI Models")

prompt = st.text_area("Enter your prompt:", height=150)

if st.button("Submit") and prompt.strip():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("GPT-3.5 via OpenRouter")

        with st.spinner("Waiting for response..."):
            try:
                api_key = st.secrets["OPENROUTER_API_KEY"]

                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "HTTP-Referer": "https://multimind-gld4dbah8hzh2pa4ujh6qq.streamlit.app",  # optional
                        "X-Title": "MultiMind",  # optional
                    },
                    json={
                        "model": "openai/gpt-3.5-turbo",
                        "messages": [
                            {"role": "user", "content": prompt}
                        ]
                    }
                )
                result = response.json()
                output = result['choices'][0]['message']['content']
                st.markdown(f"<div style='white-space: pre-wrap; overflow-y: auto; height: 300px;'>{output}</div>",
    unsafe_allow_html=True)

            except Exception as e:
                st.error(f"API request failed: {e}")

    with col2:
        st.subheader("Model 2 (Coming Soon)")
        st.code("Placeholder...")

    with col3:
        st.subheader("Model 3 (Coming Soon)")
        st.code("Placeholder...")
