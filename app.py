import streamlit as st
import requests
import html  # For escaping user/model text output

st.set_page_config(layout="wide")
st.title("🧠 MultiMind")

# Initialize chat histories if not present
if "chat_history_1" not in st.session_state:
    st.session_state.chat_history_1 = []

# Initialize prompt input state if missing
if "prompt_input_box" not in st.session_state:
    st.session_state.prompt_input_box = ""

# Input box for user prompt
prompt = st.text_input("Enter your prompt:", key="prompt_input_box")

# Submit button triggers processing
if st.button("Submit") and st.session_state.prompt_input_box.strip():
    prompt = st.session_state.prompt_input_box

    # Append user message to history
    st.session_state.chat_history_1.append(("User", prompt))

    # API call setup
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

    # Append model reply to history
    st.session_state.chat_history_1.append(("GPT-3.5", reply))

    # CLEAR prompt input AFTER processing (crucial)
    st.session_state.prompt_input_box = ""

# Prepare conversation string with proper HTML escaping
conversation = ""
for sender, message in st.session_state.chat_history_1:
    safe_message = html.escape(message)  # Escape HTML here
    conversation += f"**{sender}:**\n{safe_message}\n\n"

# Layout: 3 columns
col1, col2, col3 = st.columns(3)

# Display chat history with scroll box in first column
with col1:
    st.subheader("GPT-3.5 via OpenRouter")
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

# Placeholder columns
with col2:
    st.subheader("Model 2 (coming soon)")
    st.info("This column will show responses from your second AI model.")

with col3:
    st.subheader("Model 3 (coming soon)")
    st.info("This column will show responses from your third AI model.")
