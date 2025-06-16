import streamlit as st
import requests
import html  # For escaping output

st.set_page_config(layout="wide")
st.title("🧠 MultiMind")

# Initialize session state
if "chat_history_1" not in st.session_state:
    st.session_state.chat_history_1 = []

if "prompt_input_box" not in st.session_state:
    st.session_state.prompt_input_box = ""

# — Helper to convert our session format into OpenRouter format
def get_message_history():
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for sender, message in st.session_state.chat_history_1:
        role = "user" if sender == "User" else "assistant"
        messages.append({"role": role, "content": message})
    return messages

# Function to submit prompt and clear input
def submit_prompt():
    prompt = st.session_state.prompt_input_box.strip()
    if not prompt:
        return
    st.session_state.chat_history_1.append(("User", prompt))

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
                "messages": get_message_history()
            }
        )
        response.raise_for_status()
        result = response.json()
        reply = result['choices'][0]['message']['content']
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.session_state.chat_history_1.append(("GPT-3.5", reply))

    # CLEAR input here safely:
    st.session_state.prompt_input_box = ""

# Input text box with key bound to session state
st.text_input("Enter your prompt and press ENTER:", key="prompt_input_box", on_change=submit_prompt)

# Layout for chat display
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("GPT-3.5 via OpenRouter")

    conversation = ""
    for sender, message in st.session_state.chat_history_1:
        # Escape to avoid stray HTML tags appearing
        safe_message = html.escape(message)
        conversation += f"\n**{sender}:**\n{safe_message}\n\n"

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

with col2:
    st.subheader("Model 2 (coming soon)")
    st.info("This column will show responses from your second AI model.")

with col3:
    st.subheader("Model 3 (coming soon)")
    st.info("This column will show responses from your third AI model.")
