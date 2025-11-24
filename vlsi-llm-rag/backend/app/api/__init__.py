"""
API module for VLSI Design AI Tool Backend

This module contains all API routes, models, and handlers for the FastAPI application:
- RTL generation endpoints
- File upload and management endpoints
- Testbench generation endpoints
- Project management endpoints
- Health and status endpoints
"""

from fastapi import APIRouter, FastAPI
from typing import Dict, List, Any, Optional
import importlib
import inspect

# API module metadata
__version__ = "1.0.0"
__author__ = "VLSI Design AI Team"

# Import API components
from . import routes, models
from .routes import router as api_router
from .models import (
    GenerateRequest,
    RTLResponse,
    TestbenchRequest,
    TestbenchResponse,
    FileUploadResponse,
    ProjectCreateRequest,
    ProjectResponse,
    HealthResponse,
    ErrorResponse
)

# Export main components
__all__ = [
    # Routers
    "api_router",
    "routes",
    
    # Models
    "models",
    "GenerateRequest",
    "RTLResponse", 
    "TestbenchRequest",
    "TestbenchResponse",
    "FileUploadResponse",
    "ProjectCreateRequest",
    "ProjectResponse",
    "HealthResponse",
    "ErrorResponse",
    
    # API utilities
    "create_api_router",
    "register_routes",
    "get_api_info",
    "API_INFO"
]

# API information and metadata
API_INFO = {
    "title": "VLSI Design AI Tool API",
    "version": __version__,
    "description": """
🚀 Automated Front-End VLSI Design API

This API provides endpoints for automated RTL generation, testbench creation,
and VLSI design management using LLM RAG technology.

## Key Features

- **Specification-to-RTL Generation**: Convert natural language specs to optimized Verilog/VHDL
- **PPA-Optimized Code**: Generate Power-Performance-Area optimized RTL
- **Testbench Generation**: Automated verification testbench creation
- **RAG-Enhanced Knowledge**: Context-aware generation using VLSI design patterns
- **Project Management**: Organize designs and related files
- **File Processing**: Upload and parse specification documents

## Available Endpoints

- `POST /api/v1/generate-rtl` - Generate RTL from specification
- `POST /api/v1/generate-testbench` - Generate testbench for RTL
- `POST /api/v1/upload-spec` - Upload and parse specification file
- `POST /api/v1/projects` - Create new design project
- `GET /api/v1/health` - Health check and service status
- `GET /api/v1/info` - API information and configuration
    """,
    "contact": {
        "name": "VLSI Design AI Team",
        "email": "contact@vlsiai-tool.com",
    },
    "license_info": {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
}

# API route configurations
ROUTE_CONFIGS = {
    "generate_rtl": {
        "path": "/generate-rtl",
        "methods": ["POST"],
        "summary": "Generate RTL from Specification",
        "description": "Convert natural language specification to optimized RTL code",
        "tags": ["RTL Generation"],
        "response_model": "RTLResponse"
    },
    "generate_testbench": {
        "path": "/generate-testbench", 
        "methods": ["POST"],
        "summary": "Generate Testbench for RTL",
        "description": "Create verification testbench for generated RTL code",
        "tags": ["Verification"],
        "response_model": "TestbenchResponse"
    },
    "upload_spec": {
        "path": "/upload-spec",
        "methods": ["POST"],
        "summary": "Upload Specification File",
        "description": "Upload and parse design specification document",
        "tags": ["File Management"],
        "response_model": "FileUploadResponse"
    },
    "create_project": {
        "path": "/projects",
        "methods": ["POST"],
        "summary": "Create Design Project",
        "description": "Create a new VLSI design project with organized structure",
        "tags": ["Project Management"],
        "response_model": "ProjectResponse"
    },
    "health_check": {
        "path": "/health",
        "methods": ["GET"],
        "summary": "Health Check",
        "description": "Check API health and service status",
        "tags": ["System"],
        "response_model": "HealthResponse"
    },
    "api_info": {
        "path": "/info",
        "methods": ["GET"],
        "summary": "API Information",
        "description": "Get API information, features, and configuration",
        "tags": ["System"],
        "response_model": "dict"
    }
}

# API tags metadata
API_TAGS = [
    {
        "name": "RTL Generation",
        "description": "Endpoints for generating RTL code from specifications"
    },
    {
        "name": "Verification", 
        "description": "Testbench generation and verification endpoints"
    },
    {
        "name": "File Management",
        "description": "File upload, parsing, and management endpoints"
    },
    {
        "name": "Project Management",
        "description": "Design project organization and management"
    },
    {
        "name": "System",
        "description": "Health checks, status, and system information"
    }
]

def create_api_router(prefix: str = "/api/v1") -> APIRouter:
    """
    Create and configure the main API router
    
    Args:
        prefix: API route prefix
        
    Returns:
        Configured APIRouter instance
    """
    router = APIRouter(prefix=prefix)
    
    # Import and include route modules
    from .routes import router as main_router
    router.include_router(main_router)
    
    return router

def register_routes(app: FastAPI, prefix: str = "/api/v1"):
    """
    Register all API routes with the FastAPI application
    
    Args:
        app: FastAPI application instance
        prefix: API route prefix
    """
    router = create_api_router(prefix)
    app.include_router(router)
    
    # Add API tags metadata
    for tag in API_TAGS:
        if not any(existing_tag["name"] == tag["name"] for existing_tag in app.openapi_tags or []):
            if not hasattr(app, 'openapi_tags'):
                app.openapi_tags = []
            app.openapi_tags.append(tag)

def get_api_info() -> Dict[str, Any]:
    """
    Get comprehensive API information
    
    Returns:
        Dictionary with API metadata and route information
    """
    return {
        **API_INFO,
        "routes": ROUTE_CONFIGS,
        "tags": API_TAGS,
        "version": __version__,
        "endpoints_count": len(ROUTE_CONFIGS),
        "supported_operations": ["generate_rtl", "generate_testbench", "upload_spec", "project_management"]
    }

def get_route_documentation() -> Dict[str, Any]:
    """
    Get detailed route documentation for API reference
    
    Returns:
        Dictionary with route documentation
    """
    documentation = {}
    
    for route_name, config in ROUTE_CONFIGS.items():
        documentation[route_name] = {
            "path": f"/api/v1{config['path']}",
            "methods": config["methods"],
            "summary": config["summary"],
            "description": config["description"],
            "tags": config["tags"],
            "request_body": get_request_body_info(route_name),
            "responses": get_response_info(route_name)
        }
    
    return documentation

def get_request_body_info(route_name: str) -> Optional[Dict[str, Any]]:
    """
    Get request body information for a specific route
    
    Args:
        route_name: Name of the route
        
    Returns:
        Request body information or None
    """
    request_models = {
        "generate_rtl": {
            "model": "GenerateRequest",
            "description": "RTL generation request with specification and requirements",
            "required": True,
            "content_type": "application/json"
        },
        "generate_testbench": {
            "model": "TestbenchRequest", 
            "description": "Testbench generation request with RTL code",
            "required": True,
            "content_type": "application/json"
        },
        "upload_spec": {
            "model": "File upload",
            "description": "Specification file upload",
            "required": True,
            "content_type": "multipart/form-data"
        },
        "create_project": {
            "model": "ProjectCreateRequest",
            "description": "Project creation request with name and description",
            "required": True,
            "content_type": "application/json"
        }
    }
    
    return request_models.get(route_name)

def get_response_info(route_name: str) -> Dict[str, Any]:
    """
    Get response information for a specific route
    
    Args:
        route_name: Name of the route
        
    Returns:
        Response information dictionary
    """
    base_responses = {
        "200": {
            "description": "Successful operation"
        },
        "400": {
            "description": "Bad request - invalid input parameters",
            "model": "ErrorResponse"
        },
        "422": {
            "description": "Validation error - request data validation failed", 
            "model": "ErrorResponse"
        },
        "500": {
            "description": "Internal server error",
            "model": "ErrorResponse"
        }
    }
    
    # Add route-specific success response
    success_responses = {
        "generate_rtl": {
            "description": "RTL generated successfully",
            "model": "RTLResponse"
        },
        "generate_testbench": {
            "description": "Testbench generated successfully", 
            "model": "TestbenchResponse"
        },
        "upload_spec": {
            "description": "File uploaded and parsed successfully",
            "model": "FileUploadResponse"
        },
        "create_project": {
            "description": "Project created successfully",
            "model": "ProjectResponse"
        },
        "health_check": {
            "description": "Health status retrieved",
            "model": "HealthResponse"
        },
        "api_info": {
            "description": "API information retrieved",
            "model": "dict"
        }
    }
    
    responses = base_responses.copy()
    if route_name in success_responses:
        responses["200"] = success_responses[route_name]
    
    return responses

# API error codes and descriptions
ERROR_CODES = {
    400: {
        "code": "BAD_REQUEST",
        "description": "The request was invalid or cannot be served"
    },
    401: {
        "code": "UNAUTHORIZED", 
        "description": "Authentication is required and has failed or not been provided"
    },
    403: {
        "code": "FORBIDDEN",
        "description": "The request is understood but it has been refused or access is not allowed"
    },
    404: {
        "code": "NOT_FOUND",
        "description": "The requested resource could not be found"
    },
    422: {
        "code": "VALIDATION_ERROR",
        "description": "The request data failed validation checks"
    },
    429: {
        "code": "RATE_LIMITED",
        "description": "Too many requests - rate limiting applied"
    },
    500: {
        "code": "INTERNAL_ERROR",
        "description": "An internal server error occurred"
    },
    503: {
        "code": "SERVICE_UNAVAILABLE",
        "description": "The service is temporarily unavailable"
    }
}

def get_error_description(status_code: int) -> Dict[str, str]:
    """
    Get error code and description for HTTP status code
    
    Args:
        status_code: HTTP status code
        
    Returns:
        Dictionary with error code and description
    """
    return ERROR_CODES.get(status_code, {
        "code": "UNKNOWN_ERROR",
        "description": "An unknown error occurred"
    })

# API rate limiting configuration (for future implementation)
RATE_LIMITS = {
    "generate_rtl": {
        "requests_per_minute": 10,
        "burst_capacity": 3
    },
    "generate_testbench": {
        "requests_per_minute": 15, 
        "burst_capacity": 5
    },
    "upload_spec": {
        "requests_per_minute": 20,
        "burst_capacity": 10
    },
    "general": {
        "requests_per_minute": 60,
        "burst_capacity": 20
    }
}

def get_rate_limit_config(endpoint: str) -> Dict[str, int]:
    """
    Get rate limiting configuration for an endpoint
    
    Args:
        endpoint: Endpoint name
        
    Returns:
        Rate limiting configuration
    """
    return RATE_LIMITS.get(endpoint, RATE_LIMITS["general"])

# API version management
API_VERSIONS = {
    "v1": {
        "version": "1.0.0",
        "status": "active",
        "base_path": "/api/v1",
        "release_date": "2024-01-01",
        "endpoints": list(ROUTE_CONFIGS.keys())
    }
}

def get_api_version_info(version: str = "v1") -> Optional[Dict[str, Any]]:
    """
    Get information about a specific API version
    
    Args:
        version: API version identifier
        
    Returns:
        Version information or None if not found
    """
    return API_VERSIONS.get(version)

def get_all_api_versions() -> Dict[str, Dict[str, Any]]:
    """
    Get information about all API versions
    
    Returns:
        Dictionary of all API versions
    """
    return API_VERSIONS.copy()

# API feature flags (can be controlled via configuration)
API_FEATURES = {
    "rtl_generation": True,
    "testbench_generation": True,
    "file_upload": True,
    "project_management": True,
    "health_checks": True,
    "rate_limiting": False,  # Disabled by default
    "caching": False,        # Disabled by default
    "authentication": False  # Disabled by default
}

def is_feature_enabled(feature: str) -> bool:
    """
    Check if an API feature is enabled
    
    Args:
        feature: Feature name
        
    Returns:
        True if feature is enabled
        
    Raises:
        ValueError: If feature name is invalid
    """
    if feature not in API_FEATURES:
        raise ValueError(f"Unknown feature: {feature}. Available features: {list(API_FEATURES.keys())}")
    
    return API_FEATURES[feature]

def enable_feature(feature: str):
    """
    Enable an API feature
    
    Args:
        feature: Feature name to enable
        
    Raises:
        ValueError: If feature name is invalid
    """
    if feature not in API_FEATURES:
        raise ValueError(f"Unknown feature: {feature}")
    
    API_FEATURES[feature] = True

def disable_feature(feature: str):
    """
    Disable an API feature
    
    Args:
        feature: Feature name to disable
        
    Raises:
        ValueError: If feature name is invalid
    """
    if feature not in API_FEATURES:
        raise ValueError(f"Unknown feature: {feature}")
    
    API_FEATURES[feature] = False

# API initialization
def initialize_api():
    """
    Initialize the API module and perform setup tasks
    """
    print("🚀 Initializing VLSI Design AI Tool API...")
    print(f"📡 API Version: {__version__}")
    print(f"🔧 Available Endpoints: {len(ROUTE_CONFIGS)}")
    print(f"🏷️  API Tags: {len(API_TAGS)}")
    
    # Check if all required modules are available
    try:
        from app.services import get_service_status
        services_status = get_service_status()
        available_services = [name for name, available in services_status.items() if available]
        print(f"✅ Available Services: {', '.join(available_services)}")
    except ImportError as e:
        print(f"⚠️  Could not check service status: {e}")
    
    print("🎯 VLSI Design AI Tool API Ready!")

# Initialize API on module import
initialize_api()

print(f"✅ VLSI Design AI Tool API v{__version__} initialized successfully!")
