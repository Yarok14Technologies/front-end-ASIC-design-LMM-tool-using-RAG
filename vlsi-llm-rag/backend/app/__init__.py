"""
VLSI Design AI Tool Backend

A comprehensive automated front-end VLSI design tool using LLM RAG pipeline.
Transforms high-level design specifications into PPA-optimized, synthesizable RTL IP blocks.

Features:
- Specification-to-RTL generation using LLM with RAG
- PPA-optimized Verilog/VHDL code generation
- Testbench and verification IP generation
- Iterative verification and bug correction
- Project management and file organization
- Knowledge base with VLSI design patterns and protocols
"""

__version__ = "1.0.0"
__author__ = "VLSI Design AI Team"
__email__ = "contact@vlsiai-tool.com"

import os
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from .core.config import settings
from .services import (
    # Service instances
    rag_service,
    llm_service,
    rtl_generator,
    vip_generator,
    file_service,
    # Service classes
    RAGService,
    LLMService,
    RTLGenerator,
    VIPGenerator,
    FileService,
    # Service utilities
    initialize_services,
    get_service_status,
    is_service_available,
    get_available_services,
    get_service_info,
    check_all_services_health,
    SERVICES_STATUS,
    SERVICE_DESCRIPTIONS
)

# Export main components for easy access
__all__ = [
    # Configuration
    "settings",
    
    # Service instances
    "rag_service",
    "llm_service", 
    "rtl_generator",
    "vip_generator",
    "file_service",
    
    # Service classes
    "RAGService",
    "LLMService", 
    "RTLGenerator",
    "VIPGenerator",
    "FileService",
    
    # Service utilities
    "initialize_services",
    "get_service_status", 
    "is_service_available",
    "get_available_services",
    "get_service_info",
    "check_all_services_health",
    "SERVICES_STATUS",
    "SERVICE_DESCRIPTIONS",
    
    # API components
    "api",
    "core",
    "services", 
    "utils"
]

# Application metadata
APP_METADATA = {
    "name": "VLSI Design AI Tool",
    "version": __version__,
    "description": "Automated Front-End VLSI Design using LLM RAG",
    "author": __author__,
    "features": [
        "Specification-to-RTL Generation",
        "PPA-Optimized Code Generation", 
        "Testbench and VIP Generation",
        "RAG-Enhanced Knowledge Base",
        "Iterative Verification Loop",
        "Project Management",
        "Multi-Format Specification Support"
    ],
    "supported_formats": {
        "specification": [".txt", ".md", ".yaml", ".yml", ".json"],
        "rtl": [".v", ".sv", ".vhd", ".vhdl"],
        "documentation": [".pdf", ".doc", ".docx"]
    },
    "supported_protocols": [
        "AMBA AXI", "AMBA AHB", "AMBA APB", 
        "UART", "SPI", "I2C", "PCIe", "Ethernet"
    ]
}

def get_app_info() -> dict:
    """
    Get comprehensive application information
    
    Returns:
        dict: Application metadata and configuration
    """
    return {
        **APP_METADATA,
        "configuration": {
            "upload_directory": settings.UPLOAD_DIR,
            "knowledge_base_path": settings.CHROMA_DB_PATH,
            "max_file_size": f"{settings.MAX_FILE_SIZE / (1024 * 1024)} MB",
            "llm_configured": bool(settings.GEMINI_API_KEY),
            "rag_chunk_size": settings.CHUNK_SIZE,
            "rag_chunk_overlap": settings.CHUNK_OVERLAP
        },
        "services": get_service_status()
    }

def setup_application():
    """
    Initialize the application setup
    
    This function should be called during application startup
    to ensure all components are properly configured.
    """
    print("🚀 Initializing VLSI Design AI Tool Backend...")
    print(f"📁 Upload Directory: {settings.UPLOAD_DIR}")
    print(f"📚 Knowledge Base: {settings.CHROMA_DB_PATH}")
    print(f"🔑 LLM Configured: {bool(settings.GEMINI_API_KEY)}")
    
    # Initialize services
    services_status = initialize_services()
    
    # Print service status
    available_services = get_available_services()
    unavailable_services = get_unavailable_services()
    
    print(f"✅ Available Services: {', '.join(available_services) if available_services else 'None'}")
    if unavailable_services:
        print(f"⚠️  Unavailable Services: {', '.join(unavailable_services)}")
    
    print("🎯 VLSI Design AI Tool Backend Ready!")

# Application initialization flags
_initialized = False

def ensure_initialized():
    """
    Ensure the application is properly initialized
    
    This function can be called by modules that need to ensure
    the application setup has been completed.
    """
    global _initialized
    if not _initialized:
        setup_application()
        _initialized = True

# Import API components after initialization to avoid circular imports
try:
    from .api import routes, models
    from .utils import file_parser, prompts
    
    # Add to exports
    __all__.extend([
        "routes",
        "models", 
        "file_parser",
        "prompts"
    ])
    
except ImportError as e:
    print(f"⚠️  Some components could not be imported: {e}")

# Performance monitoring
import time
from contextlib import contextmanager

@contextmanager
def performance_timer(operation_name: str):
    """
    Context manager for performance monitoring
    
    Args:
        operation_name: Name of the operation being timed
        
    Example:
        with performance_timer("RTL Generation"):
            result = await rtl_generator.generate_from_spec(spec_text)
    """
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        duration = end_time - start_time
        print(f"⏱️  {operation_name} completed in {duration:.2f} seconds")

# Error handling utilities
class VLSIDesignError(Exception):
    """Base exception for VLSI Design AI Tool"""
    pass

class RTLGenerationError(VLSIDesignError):
    """Exception raised during RTL generation"""
    pass

class SpecificationParseError(VLSIDesignError):
    """Exception raised during specification parsing"""
    pass

class ServiceUnavailableError(VLSIDesignError):
    """Exception raised when a required service is unavailable"""
    pass

def validate_specification_content(content: str) -> bool:
    """
    Basic validation of specification content
    
    Args:
        content: Specification text content
        
    Returns:
        bool: True if content appears valid
    """
    if not content or len(content.strip()) < 10:
        return False
    
    # Check for common VLSI design keywords
    vlsi_keywords = [
        'module', 'interface', 'protocol', 'clock', 'reset', 
        'register', 'signal', 'input', 'output', 'frequency',
        'AXI', 'AHB', 'APB', 'UART', 'SPI', 'I2C'
    ]
    
    content_lower = content.lower()
    keyword_matches = sum(1 for keyword in vlsi_keywords if keyword.lower() in content_lower)
    
    # Consider valid if at least 2 VLSI keywords are found
    return keyword_matches >= 2

# Application lifecycle management
class ApplicationState:
    """Manage application state and lifecycle"""
    
    def __init__(self):
        self.start_time = time.time()
        self.requests_processed = 0
        self.rtl_generated = 0
        self.testbenches_generated = 0
        self.errors_encountered = 0
    
    def increment_requests(self):
        """Increment request counter"""
        self.requests_processed += 1
    
    def increment_rtl(self):
        """Increment RTL generation counter"""
        self.rtl_generated += 1
    
    def increment_testbenches(self):
        """Increment testbench generation counter"""
        self.testbenches_generated += 1
    
    def increment_errors(self):
        """Increment error counter"""
        self.errors_encountered += 1
    
    def get_stats(self) -> dict:
        """Get application statistics"""
        current_time = time.time()
        uptime = current_time - self.start_time
        
        return {
            "uptime_seconds": uptime,
            "uptime_human": f"{uptime / 3600:.2f} hours",
            "requests_processed": self.requests_processed,
            "rtl_generated": self.rtl_generated,
            "testbenches_generated": self.testbenches_generated,
            "errors_encountered": self.errors_encountered,
            "request_rate": self.requests_processed / uptime if uptime > 0 else 0
        }

# Global application state
app_state = ApplicationState()

# Initialize application on module import
try:
    ensure_initialized()
except Exception as e:
    print(f"❌ Application initialization failed: {e}")
    raise

print(f"✅ VLSI Design AI Tool Backend v{__version__} initialized successfully!")
