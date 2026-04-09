"""
RAG Service — LangChain + ChromaDB + OpenAI

Pipeline:
  Upload PDF → PyPDFLoader → RecursiveCharacterTextSplitter
             → OpenAIEmbeddings → ChromaDB (persist)

Query:      Question → ChromaDB similarity search (top-k)
             → RetrievalQA chain (GPT-4 Turbo) → Answer + sources
"""

import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

# In-memory doc registry (persists per process; replace with DB for production)
_doc_registry: dict[str, dict] = {}


def _build_chain(vectorstore):
    from langchain_openai import ChatOpenAI
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are WealthLens, an expert financial analyst AI at BNY Mellon.
Use the following document excerpts to answer the question accurately and concisely.
Always cite specific figures, percentages, or dates when available.
If the answer is not in the context, say so clearly.

Context:
{context}

Question: {question}

Answer (be specific, cite numbers):""",
    )

    llm = ChatOpenAI(
        model="gpt-4-turbo",
        temperature=0,
        openai_api_key=OPENAI_API_KEY,
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )


class RAGService:
    def __init__(self):
        self._vectorstore = None

    def _get_vectorstore(self):
        if self._vectorstore is not None:
            return self._vectorstore

        from langchain_openai import OpenAIEmbeddings
        from langchain_community.vectorstores import Chroma
        import chromadb

        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

        # Use in-memory client to avoid sqlite3 version issues on cloud
        chroma_client = chromadb.Client()
        self._vectorstore = Chroma(
            client=chroma_client,
            collection_name="wealthlens",
            embedding_function=embeddings,
        )
        return self._vectorstore

    def ingest(self, file_path: str, filename: str) -> int:
        """Load, chunk, embed, and store a document. Returns chunk count."""
        from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        ext = os.path.splitext(filename)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path)
        elif ext == ".csv":
            loader = CSVLoader(file_path)
        else:
            raise ValueError(f"Unsupported format: {ext}")

        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", ". ", " "],
        )
        chunks = splitter.split_documents(docs)

        # Tag each chunk with source filename
        for chunk in chunks:
            chunk.metadata["source_file"] = filename

        vs = self._get_vectorstore()
        vs.add_documents(chunks)

        _doc_registry[filename] = {
            "filename": filename,
            "chunks": len(chunks),
            "pages": len(docs),
            "uploaded_at": datetime.utcnow().isoformat(),
            "status": "indexed",
        }
        return len(chunks)

    def query(self, question: str, doc_filter: Optional[str] = None) -> dict:
        """Run a RAG query. Returns answer + source citations."""
        try:
            vs = self._get_vectorstore()
            count = vs._collection.count()
        except Exception:
            count = 0

        if count == 0:
            return {
                "answer": "No documents have been indexed yet. Please upload a PDF using the '+ Upload' button, then ask your question.",
                "sources": [],
                "confidence": 0.0,
            }

        try:
            chain = _build_chain(vs)
            result = chain.invoke({"query": question})

            sources = []
            seen = set()
            for doc in result.get("source_documents", []):
                src = doc.metadata.get("source_file", "Unknown")
                page = doc.metadata.get("page", "")
                label = f"{src} · p.{page + 1}" if page != "" else src
                if label not in seen:
                    seen.add(label)
                    sources.append(label)

            return {
                "answer": result["result"],
                "sources": sources[:4],
                "confidence": round(min(0.95, 0.65 + len(sources) * 0.07), 2),
            }
        except Exception as e:
            return {
                "answer": f"Query failed: {str(e)}",
                "sources": [],
                "confidence": 0.0,
            }

    def list_documents(self) -> list[dict]:
        return list(_doc_registry.values())
