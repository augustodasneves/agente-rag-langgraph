import streamlit as st
import requests
import os

# Configurações iniciais
st.set_page_config(page_title="RAG Agent Pro", page_icon="🤖", layout="wide")

# Gerenciamento de Tema (Claro/Escuro)
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

def toggle_theme():
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

# CSS Dinâmico com Animações Premium
theme_colors = {
    'dark': {
        'bg': '#0e1117',
        'text': '#ffffff',
        'bubble_user': '#2e2e2e',
        'bubble_assistant': '#1a1c23',
        'border': '#3e3e3e',
        'input_bg': '#262730',
        'sidebar_bg': '#1a1c23'
    },
    'light': {
        'bg': '#ffffff',
        'text': '#1f2937',
        'bubble_user': '#f3f4f6',
        'bubble_assistant': '#ffffff',
        'border': '#e5e7eb',
        'input_bg': '#f9fafb',
        'sidebar_bg': '#f3f4f6'
    }
}

curr = theme_colors[st.session_state.theme]

st.markdown(f"""
<style>
    /* Global Reset and Background */
    .stApp, .main, [data-testid="stHeader"], [data-testid="stAppViewContainer"] {{
        background-color: {curr['bg']} !important;
        color: {curr['text']} !important;
        transition: all 0.3s ease;
    }}

    /* Text Color for all elements */
    h1, h2, h3, p, span, div, label, .stMarkdown, [data-testid="stMarkdownContainer"] p {{
        color: {curr['text']} !important;
    }}

    /* Animation */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Inputs */
    .stTextInput > div > div > input {{
        background-color: {curr['input_bg']} !important;
        color: {curr['text']} !important;
        border-radius: 10px;
        border: 1px solid {curr['border']} !important;
    }}

    /* Buttons */
    .stButton > button {{
        border-radius: 10px;
        background: linear-gradient(45deg, #4b6cb7, #182848);
        color: white !important;
        border: none;
        padding: 0.5rem 2rem;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}

    .stButton > button:hover {{
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }}

    /* Chat Bubbles */
    .chat-bubble {{
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        max-width: 85%;
        animation: fadeIn 0.4s ease-out;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        line-height: 1.6;
        border: 1px solid {curr['border']};
    }}

    .user-bubble {{
        background-color: {curr['bubble_user']} !important;
        margin-left: auto;
        border-bottom-right-radius: 2px;
    }}

    .assistant-bubble {{
        background-color: {curr['bubble_assistant']} !important;
        margin-right: auto;
        border-bottom-left-radius: 2px;
    }}

    /* Titles */
    .title-gradient {{
        background: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
    }}

    /* Sidebar Fixes */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] {{
        background-color: {curr['sidebar_bg']} !important;
        border-right: 1px solid {curr['border']} !important;
    }}
    
    [data-testid="stSidebar"] * {{
        color: {curr['text']} !important;
    }}

    /* Chat Input Fixed at Bottom */
    [data-testid="stChatInput"] {{
        background-color: {curr['bg']} !important;
    }}

    /* Hide Default Streamlit Style */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# Header com seletor de tema
col1, col2 = st.columns([0.9, 0.1])
with col1:
    st.markdown('<h1 class="title-gradient">RAG Agent Explorer</h1>', unsafe_allow_html=True)
with col2:
    if st.button("🌓"):
        toggle_theme()
        st.rerun()

AGENT_URL = os.getenv("AGENT_URL", "http://localhost:8000")

# Sidebar para uploads
with st.sidebar:
    st.header("📂 Conhecimento")
    st.write("Adicione documentos PDF para treinar o agente em tempo real.")
    
    uploaded_file = st.file_uploader("Upload de PDF", type="pdf", help="Selecione um arquivo PDF para indexar")
    
    if uploaded_file:
        if st.button("🚀 Indexar Documento"):
            with st.spinner("Processando PDF e gerando embeddings..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(f"{AGENT_URL}/upload", files=files)
                    if response.status_code == 200:
                        st.success("✅ Documento indexado com sucesso!")
                    else:
                        st.error(f"❌ Erro: {response.json().get('detail', 'Falha desconhecida')}")
                except Exception as e:
                    st.error(f"❌ Erro de conexão: {e}")

    st.markdown("---")
    st.subheader("⚙️ Status do Sistema")
    try:
        health = requests.get(f"{AGENT_URL}/health").json()
        st.success(f"Backend: {health['status'].upper()}")
    except:
        st.error("Backend: OFFLINE")

# Histórico de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibição das mensagens
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
    label = "Você" if role == "user" else "Assistente"
    
    st.markdown(f"""
        <div class="chat-bubble {bubble_class}">
            <small style="opacity: 0.7;">{label}</small><br>
            {content}
        </div>
    """, unsafe_allow_html=True)

# Área de input
query = st.chat_input("Pergunte algo sobre seus documentos...")
if query:
    # Adicionar mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": query})
    st.rerun()

# Lógica para processar a última pergunta (se houver)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_query = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant"):
        with st.spinner("Consultando documentos e gerando resposta..."):
            try:
                response = requests.post(f"{AGENT_URL}/ask", json={"question": last_query})
                if response.status_code == 200:
                    ans = response.json()["answer"]
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                    st.rerun()
                else:
                    st.error("Erro ao processar sua pergunta no servidor.")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")

# Footer
st.markdown("---")
st.caption("🚀 Desenvolvido com LangGraph, PgVector & Ollama | 100% Local e Privado")
