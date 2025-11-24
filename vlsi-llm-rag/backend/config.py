import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "VLSI Design AI Tool"
    PROJECT_VERSION: str = "1.0.0"
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Vector Database
    CHROMA_DB_PATH: str = "knowledge_base/vector_db"
    
    # File Upload
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    UPLOAD_DIR: str = "uploads"
    
    # LLM Settings
    LLM_TEMPERATURE: float = 0.1
    MAX_TOKENS: int = 4000
    
    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

settings = Settings()
