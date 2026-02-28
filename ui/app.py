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
        'bg': '#121212',
        'secondary_bg': '#1e1e1e',
        'text': '#ffffff',
        'text_dim': '#b0b0b0',
        'accent': '#6366f1',
        'border': '#333333',
        'input_bg': '#252525',
        'bubble_user': '#312e81',
        'bubble_assistant': '#1e1e1e',
        'upload_bg': '#252525'
    },
    'light': {
        'bg': '#ffffff',
        'secondary_bg': '#f3f4f6',
        'text': '#1f2937',
        'text_dim': '#6b7280',
        'accent': '#4f46e5',
        'border': '#e5e7eb',
        'input_bg': '#ffffff',
        'bubble_user': '#eff6ff',
        'bubble_assistant': '#f9fafb',
        'upload_bg': '#f3f4f6'
    }
}

curr = theme_colors[st.session_state.theme]

# CSS de "Força Bruta" para domar o layout do Streamlit
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Outfit:wght@800&display=swap');

    /* 1. Global Reset & Body */
    html, body, .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {curr['bg']} !important;
        color: {curr['text']} !important;
        font-family: 'Inter', sans-serif !important;
    }}

    /* 2. Main Containers Visibility Fix */
    [data-testid="stMain"], 
    [data-testid="stHeader"], 
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    [data-testid="stElementContainer"] {{
        background-color: transparent !important;
        color: {curr['text']} !important;
    }}

    /* 3. Exhaustive Global Text Color */
    p, span, label, li, h1, h2, h3, h4, 
    small, .stMarkdown, [data-testid="stMarkdownContainer"] p,
    [data-testid="stWidgetLabel"] p, .stCaption {{
        color: {curr['text']} !important;
    }}

    /* 4. Sidebar Fixing */
    [data-testid="stSidebar"] {{
        background-color: {curr['secondary_bg']} !important;
        border-right: 1px solid {curr['border']} !important;
        width: 350px !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        padding-top: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}

    /* 5. FILE UPLOADER - Total Correction */
    [data-testid="stFileUploadDropzone"] {{
        background-color: {curr['upload_bg']} !important;
        border: 2px dashed {curr['border']} !important;
        border-radius: 12px !important;
        padding: 2rem !important;
    }}

    /* Estilo dos textos internos do uploader */
    [data-testid="stFileUploadDropzone"] div, 
    [data-testid="stFileUploadDropzone"] span,
    [data-testid="stFileUploadDropzone"] p {{
        color: {curr['text']} !important;
    }}
    
    [data-testid="stFileUploaderFileName"] {{
        color: {curr['text']} !important;
        font-weight: 600;
    }}

    /* 6. CHAT INPUT - Fixing the "Black Block" */
    /* Target the literal bottom bar container */
    [data-testid="stChatInput"] {{
        background-color: {curr['bg']} !important;
        border-top: 1px solid {curr['border']} !important;
        padding: 2rem !important;
        margin-bottom: 0px !important;
    }}
    
    /* Target the wrapper around the input */
    footer + div, [data-testid="stAppViewContainer"] > section:last-child {{
        background-color: {curr['bg']} !important;
    }}

    [data-testid="stChatInput"] textarea {{
        background-color: {curr['input_bg']} !important;
        color: {curr['text']} !important;
        border: 1px solid {curr['border']} !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }}

    /* 7. Buttons */
    .stButton > button {{
        width: 100%;
        border-radius: 10px !important;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.6rem !important;
        font-weight: 600 !important;
    }}

    /* 8. Chat Bubbles */
    .chat-bubble {{
        padding: 1.2rem;
        border-radius: 18px;
        margin-bottom: 1rem;
        max-width: 85%;
        border: 1px solid {curr['border']};
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}

    .user-bubble {{
        background-color: {curr['bubble_user']} !important;
        margin-left: auto;
        border-bottom-right-radius: 4px;
        color: { '#ffffff' if st.session_state.theme == 'dark' else curr['text'] } !important;
    }}

    .assistant-bubble {{
        background-color: {curr['bubble_assistant']} !important;
        margin-right: auto;
        border-bottom-left-radius: 4px;
    }}

    /* 9. Title Style */
    .title-gradient {{
        background: linear-gradient(to right, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Outfit', sans-serif;
    }}

    /* 10. Hide default elements */
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
