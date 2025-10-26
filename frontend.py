import streamlit as st
import requests
import json
from datetime import datetime

# ------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------
st.set_page_config(
    page_title="Munawar Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
/* --- Global Styles --- */
body {
    font-family: 'Inter', sans-serif;
    /* Deeper, less saturated background for main canvas */
    background-color: #0c1523; /* Very dark blue */
    color: #e2e8f0; /* Soft light gray for primary text */
    line-height: 1.6; /* Improved text readability */
}

/* Base text color for all containers */
p, label, li, span, h1, h2, h3, h4, h5, h6 {
    color: inherit; /* Inherit color from parent for consistency */
}

/* --- Sidebar --- */
section[data-testid="stSidebar"] {
    /* Slightly lighter than body, providing separation */
    background-color: #16243b !important; /* Deep slate blue */
    border-right: 1px solid #2d3c52; /* Subtle divider line */
    padding: 2rem 1.5rem; /* Increased vertical padding for air */
}
/* Ensure headings in the sidebar stand out */
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3, 
section[data-testid="stSidebar"] h4 {
    color: #f1f5f9; /* Near-white for contrast */
    margin-bottom: 0.75rem; /* Better vertical rhythm */
}

/* --- Forms & Inputs (Textarea, Select, Input) --- */
/* Common styling for all major input types */
textarea, select, input[type="text"], input[type="password"], input[type="number"] {
    background-color: #24354b !important; /* Darker input field background */
    color: #f1f5f9 !important; /* High-contrast text within input */
    border-radius: 8px !important; /* Slightly more rounded corners */
    border: 1px solid #3d506d !important; /* Subtler border color */
    padding: 0.75rem 1rem !important; /* Increased padding inside inputs */
    line-height: 1.4 !important; /* Ensure text sits well */
    margin-bottom: 1rem !important; /* Add space below each input */
    box-shadow: none !important; /* Remove default Streamlit shadows */
    transition: all 0.2s ease-in-out;
}
textarea:focus, select:focus, input[type="text"]:focus, input[type="password"]:focus, input[type="number"]:focus {
    border-color: #3b82f6 !important; /* Standard blue focus color */
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3) !important; /* Subtle blue glow */
    outline: none !important;
    background-color: #24354b !important; /* Keep background stable on focus */
}
/* Specifically target Streamlit's main content area inputs (if applicable) */
div[data-testid="stForm"] textarea,
div[data-testid="stForm"] input {
    width: 100%;
}


/* --- Buttons --- */
.stButton>button {
    width: 100%;
    border-radius: 8px; /* Consistent rounded corners */
    background-color: #3b82f6; /* Primary action blue */
    color: #f8fafc;
    border: none;
    font-weight: 600; /* Bolder text for CTA */
    padding: 0.75rem 1rem; /* More vertical padding */
    transition: background-color 0.2s ease-in-out;
}
.stButton>button:hover {
    background-color: #2563eb; /* Darker blue on hover */
}

/* --- Chat Bubbles (Assuming standard Streamlit custom classes) --- */
/* User Message (Highlighting user action) */
.user-message {
    background-color: #2563eb; /* Brighter blue for user */
    color: #f1f5f9;
    border-radius: 12px; /* Slightly rounder */
    padding: 14px 18px; /* More padding */
    margin: 10px 20px 10px 0; /* More balanced margins (no margin on the left for user) */
    max-width: 75%; /* Limit bubble width */
    align-self: flex-end; /* Align to the right side of the container */
}
/* Assistant Message (Subtle background) */
.assistant-message {
    background-color: #1e293b; /* Subtle contrast to the body background */
    color: #e2e8f0;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 10px 0 10px 20px; /* More balanced margins (no margin on the right for assistant) */
    max-width: 75%; /* Limit bubble width */
    align-self: flex-start; /* Align to the left side of the container */
}
/* Adjust the container that holds the chat elements for flex layout */
div[data-testid="stChatMessage"] {
    display: flex;
    flex-direction: column;
}

/* Timestamp/Meta-Info */
.timestamp {
    font-size: 12px; /* Slightly larger */
    color: #7d90a7; /* Muted, readable gray */
    text-align: right;
    margin-top: 6px; /* Increased separation */
    padding-right: 18px; /* Align with bubble padding */
}

/* --- Footer --- */
.footer {
    text-align: center;
    color: #5b6c86; /* Very muted gray */
    font-size: 13px;
    margin-top: 50px; /* More vertical spacing before the footer */
    padding-top: 20px;
    border-top: 1px solid #1e293b; /* Subtle line above footer */
}
</style>
""", unsafe_allow_html=True)
# ------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ------------------------------------------------------
# SIDEBAR CONFIGURATION
# ------------------------------------------------------
with st.sidebar:
    st.markdown("## Munawar Agent Settings")
    st.markdown("<hr style='border-color:#475569;'>", unsafe_allow_html=True)

    st.subheader("Agent Configuration")
    system_prompt = st.text_area(
        "System Prompt",
        height=90,
        placeholder="Describe your agent’s tone, role, or expertise..."
    )

    st.markdown("<hr style='border-color:#475569;'>", unsafe_allow_html=True)

    st.subheader("Model Settings")
    provider = st.selectbox("Select Provider", ["Groq", "OpenAI"])
    MODEL_OPTIONS = {
        "Groq": ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
        "OpenAI": ["gpt-4o-mini"]
    }
    selected_model = st.selectbox("Select Model", MODEL_OPTIONS[provider])
    allow_web_search = st.checkbox("Enable Web Search", value=False)

    st.markdown("<hr style='border-color:#475569;'>", unsafe_allow_html=True)

    st.subheader("Actions")
    if st.button("Clear Conversation"):
        st.session_state["messages"].clear()
        st.success("Conversation cleared successfully.")

    st.caption("Modify your configuration anytime. Settings apply to future messages.")


st.markdown("<h2 style='text-align:center; color:#f1f5f9;'>AI Agent </h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>A conversational workspace built for intelligent assistance</p>", unsafe_allow_html=True)
st.write("")



chat_container = st.container()
for msg in st.session_state["messages"]:
    role, content, timestamp = msg["role"], msg["content"], msg["time"]
    if role == "user":
        st.markdown(
            f"""
            <div class="user-message">
                <b>You:</b><br>{content}
                <div class="timestamp">{timestamp}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="assistant-message">
                <b>Munawar Agent:</b><br>{content}
                <div class="timestamp">{timestamp}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


user_query = st.chat_input("Type your message here...")

API_URL = "http://127.0.0.1:9999/chat"

if user_query:
    # Save user message
    st.session_state["messages"].append({
        "role": "user",
        "content": user_query,
        "time": datetime.now().strftime("%H:%M")
    })

    with st.spinner("Generating response..."):
        try:
            # Build payload safely
            payload = {
                "model_name": selected_model,
                "model_provider": provider,
                "system_prompt": system_prompt,
                "messages": [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state["messages"]
                ],
                "allow_search": allow_web_search
            }

            # Send to backend
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                response_data = response.json()

                if response_data.get("status") == "success":
                    agent_reply = response_data["data"]["response"]
                elif "error" in response_data:
                    agent_reply = f"Error: {response_data['error']}"
                else:
                    # Safely format JSON to avoid HTML issues
                    agent_reply = json.dumps(response_data, indent=2)
            else:
                agent_reply = f"Request failed ({response.status_code})"

        except Exception as e:
            agent_reply = f"Error: {str(e)}"

    # Save agent reply
    st.session_state["messages"].append({
        "role": "assistant",
        "content": agent_reply,
        "time": datetime.now().strftime("%H:%M")
    })

    # Rerun to refresh UI
    st.rerun()


st.markdown(
    "<div class='footer'>© 2025 Munawar Shereen</div>",
    unsafe_allow_html=True
)
