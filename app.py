import streamlit as st
import requests
import html  # For escaping output

st.set_page_config(layout="wide")

# response box layout
st.markdown(
    f"""
    <style>
    .response-box {{
        max-height: 70vh;
        min-height: 200px;
        overflow-y: auto;
        white-space: pre-wrap;
        padding: 16px;
        margin-top: 10px;
        border-radius: 15px;
        background: linear-gradient(to bottom right, #ffffff, #f1f1f1);
        border: 1px solid #ddd;
        font-family: 'Courier New', monospace;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }}
    </style>
    """,
    unsafe_allow_html=True
)


#reduce whitespace at top of page
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

#title
st.markdown("""
    <h1 style='text-align: center; font-size: 3em; margin-bottom: 1rem;'>🧠 MultiMind</h1>
""", unsafe_allow_html=True)

# Initialize session states
if "chat_history_1" not in st.session_state:
    st.session_state.chat_history_1 = []

if "chat_history_2" not in st.session_state:
    st.session_state.chat_history_2 = []

if "chat_history_3" not in st.session_state:
    st.session_state.chat_history_3 = []

if "prompt_input_box" not in st.session_state:
    st.session_state.prompt_input_box = ""

# — Helper to convert our session format into OpenRouter format
def get_message_history():
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for sender, message in st.session_state.chat_history_1:
        role = "user" if sender == "User" else "assistant"
        messages.append({"role": role, "content": message})
    return messages

def get_message_history_2():
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for sender, message in st.session_state.chat_history_2:
        role = "user" if sender == "User" else "assistant"
        messages.append({"role": role, "content": message})
    return messages

def get_message_history_3():
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for sender, message in st.session_state.chat_history_3:
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
                "model": "deepseek/deepseek-r1:free",
                "messages": get_message_history()
            }
        )
        response.raise_for_status()
        result = response.json()
        reply = result['choices'][0]['message']['content']
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.session_state.chat_history_1.append(("DeepSeek", reply))

     # --- LLaMA via OpenRouter ---
    st.session_state.chat_history_2.append(("User", prompt))  # Add same user prompt

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": "meta-llama/llama-3-8b-instruct",
                "messages": get_message_history_2()
            }
        )
        response.raise_for_status()
        result = response.json()
        reply = result['choices'][0]['message']['content']
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.session_state.chat_history_2.append(("LLaMA", reply))

       # --- Gemini via OpenRouter ---
    st.session_state.chat_history_3.append(("User", prompt))  # Add same user prompt

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": get_message_history_3()
            }
        )
        response.raise_for_status()
        result = response.json()
        reply = result['choices'][0]['message']['content']
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.session_state.chat_history_3.append(("Gemini", reply))

    # CLEAR input here safely:
    st.session_state.prompt_input_box = ""

# Input text box with key bound to session state
left, center, right = st.columns([3, 2, 3])
with center:
    st.markdown("<div style='text-align: center; font-size: 16px; font-weight: bold;'>MultiMind allows you to chat with three different AI models simultaneously. Input your prompt and press ENTER:</div>", unsafe_allow_html=True)
    st.text_area(
        label="",
        key="prompt_input_box",
        height=80,
        on_change=submit_prompt
    )



# Layout for chat display
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<h4>DeepSeek R1</h4>', unsafe_allow_html=True)

    conversation = ""
    for sender, message in st.session_state.chat_history_1:
        # Escape to avoid stray HTML tags appearing
        safe_message = html.escape(message)
        conversation += f"\n**{sender}:**\n{safe_message}\n\n"

     st.markdown(
         f"<div class='response-box'>{conversation}</div>",
         unsafe_allow_html=True,
        )


with col2:
    st.markdown('<h4>LLaMA 3</h4>', unsafe_allow_html=True)

    conversation = ""
    for sender, message in st.session_state.chat_history_2:
        safe_message = html.escape(message)
        conversation += f"\n**{sender}:**\n{safe_message}\n\n"

    st.markdown(
        f"""
        <div style="
            max-height: 70vh;
            min-height: 200px;
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

with col3:
    st.markdown('<h4>Gemini 2.0</h4>', unsafe_allow_html=True)
    conversation = ""
    for sender, message in st.session_state.chat_history_3:
        safe_message = html.escape(message)
        conversation += f"\n**{sender}:**\n{safe_message}\n\n"
    st.markdown(
        f"""
       <div style="
            max-height: 70vh;
            min-height: 200px;
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