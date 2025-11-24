"""
API routes for VLSI Design AI Tool Backend

This module contains all FastAPI route definitions for:
- RTL generation and analysis
- Testbench generation
- File upload and management
- Project management
- Health checks and system status
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Query, Path
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Optional, Dict, Any
import os
import uuid
import asyncio
from datetime import datetime

from .models import (
    GenerateRequest,
    RTLResponse,
    TestbenchRequest,
    TestbenchResponse,
    FileUploadResponse,
    ProjectCreateRequest,
    ProjectResponse,
    HealthResponse,
    ErrorResponse,
    AnalysisRequest,
    AnalysisResponse,
    SearchResponse,
    ProjectListResponse,
    ProjectFilesResponse,
    BatchGenerateRequest,
    BatchGenerateResponse,
    APIInfoResponse,
    OptimizationTarget,
    RTLanguage,
    ServiceStatus
)

from app.services import (
    rtl_generator,
    vip_generator,
    file_service,
    rag_service,
    get_service_status,
    check_all_services_health,
    app_state
)

from app.utils import (
    FileParser,
    TextProcessor,
    CodeFormatter,
    SpecificationValidator,
    generate_module_name,
    validate_verilog_syntax,
    calculate_pp_metrics,
    performance_timer
)

# Create main API router
router = APIRouter()

# In-memory storage for background tasks (in production, use Redis or database)
background_tasks: Dict[str, Dict[str, Any]] = {}

# RTL Generation Endpoints
@router.post(
    "/generate-rtl",
    response_model=RTLResponse,
    summary="Generate RTL from Specification",
    description="""
Generate optimized RTL code from natural language specification.

This endpoint uses LLM with RAG to convert design specifications into
PPA-optimized Verilog/VHDL code with proper validation.
    """,
    tags=["RTL Generation"]
)
async def generate_rtl(request: GenerateRequest):
    """
    Generate RTL code from natural language specification.
    
    - **spec_text**: Design specification in natural language
    - **requirements**: Structured design constraints and requirements
    - **optimization_target**: Power, Performance, Area, or Balanced optimization
    - **language**: Target RTL language (Verilog, VHDL, SystemVerilog)
    - **include_testbench**: Whether to generate testbench (handled separately)
    
    Returns generated RTL code with validation results and PPA metrics.
    """
    try:
        app_state.increment_requests()
        
        with performance_timer("RTL Generation"):
            # Generate RTL using the RTL generator service
            result = await rtl_generator.generate_from_spec(
                spec_text=request.spec_text,
                requirements=request.requirements
            )
            
            # Add PPA metrics
            ppa_metrics = calculate_pp_metrics(result["code"])
            result["ppa_metrics"] = ppa_metrics
            
            # Add generation metadata
            result["language"] = request.language
            result["optimization_target"] = request.optimization_target
            result["generation_time"] = performance_timer.duration if hasattr(performance_timer, 'duration') else 0
            
            # Save generated RTL to file
            if result["code"]:
                await file_service.save_generated_rtl(
                    rtl_code=result["code"],
                    module_name=result["module_name"],
                    metadata={
                        "specification": request.spec_text[:500] + "..." if len(request.spec_text) > 500 else request.spec_text,
                        "requirements": request.requirements,
                        "optimization_target": request.optimization_target,
                        "generation_time": result["generation_time"]
                    }
                )
            
            app_state.increment_rtl()
        
        return RTLResponse(**result)
        
    except Exception as e:
        app_state.increment_errors()
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="GENERATION_ERROR",
                message=f"RTL generation failed: {str(e)}",
                suggestion="Please check your specification and try again. Ensure the specification includes clear interface definitions and functional requirements."
            ).dict()
        )

@router.post(
    "/generate-testbench",
    response_model=TestbenchResponse,
    summary="Generate Testbench for RTL",
    description="""
Generate verification testbench for RTL code.

Creates comprehensive testbenches with test scenarios, assertions,
and coverage points for the provided RTL module.
    """,
    tags=["Verification"]
)
async def generate_testbench(request: TestbenchRequest):
    """
    Generate testbench for RTL code.
    
    - **rtl_code**: RTL code for which to generate testbench
    - **module_name**: Name of the module under test
    - **test_scenarios**: Specific test scenarios to include
    - **verification_methodology**: UVM, OVM, or basic testbench
    
    Returns generated testbench code with implemented scenarios.
    """
    try:
        app_state.increment_requests()
        
        with performance_timer("Testbench Generation"):
            # Generate testbench using VIP generator service
            result = await vip_generator.generate_testbench(
                rtl_code=request.rtl_code,
                module_name=request.module_name
            )
            
            # Add test scenarios and metadata
            result["test_scenarios"] = request.test_scenarios or ["basic functionality", "reset sequence", "error conditions"]
            result["generation_time"] = performance_timer.duration if hasattr(performance_timer, 'duration') else 0
            
            # Save testbench to file
            if result["testbench_code"]:
                await file_service.save_testbench(
                    testbench_code=result["testbench_code"],
                    module_name=request.module_name
                )
            
            app_state.increment_testbenches()
        
        return TestbenchResponse(**result)
        
    except Exception as e:
        app_state.increment_errors()
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="TESTBENCH_GENERATION_ERROR",
                message=f"Testbench generation failed: {str(e)}",
                suggestion="Please ensure the RTL code is valid and includes proper module declaration."
            ).dict()
        )

# File Management Endpoints
@router.post(
    "/upload-spec",
    response_model=FileUploadResponse,
    summary="Upload Specification File",
    description="""
Upload and parse design specification file.

Supports multiple file formats including TXT, MD, YAML, JSON.
Automatically extracts interfaces, protocols, and parameters.
    """,
    tags=["File Management"]
)
async def upload_specification(
    file: UploadFile = File(..., description="Specification file to upload"),
    project_id: Optional[str] = Query(None, description="Optional project ID for organization")
):
    """
    Upload and parse specification file.
    
    Supported formats: .txt, .md, .yaml, .yml, .json, .pdf, .doc, .docx
    
    Returns parsed specification data with extracted interfaces and parameters.
    """
    try:
        app_state.increment_requests()
        
        # Validate file type
        allowed_extensions = {'.txt', '.md', '.yaml', '.yml', '.json', '.pdf', '.doc', '.docx'}
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponse(
                    error="INVALID_FILE_TYPE",
                    message=f"File type {file_extension} not supported",
                    suggestion=f"Please upload one of: {', '.join(allowed_extensions)}"
                ).dict()
            )
        
        # Save uploaded file
        file_metadata = await file_service.save_uploaded_file(file, project_id)
        
        # Read and parse file content
        file_content = await file_service.read_file_content(file_metadata["file_path"])
        
        # Parse specification
        parsed_data = FileParser.parse_specification(file_content, file_extension)
        
        # Add complexity analysis
        complexity = TextProcessor.estimate_complexity(file_content)
        parsed_data["complexity_analysis"] = complexity
        
        # Validate specification structure
        validation = SpecificationValidator.validate_specification_structure(parsed_data)
        parsed_data["validation"] = validation
        
        response_data = {
            **file_metadata,
            "parsed_data": parsed_data
        }
        
        return FileUploadResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        app_state.increment_errors()
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="FILE_PROCESSING_ERROR",
                message=f"File processing failed: {str(e)}",
                suggestion="Please ensure the file is not corrupted and try again."
            ).dict()
        )

# Project Management Endpoints
@router.post(
    "/projects",
    response_model=ProjectResponse,
    summary="Create Design Project",
    description="""
Create a new VLSI design project.

Sets up organized directory structure for specifications, RTL,
testbenches, constraints, and reports.
    """,
    tags=["Project Management"]
)
async def create_project(request: ProjectCreateRequest):
    """
    Create a new VLSI design project.
    
    - **name**: Project name
    - **description**: Project description
    - **technology_node**: Target technology node
    - **constraints**: Design constraints
    
    Returns project information with directory structure.
    """
    try:
        app_state.increment_requests()
        
        # Create project structure
        project_info = await file_service.create_project(
            project_name=request.name,
            description=request.description or ""
        )
        
        # Add additional project metadata
        project_info.update({
            "technology_node": request.technology_node,
            "constraints": request.constraints or {},
            "metadata": request.metadata or {},
            "updated_at": project_info["created_at"],  # Same as created for new project
            "file_count": {},
            "total_files": 0,
            "total_size": 0
        })
        
        return ProjectResponse(**project_info)
        
    except Exception as e:
        app_state.increment_errors()
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="PROJECT_CREATION_ERROR",
                message=f"Project creation failed: {str(e)}",
                suggestion="Please check the project name and try again. Ensure the name contains only alphanumeric characters, spaces, hyphens, or underscores."
            ).dict()
        )

@router.get(
    "/projects",
    response_model=ProjectListResponse,
    summary="List Projects",
    description="Get list of all design projects with basic information.",
    tags=["Project Management"]
)
async def list_projects(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Page size")
):
    """
    List all design projects.
    
    Returns paginated list of projects with basic information.
    """
    try:
        # This would typically query a database
        # For now, return empty list as we're using file-based storage
        projects = []
        total_projects = 0
        
        return ProjectListResponse(
            projects=projects,
            total_projects=total_projects,
            page=page,
            page_size=page_size,
            total_pages=max(1, (total_projects + page_size - 1) // page_size)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="PROJECT_LIST_ERROR",
                message=f"Failed to list projects: {str(e)}"
            ).dict()
        )

@router.get(
    "/projects/{project_id}/files",
    response_model=ProjectFilesResponse,
    summary="Get Project Files",
    description="Get all files in a project organized by category.",
    tags=["Project Management"]
)
async def get_project_files(
    project_id: str = Path(..., description="Project ID")
):
    """
    Get all files in a project.
    
    Returns files organized by category (specifications, RTL, testbenches, etc.)
    with detailed file information.
    """
    try:
        project_files = await file_service.get_project_files(project_id)
        
        # Calculate statistics
        total_files = sum(len(files) for files in project_files.values())
        total_size = 0  # Would calculate from actual files
        
        file_type_breakdown = {category: len(files) for category, files in project_files.items()}
        
        return ProjectFilesResponse(
            project_id=project_id,
            files=project_files,
            total_files=total_files,
            total_size=total_size,
            file_type_breakdown=file_type_breakdown
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error="PROJECT_NOT_FOUND",
                message=str(e)
            ).dict()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="PROJECT_FILES_ERROR",
                message=f"Failed to get project files: {str(e)}"
            ).dict()
        )

# Analysis and Search Endpoints
@router.post(
    "/analyze-rtl",
    response_model=AnalysisResponse,
    summary="Analyze RTL Code",
    description="Perform static analysis on RTL code including syntax checking, complexity analysis, and PPA estimation.",
    tags=["Analysis"]
)
async def analyze_rtl(request: AnalysisRequest):
    """
    Analyze RTL code.
    
    - **rtl_code**: RTL code to analyze
    - **analysis_type**: Types of analysis to perform
    
    Returns comprehensive analysis results and recommendations.
    """
    try:
        app_state.increment_requests()
        
        analysis_id = str(uuid.uuid4())
        results = {}
        
        # Perform requested analyses
        for analysis_type in request.analysis_type:
            if analysis_type == "syntax":
                results["syntax"] = validate_verilog_syntax(request.rtl_code)
            elif analysis_type == "complexity":
                results["complexity"] = CodeFormatter.count_code_metrics(request.rtl_code)
            elif analysis_type == "ppa_estimation":
                results["ppa_estimation"] = calculate_pp_metrics(request.rtl_code)
            elif analysis_type == "port_analysis":
                results["port_analysis"] = CodeFormatter.extract_module_ports(request.rtl_code)
        
        # Generate summary and recommendations
        summary = {
            "total_analyses": len(request.analysis_type),
            "completed_analyses": list(results.keys()),
            "overall_quality": "good"  # Would calculate based on results
        }
        
        recommendations = []
        if "syntax" in results and not results["syntax"]["valid"]:
            recommendations.append("Fix syntax issues in RTL code")
        if "complexity" in results and results["complexity"]["always_blocks"] > 10:
            recommendations.append("Consider simplifying design - high number of always blocks")
        
        return AnalysisResponse(
            analysis_id=analysis_id,
            analysis_type=request.analysis_type,
            results=results,
            summary=summary,
            recommendations=recommendations,
            analysis_time=0.5,  # Would calculate actual time
            timestamp=datetime.now()
        )
        
    except Exception as e:
        app_state.increment_errors()
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="ANALYSIS_ERROR",
                message=f"RTL analysis failed: {str(e)}"
            ).dict()
        )

@router.get(
    "/search",
    response_model=SearchResponse,
    summary="Search Knowledge Base",
    description="Search the RAG knowledge base for relevant VLSI design patterns, protocols, and examples.",
    tags=["Analysis"]
)
async def search_knowledge_base(
    query: str = Query(..., description="Search query"),
    n_results: int = Query(5, ge=1, le=20, description="Number of results to return")
):
    """
    Search knowledge base.
    
    Returns relevant documents from the VLSI knowledge base
    including protocols, design patterns, and reference implementations.
    """
    try:
        app_state.increment_requests()
        
        with performance_timer("Knowledge Base Search"):
            results = rag_service.query(query, n_results=n_results)
        
        return SearchResponse(
            query=query,
            results=results,
            total_results=len(results),
            search_time=performance_timer.duration if hasattr(performance_timer, 'duration') else 0
        )
        
    except Exception as e:
        app_state.increment_errors()
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="SEARCH_ERROR",
                message=f"Knowledge base search failed: {str(e)}"
            ).dict()
        )

# Batch Operations
@router.post(
    "/batch/generate-rtl",
    response_model=BatchGenerateResponse,
    summary="Batch RTL Generation",
    description="Generate RTL for multiple specifications in a single request.",
    tags=["Batch Operations"]
)
async def batch_generate_rtl(request: BatchGenerateRequest):
    """
    Batch generate RTL for multiple specifications.
    
    - **specifications**: List of generation requests
    - **parallel**: Whether to process in parallel
    
    Returns results for all specifications with batch statistics.
    """
    try:
        app_state.increment_requests()
        
        batch_id = str(uuid.uuid4())
        results = []
        successful = 0
        failed = 0
        
        start_time = datetime.now()
        
        # Process specifications
        for spec_request in request.specifications:
            try:
                result = await rtl_generator.generate_from_spec(
                    spec_text=spec_request.spec_text,
                    requirements=spec_request.requirements
                )
                
                # Convert to RTLResponse
                rtl_response = RTLResponse(
                    **result,
                    language=spec_request.language,
                    optimization_target=spec_request.optimization_target,
                    generation_time=0.5  # Would calculate actual time
                )
                
                results.append(rtl_response)
                successful += 1
                app_state.increment_rtl()
                
            except Exception as e:
                failed += 1
                app_state.increment_errors()
                # Continue with other specifications even if one fails
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return BatchGenerateResponse(
            results=results,
            total_processed=len(request.specifications),
            successful=successful,
            failed=failed,
            batch_id=batch_id,
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="BATCH_GENERATION_ERROR",
                message=f"Batch generation failed: {str(e)}"
            ).dict()
        )

# System Endpoints
@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check system health and service status.",
    tags=["System"]
)
async def health_check():
    """
    Health check endpoint.
    
    Returns comprehensive health status of all services
    and system information.
    """
    try:
        # Check service health
        services_health = await check_all_services_health()
        
        # Get service status
        service_status = get_service_status()
        
        # Prepare service health information
        services = {}
        for service_name, health_info in services_health["services"].items():
            services[service_name] = {
                "status": health_info["status"],
                "message": health_info["message"],
                "last_check": datetime.now(),
                "details": health_info
            }
        
        # Determine overall status
        overall_status = ServiceStatus.HEALTHY
        if any(health["status"] == "unhealthy" for health in services_health["services"].values()):
            overall_status = ServiceStatus.UNHEALTHY
        elif any(health["status"] == "degraded" for health in services_health["services"].values()):
            overall_status = ServiceStatus.DEGRADED
        
        # Get system statistics
        stats = app_state.get_stats()
        
        return HealthResponse(
            status=overall_status,
            version="1.0.0",
            timestamp=datetime.now(),
            services=services,
            system_info=services_health.get("system_info", {}),
            uptime_seconds=stats["uptime_seconds"],
            total_requests=stats["requests_processed"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="HEALTH_CHECK_ERROR",
                message=f"Health check failed: {str(e)}",
                suggestion="The system may be experiencing issues. Please try again later."
            ).dict()
        )

@router.get(
    "/info",
    response_model=APIInfoResponse,
    summary="API Information",
    description="Get detailed API information, features, and configuration.",
    tags=["System"]
)
async def api_info():
    """
    API information endpoint.
    
    Returns comprehensive information about the API,
    available features, and system configuration.
    """
    try:
        from app import get_app_info
        from app.core.config import settings
        
        app_info = get_app_info()
        stats = app_state.get_stats()
        
        # Get service configuration
        service_config = settings.get_service_config()
        
        return APIInfoResponse(
            name=app_info["name"],
            version=app_info["version"],
            description=app_info["description"],
            features=app_info["features"],
            supported_languages=["Verilog", "VHDL", "SystemVerilog"],
            supported_protocols=app_info["supported_protocols"],
            service_config={
                "llm_provider": service_config["llm"]["provider"],
                "llm_model": service_config["llm"]["model"],
                "rag_enabled": service_config["rag"]["enabled"],
                "max_file_size": service_config["file_handling"]["max_file_size"],
                "allowed_extensions": service_config["file_handling"]["allowed_extensions"]
            },
            endpoints=[
                {
                    "path": "/api/v1/generate-rtl",
                    "methods": ["POST"],
                    "description": "Generate RTL from specification"
                },
                {
                    "path": "/api/v1/generate-testbench", 
                    "methods": ["POST"],
                    "description": "Generate testbench for RTL"
                },
                {
                    "path": "/api/v1/upload-spec",
                    "methods": ["POST"],
                    "description": "Upload specification file"
                },
                # ... more endpoints
            ],
            uptime=stats["uptime_seconds"],
            total_requests=stats["requests_processed"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="API_INFO_ERROR",
                message=f"Failed to get API information: {str(e)}"
            ).dict()
        )

@router.get(
    "/stats",
    summary="API Statistics",
    description="Get detailed API usage statistics and performance metrics.",
    tags=["System"]
)
async def api_statistics():
    """
    API statistics endpoint.
    
    Returns detailed usage statistics, performance metrics,
    and generation statistics.
    """
    try:
        stats = app_state.get_stats()
        
        # Add additional statistics
        additional_stats = {
            "active_requests": 0,  # Would track in production
            "average_response_time": 0,  # Would calculate
            "error_rate": stats["errors_encountered"] / max(1, stats["requests_processed"]),
            "generation_success_rate": stats["rtl_generated"] / max(1, stats["requests_processed"]),
            "system_load": "normal"  # Would calculate
        }
        
        return {
            "timestamp": datetime.now(),
            "requests": stats,
            "performance": additional_stats,
            "services": get_service_status()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="STATS_ERROR",
                message=f"Failed to get statistics: {str(e)}"
            ).dict()
        )

# Utility Endpoints
@router.post(
    "/utils/validate-spec",
    summary="Validate Specification",
    description="Validate specification structure and completeness without generating RTL.",
    tags=["Utilities"]
)
async def validate_specification(spec_text: str = Query(..., description="Specification text to validate")):
    """
    Validate specification structure.
    
    Returns validation results with issues and recommendations.
    """
    try:
        # Parse and validate specification
        parsed_data = FileParser.parse_specification(spec_text, "txt")
        validation = SpecificationValidator.validate_specification_structure(parsed_data)
        
        # Add complexity analysis
        complexity = TextProcessor.estimate_complexity(spec_text)
        
        return {
            "validation": validation,
            "complexity": complexity,
            "parsed_data": {
                "interfaces": parsed_data["interfaces"],
                "protocols": parsed_data["protocols"],
                "parameters": parsed_data["parameters"]
            },
            "recommendations": [
                "Ensure all interfaces are clearly defined",
                "Specify clock frequency and timing requirements",
                "Include power and area constraints if applicable"
            ] if validation["score"] < 80 else []
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="VALIDATION_ERROR",
                message=f"Specification validation failed: {str(e)}"
            ).dict()
        )

@router.get(
    "/utils/suggest-module-name",
    summary="Suggest Module Name",
    description="Generate meaningful module name from specification text.",
    tags=["Utilities"]
)
async def suggest_module_name(spec_text: str = Query(..., description="Specification text")):
    """
    Suggest module name from specification.
    
    Returns generated module name based on specification content.
    """
    try:
        module_name = generate_module_name(spec_text)
        
        return {
            "suggested_name": module_name,
            "alternative_names": [
                module_name.replace("module_", "design_"),
                module_name.replace("module_", "ip_"),
                module_name + "_top"
            ],
            "keywords": TextProcessor.extract_keywords(spec_text)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="NAME_GENERATION_ERROR",
                message=f"Module name generation failed: {str(e)}"
            ).dict()
        )

# File Download Endpoints
@router.get(
    "/download/{file_type}/{filename}",
    summary="Download Generated File",
    description="Download generated RTL, testbench, or report files.",
    tags=["File Management"]
)
async def download_file(
    file_type: str = Path(..., description="Type of file to download"),
    filename: str = Path(..., description="Filename to download")
):
    """
    Download generated file.
    
    Supports downloading RTL files, testbenches, and reports.
    """
    try:
        # Construct file path based on type and filename
        if file_type == "rtl":
            file_path = f"uploads/rtl/{filename}"
        elif file_type == "testbench":
            file_path = f"uploads/testbenches/{filename}"
        elif file_type == "report":
            file_path = f"uploads/reports/{filename}"
        else:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponse(
                    error="INVALID_FILE_TYPE",
                    message=f"Invalid file type: {file_type}",
                    suggestion="Supported types: rtl, testbench, report"
                ).dict()
            )
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail=ErrorResponse(
                    error="FILE_NOT_FOUND",
                    message=f"File not found: {filename}"
                ).dict()
            )
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="DOWNLOAD_ERROR",
                message=f"File download failed: {str(e)}"
            ).dict()
        )

print("✅ VLSI Design AI Tool API Routes loaded successfully!")
