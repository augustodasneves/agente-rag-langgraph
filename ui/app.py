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
    /* Global Background and Basic Font Color */
    html, body, .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {curr['bg']} !important;
        color: {curr['text']} !important;
        transition: background-color 0.3s ease, color 0.3s ease;
    }}

    /* Target every possible main container */
    [data-testid="stMain"], 
    [data-testid="stHeader"], 
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stVerticalBlock"] {{
        background-color: {curr['bg']} !important;
    }}

    /* Force text color on everything including nested spans and labels */
    .stApp *, [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p, 
    span, label, p, h1, h2, h3, h4, h5, h6, small {{
        color: {curr['text']} !important;
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: {curr['sidebar_bg']} !important;
        border-right: 1px solid {curr['border']} !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2 {{
        color: {curr['text']} !important;
    }}

    /* Input Fields */
    .stTextInput input, .stSelectbox div, .stTextArea textarea {{
        background-color: {curr['input_bg']} !important;
        color: {curr['text']} !important;
        border: 1px solid {curr['border']} !important;
        border-radius: 8px !important;
    }}

    /* Chat Input Fixed at the bottom */
    [data-testid="stChatInput"] {{
        background-color: {curr['bg']} !important;
        border-top: 1px solid {curr['border']} !important;
        padding-bottom: 20px !important;
    }}
    
    [data-testid="stChatInput"] textarea {{
        background-color: {curr['input_bg']} !important;
        color: {curr['text']} !important;
        border: 1px solid {curr['border']} !important;
    }}

    /* Buttons */
    .stButton > button {{
        border-radius: 12px;
        background: linear-gradient(45deg, #4b6cb7, #182848);
        color: white !important;
        border: none;
        padding: 0.6rem 2.2rem;
        transition: all 0.3s ease;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        background: linear-gradient(45deg, #5c7dd8, #2a3d66);
    }}

    /* Custom Chat Bubbles */
    .chat-bubble {{
        padding: 1.2rem;
        border-radius: 18px;
        margin-bottom: 1.2rem;
        max-width: 85%;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        line-height: 1.6;
        border: 1px solid {curr['border']};
        animation: fadeIn 0.5s ease-out;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(15px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .user-bubble {{
        background-color: {curr['bubble_user']} !important;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }}

    .assistant-bubble {{
        background-color: {curr['bubble_assistant']} !important;
        margin-right: auto;
        border-bottom-left-radius: 4px;
    }}

    /* Title Styling */
    .title-gradient {{
        background: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1.5rem;
        letter-spacing: -1px;
    }}

    /* Clean UI */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stHeader"] {{background-color: transparent !important;}}
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
