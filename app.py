import streamlit as st
import requests
import html  # <-- Import this to escape message content

st.set_page_config(layout="wide")
st.title("🧠 MultiMind")

# Initialize chat histories if not already
if "chat_history_1" not in st.session_state:
    st.session_state.chat_history_1 = []

# Initialize prompt input if not already
if "prompt_input_box" not in st.session_state:
    st.session_state.prompt_input_box = ""

# Input box for prompt
prompt = st.text_input("Enter your prompt:", key="prompt_input_box")

# Submit button logic
if st.button("Submit") and st.session_state.prompt_input_box.strip():
    prompt = st.session_state.prompt_input_box

    # Add prompt to chat history
    st.session_state.chat_history_1.append(("User", prompt))

    # Call OpenRouter API
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

    # Append model reply
    st.session_state.chat_history_1.append(("GPT-3.5", reply))

    # Clear input box AFTER processing the input
    st.session_state.prompt_input_box = ""

# Layout columns
col1, col2, col3 = st.columns(3)

# Build conversation string with escaped message content
conversation = ""
for sender, message in st.session_state.chat_history_1:
    safe_message = html.escape(message)  # <-- Escape each message here
    conversation += f"**{sender}:**\n{safe_message}\n\n"

# Display conversation inside scrollable box
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

# Placeholders for future models
with col2:
    st.subheader("Model 2 (coming soon)")
    st.info("This column will show responses from your second AI model.")

with col3:
    st.subheader("Model 3 (coming soon)")
    st.info("This column will show responses from your third AI model.")
