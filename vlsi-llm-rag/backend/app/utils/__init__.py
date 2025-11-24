"""
Utilities module for VLSI Design AI Tool Backend

This module contains utility functions and helpers used across the application:
- File parsing and specification processing
- LLM prompt templates and management
- Text processing and formatting utilities
- Validation and helper functions
"""

import os
import re
import json
import yaml
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

# Version and module info
__version__ = "1.0.0"

# Export main utilities
from .file_parser import FileParser, parse_specification, parse_requirements
from .prompts import (
    PromptManager,
    RTLCreationPrompts,
    TestbenchPrompts,
    VerificationPrompts,
    get_rtl_prompt,
    get_testbench_prompt,
    get_verification_prompt,
    DEFAULT_PROMPT_TEMPLATES
)

__all__ = [
    # File parsing
    "FileParser",
    "parse_specification", 
    "parse_requirements",
    
    # Prompt management
    "PromptManager",
    "RTLCreationPrompts",
    "TestbenchPrompts", 
    "VerificationPrompts",
    "get_rtl_prompt",
    "get_testbench_prompt",
    "get_verification_prompt",
    "DEFAULT_PROMPT_TEMPLATES",
    
    # Text processing
    "TextProcessor",
    "CodeFormatter",
    "SpecificationValidator",
    
    # Helper functions
    "generate_module_name",
    "extract_ports_from_rtl",
    "validate_verilog_syntax",
    "calculate_pp_metrics",
    "create_project_structure"
]

# Text processing utilities
class TextProcessor:
    """Text processing and normalization utilities"""
    
    @staticmethod
    def normalize_specification(text: str) -> str:
        """
        Normalize specification text by removing extra whitespace,
        standardizing formatting, and cleaning up common issues.
        
        Args:
            text: Raw specification text
            
        Returns:
            Normalized specification text
        """
        if not text:
            return ""
        
        # Remove extra whitespace and normalize line endings
        text = re.sub(r'\r\n', '\n', text)  # Windows to Unix
        text = re.sub(r'\r', '\n', text)    # Old Mac to Unix
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Multiple blank lines to one
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs to one
        
        # Remove leading/trailing whitespace from each line
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        return text.strip()
    
    @staticmethod
    def extract_keywords(text: str, min_length: int = 3) -> List[str]:
        """
        Extract meaningful keywords from specification text
        
        Args:
            text: Specification text
            min_length: Minimum keyword length
            
        Returns:
            List of extracted keywords
        """
        # Common VLSI and digital design terms
        vlsi_terms = {
            'module', 'interface', 'protocol', 'clock', 'reset', 'register',
            'signal', 'input', 'output', 'wire', 'reg', 'parameter', 'localparam',
            'always', 'assign', 'posedge', 'negedge', 'begin', 'end', 'if', 'else',
            'case', 'default', 'function', 'task', 'generate', 'for', 'while',
            'axi', 'ahb', 'apb', 'uart', 'spi', 'i2c', 'pcie', 'ethernet',
            'fsm', 'state', 'transition', 'counter', 'fifo', 'memory', 'cache',
            'synthesis', 'timing', 'area', 'power', 'performance', 'frequency',
            'synchronizer', 'arbiter', 'decoder', 'encoder', 'multiplexer', 'adder'
        }
        
        # Extract words (alphanumeric with underscores)
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', text.lower())
        
        # Filter by length and relevance
        keywords = []
        for word in words:
            if (len(word) >= min_length and 
                word not in {'the', 'and', 'for', 'with', 'this', 'that'} and
                (word in vlsi_terms or word.endswith(('tor', 'ter', 'der', 'ser')))):
                keywords.append(word)
        
        return list(set(keywords))  # Remove duplicates
    
    @staticmethod
    def split_into_sections(text: str) -> Dict[str, str]:
        """
        Split specification text into logical sections
        
        Args:
            text: Specification text
            
        Returns:
            Dictionary of section names to content
        """
        sections = {}
        current_section = "general"
        current_content = []
        
        lines = text.split('\n')
        for line in lines:
            # Detect section headers (lines with colons or all caps)
            if (':' in line and len(line.strip()) < 100) or line.strip().isupper():
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                    current_content = []
                
                # Start new section
                current_section = line.strip().lower().replace(':', '').replace(' ', '_')
            else:
                current_content.append(line)
        
        # Add the last section
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    @staticmethod
    def estimate_complexity(text: str) -> Dict[str, Any]:
        """
        Estimate the complexity of a specification
        
        Args:
            text: Specification text
            
        Returns:
            Complexity metrics
        """
        # Basic metrics
        word_count = len(text.split())
        line_count = len(text.split('\n'))
        section_count = len(TextProcessor.split_into_sections(text))
        keyword_count = len(TextProcessor.extract_keywords(text))
        
        # Complexity heuristics
        complexity_score = (
            (word_count / 100) +
            (section_count * 2) +
            (keyword_count * 0.5)
        )
        
        # Categorize complexity
        if complexity_score < 10:
            complexity_level = "Simple"
        elif complexity_score < 25:
            complexity_level = "Moderate"
        elif complexity_score < 50:
            complexity_level = "Complex"
        else:
            complexity_level = "Very Complex"
        
        return {
            "word_count": word_count,
            "line_count": line_count,
            "section_count": section_count,
            "keyword_count": keyword_count,
            "complexity_score": round(complexity_score, 2),
            "complexity_level": complexity_level
        }

# Code formatting utilities
class CodeFormatter:
    """Utilities for formatting and analyzing RTL code"""
    
    @staticmethod
    def format_verilog_code(code: str, indent_size: int = 2) -> str:
        """
        Basic Verilog code formatting
        
        Args:
            code: Verilog code to format
            indent_size: Number of spaces per indent level
            
        Returns:
            Formatted Verilog code
        """
        if not code:
            return code
        
        lines = code.split('\n')
        formatted_lines = []
        indent_level = 0
        in_block_comment = False
        
        for line in lines:
            stripped_line = line.strip()
            
            # Skip empty lines but preserve structure
            if not stripped_line:
                formatted_lines.append('')
                continue
            
            # Handle block comments
            if '/*' in stripped_line and '*/' not in stripped_line:
                in_block_comment = True
            if '*/' in stripped_line:
                in_block_comment = False
            
            # Calculate indentation
            if in_block_comment:
                indent = indent_level * indent_size
                formatted_lines.append(' ' * indent + stripped_line)
                continue
            
            # Decrease indent for end statements
            if (stripped_line.startswith('end') or 
                stripped_line.startswith('endmodule') or
                stripped_line == 'endcase' or
                stripped_line == 'endfunction' or
                stripped_line == 'endtask'):
                indent_level = max(0, indent_level - 1)
            
            # Apply current indentation
            indent = indent_level * indent_size
            formatted_lines.append(' ' * indent + stripped_line)
            
            # Increase indent for block starts
            if (stripped_line.endswith(' begin') or
                'case' in stripped_line and 'endcase' not in stripped_line or
                'function' in stripped_line or
                'task' in stripped_line):
                indent_level += 1
        
        return '\n'.join(formatted_lines)
    
    @staticmethod
    def extract_module_ports(code: str) -> Dict[str, List[Dict[str, str]]]:
        """
        Extract port declarations from Verilog module
        
        Args:
            code: Verilog module code
            
        Returns:
            Dictionary with input, output, and inout ports
        """
        ports = {
            "inputs": [],
            "outputs": [],
            "inouts": []
        }
        
        # Simple regex pattern for port extraction (basic implementation)
        port_pattern = r'(input|output|inout)\s+(wire|reg)?\s*(\[.*?\])?\s*(\w+)'
        
        matches = re.finditer(port_pattern, code, re.IGNORECASE)
        for match in matches:
            port_type = match.group(1).lower()
            data_type = match.group(2) or "wire"
            width = match.group(3) or ""
            name = match.group(4)
            
            port_info = {
                "name": name,
                "type": data_type,
                "width": width.strip('[] ') if width else "1",
                "description": ""
            }
            
            if port_type == "input":
                ports["inputs"].append(port_info)
            elif port_type == "output":
                ports["outputs"].append(port_info)
            elif port_type == "inout":
                ports["inouts"].append(port_info)
        
        return ports
    
    @staticmethod
    def count_code_metrics(code: str) -> Dict[str, int]:
        """
        Count basic code metrics
        
        Args:
            code: RTL code to analyze
            
        Returns:
            Dictionary of code metrics
        """
        if not code:
            return {}
        
        lines = code.split('\n')
        total_lines = len(lines)
        code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('//')])
        comment_lines = len([line for line in lines if line.strip().startswith('//')])
        blank_lines = len([line for line in lines if not line.strip()])
        
        # Count basic constructs
        always_blocks = len(re.findall(r'\balways\b', code, re.IGNORECASE))
        assign_statements = len(re.findall(r'\bassign\b', code, re.IGNORECASE))
        module_instances = len(re.findall(r'\b\w+\s+\w+\s*\(', code))
        
        return {
            "total_lines": total_lines,
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "blank_lines": blank_lines,
            "always_blocks": always_blocks,
            "assign_statements": assign_statements,
            "module_instances": module_instances
        }

# Specification validation
class SpecificationValidator:
    """Validation utilities for specifications and requirements"""
    
    @staticmethod
    def validate_specification_structure(spec_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate specification structure and completeness
        
        Args:
            spec_data: Parsed specification data
            
        Returns:
            Validation results
        """
        issues = []
        warnings = []
        
        # Check for required fields
        if not spec_data.get("raw_text"):
            issues.append("Specification text is empty")
        
        # Check for minimum content length
        raw_text = spec_data.get("raw_text", "")
        if len(raw_text.strip()) < 50:
            warnings.append("Specification seems very short - may lack detail")
        
        # Check for interface information
        interfaces = spec_data.get("interfaces", [])
        if not interfaces:
            warnings.append("No interfaces specified - consider adding interface details")
        
        # Check for protocols
        protocols = spec_data.get("protocols", [])
        if not protocols:
            warnings.append("No protocols specified - consider adding protocol requirements")
        
        # Validate parameters
        parameters = spec_data.get("parameters", {})
        for key, value in parameters.items():
            if not key.strip():
                issues.append("Empty parameter name found")
            if not value.strip():
                warnings.append(f"Parameter '{key}' has empty value")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "score": max(0, 100 - (len(issues) * 20 + len(warnings) * 5))
        }
    
    @staticmethod
    def validate_requirements(requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate design requirements
        
        Args:
            requirements: Design requirements dictionary
            
        Returns:
            Validation results
        """
        issues = []
        warnings = []
        
        # Check for basic requirements
        if not requirements.get("interface"):
            warnings.append("No interface type specified")
        
        if not requirements.get("performance"):
            warnings.append("No performance target specified")
        
        # Validate specific requirement types
        if requirements.get("frequency"):
            try:
                freq = requirements["frequency"]
                if isinstance(freq, str):
                    # Extract numeric value from string
                    freq_value = float(re.findall(r'\d+\.?\d*', freq)[0])
                    if freq_value > 1000:  # GHz range
                        warnings.append("Very high frequency specified - ensure feasibility")
            except (ValueError, IndexError):
                issues.append("Invalid frequency specification")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }

# Helper functions
def generate_module_name(spec_text: str, prefix: str = "module") -> str:
    """
    Generate a meaningful module name from specification text
    
    Args:
        spec_text: Specification text
        prefix: Prefix for the module name
        
    Returns:
        Generated module name
    """
    # Extract keywords
    keywords = TextProcessor.extract_keywords(spec_text)
    
    # Filter for relevant module-like keywords
    module_keywords = [kw for kw in keywords if kw in [
        'controller', 'interface', 'arbiter', 'decoder', 'encoder',
        'fifo', 'memory', 'cache', 'bridge', 'adapter', 'converter'
    ]]
    
    # Use protocol names if available
    protocols = re.findall(r'\b(axi|ahb|apb|uart|spi|i2c|pcie)\b', spec_text.lower())
    
    # Construct module name
    name_parts = []
    if protocols:
        name_parts.append(protocols[0])
    if module_keywords:
        name_parts.append(module_keywords[0])
    elif keywords:
        name_parts.append(keywords[0])
    
    if not name_parts:
        name_parts = ["design"]
    
    module_name = "_".join(name_parts)
    return f"{prefix}_{module_name}"

def extract_ports_from_rtl(rtl_code: str) -> Dict[str, List[str]]:
    """
    Extract port names from RTL code
    
    Args:
        rtl_code: RTL code to analyze
        
    Returns:
        Dictionary of port lists by direction
    """
    ports = {"inputs": [], "outputs": [], "inouts": []}
    
    # Simple pattern matching for port declarations
    patterns = {
        "inputs": r'\binput\s+(wire|reg)?\s*(\[.*?\])?\s*(\w+)',
        "outputs": r'\boutput\s+(wire|reg)?\s*(\[.*?\])?\s*(\w+)',
        "inouts": r'\binout\s+(wire|reg)?\s*(\[.*?\])?\s*(\w+)'
    }
    
    for port_type, pattern in patterns.items():
        matches = re.findall(pattern, rtl_code, re.IGNORECASE)
        for match in matches:
            port_name = match[2]  # Third group is the port name
            ports[port_type].append(port_name)
    
    return ports

def validate_verilog_syntax(code: str) -> Dict[str, Any]:
    """
    Basic Verilog syntax validation
    
    Args:
        code: Verilog code to validate
        
    Returns:
        Validation results
    """
    issues = []
    warnings = []
    
    # Check for basic structure
    if "module" not in code:
        issues.append("Missing module declaration")
    
    if "endmodule" not in code:
        issues.append("Missing endmodule statement")
    
    # Check for common syntax issues
    if "always @" in code and "begin" not in code:
        warnings.append("Always block may be missing begin/end")
    
    # Check for potential issues
    if re.search(r'=\s*\'[bdh]?x', code, re.IGNORECASE):
        warnings.append("Code contains unknown values (X) - ensure intentional")
    
    if "assign" in code and "=" in code:
        # Check for potential combinational loops
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if "assign" in line and "=" in line:
                # Simple check for self-assignment patterns
                if re.search(r'assign\s+\w+\s*=\s*\w+', line):
                    var_match = re.search(r'assign\s+(\w+)\s*=', line)
                    if var_match:
                        var_name = var_match.group(1)
                        if re.search(r'=\s*[^=]*\b' + re.escape(var_name) + r'\b', line):
                            warnings.append(f"Potential combinational loop with variable '{var_name}'")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings
    }

def calculate_pp_metrics(rtl_code: str) -> Dict[str, float]:
    """
    Calculate basic Power-Performance metrics estimate
    
    Args:
        rtl_code: RTL code to analyze
        
    Returns:
        Estimated PPA metrics
    """
    metrics = CodeFormatter.count_code_metrics(rtl_code)
    
    # Simple heuristic-based estimation
    complexity_score = (
        metrics.get("always_blocks", 0) * 2 +
        metrics.get("assign_statements", 0) * 1 +
        metrics.get("module_instances", 0) * 3
    )
    
    # Normalize scores (these are relative estimates)
    area_estimate = max(1, complexity_score * 10)
    power_estimate = max(1, complexity_score * 5)
    performance_estimate = max(10, 100 - complexity_score)
    
    return {
        "area_score": area_estimate,
        "power_score": power_estimate,
        "performance_score": performance_estimate,
        "complexity_level": "Low" if complexity_score < 5 else 
                           "Medium" if complexity_score < 15 else "High"
    }

def create_project_structure(project_path: str) -> bool:
    """
    Create standard project directory structure
    
    Args:
        project_path: Path to project directory
        
    Returns:
        True if successful, False otherwise
    """
    try:
        directories = [
            "specifications",
            "rtl",
            "testbenches", 
            "constraints",
            "scripts",
            "reports",
            "logs",
            "documents"
        ]
        
        for directory in directories:
            dir_path = os.path.join(project_path, directory)
            os.makedirs(dir_path, exist_ok=True)
        
        # Create basic README
        readme_content = """# VLSI Design Project
        
## Project Structure
- specifications/ - Design specifications and requirements
- rtl/ - Generated RTL code
- testbenches/ - Verification testbenches  
- constraints/ - Timing and synthesis constraints
- scripts/ - Automation scripts
- reports/ - Analysis and synthesis reports
- logs/ - Execution logs
- documents/ - Project documentation

## Generated by VLSI Design AI Tool
"""
        readme_path = os.path.join(project_path, "README.md")
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        return True
        
    except Exception as e:
        print(f"Error creating project structure: {e}")
        return False

# Module initialization
print(f"✅ VLSI Design AI Tool Utilities v{__version__} loaded successfully!")
