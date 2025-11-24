from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class GenerateRequest(BaseModel):
    spec_text: str
    requirements: Optional[Dict[str, Any]] = None
    optimization_target: str = "balanced"  # power, performance, area, balanced

class RTLResponse(BaseModel):
    module_name: str
    code: str
    explanation: str
    rag_context: List[Dict[str, Any]]
    validation_result: Dict[str, Any]

class TestbenchRequest(BaseModel):
    rtl_code: str
    module_name: str

class TestbenchResponse(BaseModel):
    testbench_code: str
    module_name: str

class FileUploadResponse(BaseModel):
    filename: str
    content_type: str
    parsed_data: Dict[str, Any]
