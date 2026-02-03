from typing import TypedDict, List, Dict, Any
import logging
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from agent.config.settings import settings
from agent.services.vector_store import vector_store_service

logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    """Represents the state of the RAG agent."""
    question: str
    documents: List[str]
    answer: str

class RAGWorkflow:
    def __init__(self, vector_store=vector_store_service):
        self.vector_store = vector_store
        self.llm = ChatOllama(
            model=settings.LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.2,
            num_predict=1024,
        )
        self.prompt = ChatPromptTemplate.from_template("""
        Você é um assistente especialista em análise de documentos. 
        Use os trechos de contexto abaixo para responder à pergunta de forma detalhada e organizada.
        
        CONTEXTO:
        {context}
        
        PERGUNTA: 
        {question} 
        
        RESPOSTA DETALHADA:
        """)

    def retrieve(self, state: AgentState) -> Dict[str, Any]:
        """Node: Retrieve relevant documents."""
        logger.info(f"Retrieving documents for question: {state['question']}")
        docs = self.vector_store.similarity_search(state["question"], k=settings.RETRIEVAL_K)
        return {"documents": [doc.page_content for doc in docs]}

    def generate(self, state: AgentState) -> Dict[str, Any]:
        """Node: Generate answer from context."""
        logger.info("Generating answer.")
        if not state["documents"]:
            return {"answer": "Desculpe, não encontrei nenhum documento relevante para responder a essa pergunta."}

        context = "\n\n".join(state["documents"])
        chain = self.prompt | self.llm
        response = chain.invoke({"question": state["question"], "context": context})
        return {"answer": response.content}

    def compile(self):
        """Assemble the graph."""
        workflow = StateGraph(AgentState)
        workflow.add_node("retrieve", self.retrieve)
        workflow.add_node("generate", self.generate)
        
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)
        
        return workflow.compile()

# Build the graph
rag_app = RAGWorkflow().compile()
