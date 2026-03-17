from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.config import settings

class VectorStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_db = Chroma(persist_directory=settings.VECTOR_DB_PATH, embedding_function=self.embeddings)

    def add_document(self, text: str, metadata: dict):
        # Split text into chunks first
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_text(text)
        
        self.vector_db.add_texts(texts=chunks, metadatas=[metadata]*len(chunks))

    def retrieve_context(self, query: str, k=3):
        results = self.vector_db.similarity_search(query, k=k)
        return "\n".join([doc.page_content for doc in results])
