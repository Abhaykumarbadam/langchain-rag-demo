import os
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Embedding model is shared
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Mapping of book_id to Chroma persist directories
BOOK_VECTOR_DIRS = {
    "alice": "chroma/alice",
    "jungle": "chroma/jungle",
    # add more books here with their vectorstore dirs
}

# Cache for loaded RetrievalQA chains per book
qa_chains = {}

def get_qa_chain(book_id: str) -> RetrievalQA:
    """
    Load or return cached RetrievalQA chain for the given book_id.
    """
    if book_id not in qa_chains:
        persist_dir = BOOK_VECTOR_DIRS.get(book_id)
        if not persist_dir:
            raise ValueError(f"No vector store directory configured for book_id '{book_id}'")

        db = Chroma(persist_directory=persist_dir, embedding_function=embedding_function)
        retriever = db.as_retriever(search_kwargs={"k": 10})

        llm = ChatOpenAI(
            model="llama3-70b-8192",
            openai_api_key=os.getenv("GROQ_API_KEY"),
            openai_api_base="https://api.groq.com/openai/v1",
            temperature=0.7
        )
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
        qa_chains[book_id] = qa_chain
    return qa_chains[book_id]

def get_answer(query: str, book_id: str):
    """
    Given a query string and book_id, return answer and sources
    from the corresponding RetrievalQA chain.
    """
    qa = get_qa_chain(book_id)
    result = qa.invoke({"query": query})  # or qa(query) depending on LangChain version
    answer = result.get("result") or result
    sources = result.get("source_documents", [])
    return answer, sources

# Optional CLI test
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python query_data.py <book_id> 'your question here'")
        sys.exit(1)

    book_id = sys.argv[1]
    query = sys.argv[2]

    answer, sources = get_answer(query, book_id)
    print(f"\nAnswer:\n{answer}\n")
    print("Sources:")
    for doc in sources:
        print(f"- {doc.metadata.get('source', 'Unknown')}")
