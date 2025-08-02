# langchain-rag-demo

This repository contains the "Literary AI Explorer," a retrieval-augmented generation (RAG) application built with LangChain and Streamlit. It allows you to ask questions about classic literature—specifically "Alice's Adventures in Wonderland" and "The Jungle Book"—and receive contextually-aware answers.

The application uses a vector database (ChromaDB) populated with the text of these books to provide relevant context to a large language model (Llama 3 via Groq), ensuring the answers are grounded in the source material.

## Features

- **Interactive UI**: A polished and responsive web interface built with Streamlit.
- **Dual Book Querying**: Supports natural language questions for both "Alice in Wonderland" and "The Jungle Book".
- **Context-Aware Answers**: Implements a RAG pipeline to retrieve relevant text chunks before generating an answer.
- **Source Verification**: Displays the exact source passages from the book that were used to generate the answer.
- **High-Performance LLM**: Powered by the Llama 3 70B model via the fast Groq API.
- **Local Embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2` from Hugging Face to generate embeddings locally.

## How It Works

The project is divided into two main processes: data indexing and querying.

1.  **Data Indexing (`create_database.py`)**:
    *   Source documents (the text of the books in Markdown format) are loaded from the `data/` directory.
    *   The documents are split into smaller, overlapping chunks using `RecursiveCharacterTextSplitter`.
    *   Each chunk is converted into a numerical vector (embedding) using a Hugging Face sentence-transformer model.
    *   These embeddings are stored in a ChromaDB vector store, creating a searchable index for each book.

2.  **Querying and Generation (`app.py`, `query_data.py`)**:
    *   The Streamlit app captures a user's question.
    *   The question is converted into an embedding using the same model.
    *   ChromaDB performs a similarity search to find the most relevant text chunks from the specified book's vector store.
    *   These retrieved chunks (context) and the original question are passed to the Llama 3 model via a LangChain `RetrievalQA` chain.
    *   The model generates a comprehensive answer based on the provided context, which is then displayed in the UI along with the source chunks.

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/abhaykumarbadam/langchain-rag-demo.git
cd langchain-rag-demo
```

### 2. Set Up Environment Variables

You will need a Groq API key to use the language model.

1.  Create a file named `.env` in the root of the project directory.
2.  Add your Groq API key to the file:
    ```
    GROQ_API_KEY="your-groq-api-key"
    ```

### 3. Install Dependencies

It is recommended to use a virtual environment.

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the required packages
pip install -r requirements.txt

# Install markdown support for unstructured
pip install "unstructured[md]"
```
**Note on `onnxruntime`**: If you encounter issues installing `chromadb` on macOS, you may need to install `onnxruntime` separately first: `conda install onnxruntime -c conda-forge`. On Windows, ensure you have Microsoft Visual C++ Build Tools installed.

### 4. Prepare Source Data

1.  Create the data directory: `mkdir -p data/books`
2.  Place the text files for your books inside. For this project, you would need `alice.md` and `jungle.md`.
    ```
    .
    └── data/
        └── books/
            ├── alice.md
            └── jungle.md
    ```

### 5. Create the Vector Databases

The application expects separate vector stores for each book. The `create_database.py` script processes all files in `data/books` and saves them to a single `chroma` directory. You will need to run it for each book individually and organize the output.

**For Alice in Wonderland:**
1.  Temporarily move `jungle.md` out of the `data/books` directory.
2.  Run the script: `python create_database.py`
3.  This creates a `chroma/` directory. Rename it: `mv chroma chroma_alice`

**For The Jungle Book:**
1.  Move `alice.md` out and place `jungle.md` back into the `data/books` directory.
2.  Run the script again: `python create_database.py`
3.  Rename the new `chroma/` directory: `mv chroma chroma_jungle`

Finally, create the main `chroma` directory and move your book-specific stores into it. Your final structure should look like this:

```
.
└── chroma/
    ├── alice/
    │   └── ... (chromadb files)
    └── jungle/
        └── ... (chromadb files)
```
*Note: You must update the `BOOK_VECTOR_DIRS` dictionary in `query_data.py` if you use different names or add more books.*

## Usage

### Running the Web Application

Once the setup is complete, run the Streamlit app:

```bash
streamlit run app.py
```

Navigate to the local URL provided by Streamlit (usually `http://localhost:8501`) in your web browser. You can now ask questions in the text-input field or click on the pre-populated sample questions.

### Using the Command-Line Interface (CLI)

You can also query the system directly from your terminal using `query_data.py`.

**Syntax**: `python query_data.py <book_id> "<your_question>"`

-   `<book_id>` must be a key from `BOOK_VECTOR_DIRS` in `query_data.py` (e.g., `alice` or `jungle`).

**Example:**
```bash
python query_data.py jungle "What is the Law of the Jungle?"
```

## Project Structure

```
.
├── data/
│   └── books/
│       ├── alice.md
│       └── jungle.md
├── chroma/
│   ├── alice/
│   └── jungle/
├── app.py                  # The main Streamlit web application.
├── create_database.py      # Script to ingest data and build the ChromaDB vector stores.
├── query_data.py           # Contains the core RAG logic for querying the LLM.
├── requirements.txt        # Python dependencies for the project.
└── README.md