import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("🧠 MultiMind")

# Initialize session state variables if missing
if "prompt_input_box" not in st.session_state:
    st.session_state.prompt_input_box = ""

if "chat_history_1" not in st.session_state:
    st.session_state.chat_history_1 = []

if "clear_input_flag" not in st.session_state:
    st.session_state.clear_input_flag = False

# Clear the prompt input safely by setting a flag and rerunning
def clear_input():
    st.session_state.prompt_input_box = ""
    st.session_state.clear_input_flag = False
    st.experimental_rerun()

# If the clear flag is set, clear input and rerun
if st.session_state.clear_input_flag:
    clear_input()

# Prompt input
prompt = st.text_input("Enter your prompt:", value=st.session_state.prompt_input_box, key="prompt_input_box")

# Submit button logic
if st.button("Submit") and prompt.strip():
    prompt_text = prompt.strip()
    st.session_state.chat_history_1.append(("User", prompt_text))

    # GPT-3.5 API call via OpenRouter
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
                "messages": [{"role": "user", "content": prompt_text}]
            }
        )
        response.raise_for_status()
        result = response.json()
        reply = result['choices'][0]['message']['content']
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.session_state.chat_history_1.append(("GPT-3.5", reply))

    # Set flag to clear input next run (safe)
    st.session_state.clear_input_flag = True

# Layout for three columns
col1, col2, col3 = st.columns(3)

# Display GPT-3.5 chat history in col1 with scrollable box
with col1:
    st.subheader("GPT-3.5 via OpenRouter")

    conversation = ""
    for sender, message in st.session_state.chat_history_1:
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

# Placeholders for Model 2 and Model 3
with col2:
    st.subheader("Model 2 (coming soon)")
    st.info("This column will show responses from your second AI model.")

with col3:
    st.subheader("Model 3 (coming soon)")
    st.info("This column will show responses from your third AI model.")
