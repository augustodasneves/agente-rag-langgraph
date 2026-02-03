import streamlit as st
import requests
import os

st.set_page_config(page_title="RAG Agent Pro", page_icon="🤖", layout="wide")

# Premium styling
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
        border-radius: 10px;
        border: 1px solid #4a4a4a;
    }
    .stButton > button {
        border-radius: 10px;
        background: linear-gradient(45deg, #4b6cb7, #182848);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .chat-bubble {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        max-width: 80%;
    }
    .user-bubble {
        background-color: #2e2e2e;
        margin-left: auto;
    }
    .assistant-bubble {
        background-color: #1a1c23;
        border: 1px solid #3e3e3e;
    }
    .title-gradient {
        background: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title-gradient">RAG Agent Explorer</h1>', unsafe_allow_html=True)

AGENT_URL = os.getenv("AGENT_URL", "http://localhost:8000")

# Sidebar for uploads
with st.sidebar:
    st.header("📂 Document Knowledge")
    uploaded_file = st.file_uploader("Upload PDF context", type="pdf")
    if uploaded_file:
        if st.button("Ingest Document"):
            with st.spinner("Processing PDF..."):
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(f"{AGENT_URL}/upload", files={"file": (uploaded_file.name, uploaded_file.getvalue())})
                if response.status_code == 200:
                    st.success("Document ingested!")
                else:
                    st.error("Failed to ingest document.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
    st.markdown(f"""
        <div class="chat-bubble {bubble_class}">
            <b>{"You" if role == "user" else "Assistant"}:</b><br>{content}
        </div>
    """, unsafe_allow_html=True)

# Input area
with st.container():
    query = st.chat_input("Ask anything about your documents...")
    if query:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(f"{AGENT_URL}/ask", json={"question": query})
                    if response.status_code == 200:
                        ans = response.json()["answer"]
                        st.markdown(ans)
                        st.session_state.messages.append({"role": "assistant", "content": ans})
                    else:
                        st.error("Error communicating with agent.")
                except Exception as e:
                    st.error(f"Connection error: {e}")

# Footer
st.markdown("---")
st.caption("Powered by LangGraph, PgVector & Ollama")
