from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.api.routes import router as api_router
from app.core.config import settings

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Automated Front-End VLSI Design AI Tool using LLM RAG",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React frontend
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Serve static files for uploads
if os.path.exists("uploads"):
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Serve knowledge base files
if os.path.exists("knowledge_base"):
    app.mount("/knowledge", StaticFiles(directory="knowledge_base"), name="knowledge")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🚀 Automated Front-End VLSI Design AI Tool",
        "version": settings.PROJECT_VERSION,
        "docs": "/api/docs",
        "endpoints": {
            "health": "/api/v1/health",
            "generate_rtl": "/api/v1/generate-rtl",
            "generate_testbench": "/api/v1/generate-testbench",
            "upload_spec": "/api/v1/upload-spec"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint for load balancers and monitoring"""
    return {
        "status": "healthy",
        "service": "VLSI RAG Backend",
        "version": settings.PROJECT_VERSION
    }

@app.get("/api/status")
async def status():
    """Detailed status endpoint"""
    import psutil
    import datetime
    
    # Check if knowledge base is accessible
    kb_status = "healthy" if os.path.exists(settings.CHROMA_DB_PATH) else "unhealthy"
    
    # Check if upload directory exists
    upload_status = "healthy" if os.path.exists(settings.UPLOAD_DIR) else "unhealthy"
    
    # System information
    system_info = {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "boot_time": datetime.datetime.fromtimestamp(psutil.boot_time()).isoformat()
    }
    
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "components": {
            "knowledge_base": kb_status,
            "upload_directory": upload_status,
            "llm_service": "available" if settings.GEMINI_API_KEY else "unconfigured"
        },
        "system": system_info
    }

@app.get("/api/info")
async def api_info():
    """API information and configuration"""
    return {
        "project_name": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "features": {
            "rag_enabled": True,
            "llm_integration": bool(settings.GEMINI_API_KEY),
            "file_upload": True,
            "testbench_generation": True
        },
        "limits": {
            "max_file_size": f"{settings.MAX_FILE_SIZE / (1024 * 1024)} MB",
            "chunk_size": settings.CHUNK_SIZE,
            "max_tokens": settings.MAX_TOKENS
        },
        "endpoints": [
            {"method": "GET", "path": "/api/v1/health", "description": "Health check"},
            {"method": "POST", "path": "/api/v1/generate-rtl", "description": "Generate RTL from specification"},
            {"method": "POST", "path": "/api/v1/generate-testbench", "description": "Generate testbench for RTL"},
            {"method": "POST", "path": "/api/v1/upload-spec", "description": "Upload and parse specification file"},
            {"method": "GET", "path": "/api/status", "description": "Detailed system status"},
            {"method": "GET", "path": "/api/info", "description": "API information"}
        ]
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Endpoint not found",
        "path": request.url.path,
        "available_endpoints": [
            "/api/v1/health",
            "/api/v1/generate-rtl", 
            "/api/v1/generate-testbench",
            "/api/v1/upload-spec",
            "/api/docs"
        ]
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "Internal server error",
        "message": "An unexpected error occurred. Please try again later.",
        "request_id": getattr(request, "request_id", "unknown")
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    import os
    from app.services.rag_service import rag_service
    from app.services.llm_service import llm_service
    
    # Create necessary directories
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)
    os.makedirs("knowledge_base/specs", exist_ok=True)
    os.makedirs("knowledge_base/protocols", exist_ok=True)
    
    print("🚀 VLSI Design AI Tool Backend Starting...")
    print(f"📁 Upload directory: {settings.UPLOAD_DIR}")
    print(f"📚 Knowledge base: {settings.CHROMA_DB_PATH}")
    print(f"🔑 LLM configured: {bool(settings.GEMINI_API_KEY)}")
    
    # Initialize services
    try:
        # Test RAG service
        rag_results = rag_service.query("AXI protocol", n_results=1)
        print(f"✅ RAG service initialized - {len(rag_results)} documents in knowledge base")
    except Exception as e:
        print(f"⚠️  RAG service warning: {e}")
    
    try:
        # Test LLM service
        if llm_service.model:
            print("✅ LLM service initialized - Gemini API connected")
        else:
            print("⚠️  LLM service: No API key configured - using fallback mode")
    except Exception as e:
        print(f"❌ LLM service error: {e}")

# Shutdown event  
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 VLSI Design AI Tool Backend Shutting Down...")

# Favicon
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('static/favicon.ico') if os.path.exists('static/favicon.ico') else None

if __name__ == "__main__":
    import uvicorn
    
    # Development server configuration
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload in development
        log_level="info",
        access_log=True
    )
