from dotenv import load_dotenv
from src.ingestion.loader import load_pdf
from src.ingestion.chunking import split_documents
from src.embeddings.embedding_model import get_embedding_model
from src.vectorstore.chroma_db import create_vector_store
from src.retrieval.retriever import get_retriever
from src.llm.llm_model import get_llm
from src.workflow.langgraph_flow import build_graph

load_dotenv()

def main():
    docs = load_pdf("data/sample.pdf")
    chunks = split_documents(docs)
    db = create_vector_store(chunks, get_embedding_model())
    retriever = get_retriever(db)
    llm = get_llm()
    graph = build_graph(retriever, llm)

    while True:
        q = input("Ask (exit to quit): ")
        if q == "exit": break
        res = graph.invoke({"query": q})
        print("Answer:", res.get("answer"))

if __name__ == "__main__":
    main()
