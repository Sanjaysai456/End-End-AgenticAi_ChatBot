import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from src.langgraphagenticai.state.state import State

# Path to the medical PDF (relative to project root)
MEDICAL_PDF_PATH = "The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND (1).pdf"
FAISS_INDEX_PATH = "./medical_rag_index"

# Embedding model (local, free — no API key required)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class MedicalRAGNode:
    """
    Agentic RAG node that answers medical queries using the
    Gale Encyclopedia of Medicine PDF as its knowledge base.

    On first run:
      - Loads and chunks the PDF
      - Embeds chunks using HuggingFace all-MiniLM-L6-v2
      - Saves FAISS index to ./medical_rag_index/
    On subsequent runs:
      - Loads the saved FAISS index directly (fast)
    """

    def __init__(self, llm):
        self.llm = llm
        self._vectorstore = None
        self._embeddings = None

    # ------------------------------------------------------------------ #
    # Internal helpers                                                     #
    # ------------------------------------------------------------------ #

    def _get_embeddings(self):
        """Lazy-load the HuggingFace embedding model."""
        if self._embeddings is None:
            print("[MedicalRAG] Loading embedding model (all-MiniLM-L6-v2)...")
            self._embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
        return self._embeddings

    def _build_or_load_vectorstore(self):
        """
        Returns the FAISS vectorstore. Builds it from the PDF on first run;
        loads from disk on subsequent runs.
        """
        if self._vectorstore is not None:
            return self._vectorstore

        embeddings = self._get_embeddings()

        # Load cached index if it exists
        if os.path.exists(FAISS_INDEX_PATH):
            print("[MedicalRAG] Loading FAISS index from disk...")
            self._vectorstore = FAISS.load_local(
                FAISS_INDEX_PATH,
                embeddings,
                allow_dangerous_deserialization=True,
            )
            print("[MedicalRAG] FAISS index loaded ✅")
            return self._vectorstore

        # --- First-time build ---
        print("[MedicalRAG] Building FAISS index from PDF (this may take ~1-2 min)...")

        if not os.path.exists(MEDICAL_PDF_PATH):
            raise FileNotFoundError(
                f"Medical PDF not found at '{MEDICAL_PDF_PATH}'. "
                "Please ensure the PDF is in the project root directory."
            )

        # Load PDF pages
        loader = PyPDFLoader(MEDICAL_PDF_PATH)
        pages = loader.load()
        print(f"[MedicalRAG] Loaded {len(pages)} pages from PDF.")

        # Split into manageable chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", " "],
        )
        chunks = splitter.split_documents(pages)
        print(f"[MedicalRAG] Created {len(chunks)} text chunks.")

        # Embed and store
        self._vectorstore = FAISS.from_documents(chunks, embeddings)
        self._vectorstore.save_local(FAISS_INDEX_PATH)
        print(f"[MedicalRAG] FAISS index saved to '{FAISS_INDEX_PATH}' ✅")

        return self._vectorstore

    # ------------------------------------------------------------------ #
    # Public node interface                                                #
    # ------------------------------------------------------------------ #

    def process(self, state: State) -> dict:
        """
        Main LangGraph node entry point.
        Retrieves relevant chunks from the medical PDF and answers the query.
        """
        messages = state.get("messages", [])
        if not messages:
            return {
                "messages": [
                    AIMessage(content="Please ask a medical question and I'll help you from the encyclopedia.")
                ]
            }

        # Extract the latest user question
        user_query = messages[-1].content

        try:
            vectorstore = self._build_or_load_vectorstore()

            # Retrieve top-5 most relevant chunks
            retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 5},
            )
            relevant_docs = retriever.invoke(user_query)

            # Concatenate retrieved context
            context = "\n\n---\n\n".join(
                [f"[Source: Page {doc.metadata.get('page', '?')}]\n{doc.page_content}"
                 for doc in relevant_docs]
            )

            system_prompt = """You are a knowledgeable medical assistant powered by the Gale Encyclopedia of Medicine.
Use ONLY the provided context to answer the user's medical question accurately and clearly.

Guidelines:
- Give clear, structured answers using bullet points or numbered lists where appropriate
- Mention relevant page references from the context when available
- If the context doesn't contain enough information, say so honestly
- Do NOT hallucinate or add information not present in the context
- Format your answer in markdown for readability
- Always end with: "⚕️ *Consult a qualified healthcare professional for personalized medical advice.*"

Context from Gale Encyclopedia of Medicine:
{context}
""".format(context=context)

            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_query),
            ])

            return {"messages": [response]}

        except FileNotFoundError as e:
            error_msg = f"❌ Medical knowledge base not available: {str(e)}"
            return {"messages": [AIMessage(content=error_msg)]}
        except Exception as e:
            error_msg = f"❌ Error in Medical RAG agent: {str(e)}"
            print(f"[MedicalRAG] Exception: {e}")
            return {"messages": [AIMessage(content=error_msg)]}
