import chromadb
from sentence_transformers import SentenceTransformer
import os
from typing import List, Dict, Any
from ...config import settings

class RAGService:
    def __init__(self):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection = self._get_or_create_collection()
        self._initialize_knowledge_base()
    
    def _get_or_create_collection(self):
        try:
            return self.client.get_collection("vlsi_knowledge")
        except:
            return self.client.create_collection("vlsi_knowledge")
    
    def _initialize_knowledge_base(self):
        """Initialize with some VLSI design knowledge"""
        if self.collection.count() == 0:
            default_docs = [
                {
                    "id": "1",
                    "text": "AMBA AXI Protocol: Separate address/control and data phases. Support for burst transactions. Five independent channels: read address, read data, write address, write data, write response.",
                    "metadata": {"type": "protocol", "source": "axi"}
                },
                {
                    "id": "2", 
                    "text": "UART Protocol: Asynchronous serial communication. Start bit, data bits (5-8), optional parity bit, stop bit(s). Common baud rates: 9600, 115200.",
                    "metadata": {"type": "protocol", "source": "uart"}
                },
                {
                    "id": "3",
                    "text": "FSM Design: Use one-hot encoding for better timing. Separate combinational and sequential logic. Include reset functionality.",
                    "metadata": {"type": "design_pattern", "source": "fsm"}
                },
                {
                    "id": "4",
                    "text": "PPA Optimization: Use clock gating for power reduction. Pipeline design for performance. Resource sharing for area optimization.",
                    "metadata": {"type": "optimization", "source": "ppa"}
                }
            ]
            
            self.collection.add(
                documents=[doc["text"] for doc in default_docs],
                metadatas=[doc["metadata"] for doc in default_docs],
                ids=[doc["id"] for doc in default_docs]
            )
    
    def query(self, query_text: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Query the knowledge base for relevant information"""
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            
            formatted_results = []
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    "text": doc,
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if results['distances'] else 0
                })
            
            return formatted_results
        except Exception as e:
            print(f"RAG Query Error: {e}")
            return []
    
    def add_document(self, text: str, metadata: Dict[str, Any]):
        """Add a new document to the knowledge base"""
        doc_id = f"doc_{self.collection.count() + 1}"
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )

rag_service = RAGService()
