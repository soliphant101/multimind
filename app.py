import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("🧠 MultiMind")

# Initialize session state keys upfront
if "prompt_input_box" not in st.session_state:
    st.session_state["prompt_input_box"] = ""
if "chat_history_1" not in st.session_state:
    st.session_state["chat_history_1"] = []

# Define a callback to clear input when submit is pressed
def clear_input():
    st.session_state["prompt_input_box"] = ""

# Prompt input with key tied to session state
prompt = st.text_input("Enter your prompt:", key="prompt_input_box")

# Submit button
if st.button("Submit") and st.session_state["prompt_input_box"].strip():
    prompt = st.session_state["prompt_input_box"]

    # Add user prompt to chat history
    st.session_state["chat_history_1"].append(("User", prompt))

    # API Call (put your real API key here in secrets)
    api_key = st.secrets.get("OPENROUTER_API_KEY", "")
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

    # Add model reply to chat history
    st.session_state["chat_history_1"].append(("GPT-3.5", reply))

    # Clear input box
    clear_input()

# Display chat history in a single scrollable box
conversation = ""
for sender, message in st.session_state["chat_history_1"]:
    conversation += f"**{sender}:**\n{message}\n\n"

st.markdown(
    f"""
    <div style="
        max-height: 400px;
        overflow-y: auto;
        white-space: pre-wrap;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: #f9f9f9;
        font-family: monospace;
    ">
    {conversation}
    </div>
    """,
    unsafe_allow_html=True,
)
