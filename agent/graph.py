from typing import TypedDict, List
import os
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from agent.database import get_vector_store

class AgentState(TypedDict):
    question: str
    documents: List[str]
    answer: str

def retrieve(state: AgentState):
    print("---RETRIEVING---")
    question = state["question"]
    vector_store = get_vector_store()
    # Aumentando para 10 documentos para dar mais contexto
    docs = vector_store.similarity_search(question, k=10)
    return {"documents": [doc.page_content for doc in docs]}

def generate(state: AgentState):
    print("---GENERATING---")
    question = state["question"]
    documents = state["documents"]
    
    if not documents:
        return {"answer": "Desculpe, não encontrei nenhum documento relevante para responder a essa pergunta."}

    # Prompt mais robusto e detalhista
    prompt = ChatPromptTemplate.from_template("""
    Você é um assistente especialista em análise de documentos. 
    Use os trechos de contexto abaixo para responder à pergunta de forma detalhada, organizada e completa.
    
    DIRETRIZES:
    1. Se a informação estiver no contexto, forneça uma resposta rica e explicativa.
    2. Se houver diferentes partes do contexto que se complementam, una-as na resposta.
    3. Se você não encontrar a resposta exata, mas houver informações relacionadas, mencione o que foi encontrado.
    4. Caso não encontre NADA sobre o assunto, responda exatamente: "Desculpe, não encontrei informações sobre isso nos documentos fornecidos."
    5. Não use conhecimentos externos ao contexto fornecido.
    
    CONTEXTO:
    {context}
    
    PERGUNTA: 
    {question} 
    
    RESPOSTA DETALHADA:
    """)
    
    llm = ChatOllama(
        model=os.getenv("LLM_MODEL", "llama3.2"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0.2, # Aumentado levemente para melhor fluência sem perder precisão
        num_predict=1024, # Aumentado para permitir respostas mais longas
    )
    
    context = "\n\n".join(documents)
    chain = prompt | llm
    
    response = chain.invoke({"question": question, "context": context})
    return {"answer": response.content}

def create_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate", generate)
    
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)
    
    return workflow.compile()

app_graph = create_graph()
