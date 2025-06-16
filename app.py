import streamlit as st
import requests


st.set_page_config(layout="wide")
st.title("MultiMind: Compare AI Models")

# User input
prompt = st.text_input("Enter your prompt:", key="prompt_input")

# Handle submission
if st.button("Submit") and prompt.strip():
    # Add user's message to GPT-3.5's chat history
    st.session_state.chat_history_1.append(("User", prompt))

    # === GPT-3.5 (OpenRouter) ===
    api_key = st.secrets["OPENROUTER_API_KEY"]
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://multimind-gld4dbah8hzh2pa4ujh6qq.streamlit.app",
        "X-Title": "MultiMind"
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        result = response.json()
        reply = result['choices'][0]['message']['content']
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    # Add model's reply to chat history
    st.session_state.chat_history_1.append(("GPT-3.5", reply))

    # === Placeholder for Model 2 ===
    # st.session_state.chat_history_2.append(("User", prompt))
    # response_2 = call_model_2(prompt)
    # st.session_state.chat_history_2.append(("Model 2", response_2))

    # === Placeholder for Model 3 ===
    # st.session_state.chat_history_3.append(("User", prompt))
    # response_3 = call_model_3(prompt)
    # st.session_state.chat_history_3.append(("Model 3", response_3))

    # Clear input field after submission
    st.session_state.prompt_input = ""


    with col2:
        st.subheader("Model 2 (Coming Soon)")
        st.code("Placeholder...")

    with col3:
        st.subheader("Model 3 (Coming Soon)")
        st.code("Placeholder...")
