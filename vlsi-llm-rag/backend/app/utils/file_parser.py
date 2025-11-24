import re
from typing import Dict, Any, List
import yaml
import json

class FileParser:
    @staticmethod
    def parse_specification(file_content: str, file_type: str = "txt") -> Dict[str, Any]:
        """Parse specification file and extract structured information"""
        
        parsed_data = {
            "raw_text": file_content,
            "interfaces": [],
            "protocols": [],
            "requirements": {},
            "parameters": {}
        }
        
        # Extract interfaces (looking for common patterns)
        interface_patterns = [
            r'interface\s*:\s*(.+)',
            r'port\s*:\s*(.+)', 
            r'input\s+(\w+\s*\w*)\s*,\s*output',
            r'output\s+(\w+\s*\w*)\s*,\s*input'
        ]
        
        for pattern in interface_patterns:
            matches = re.findall(pattern, file_content, re.IGNORECASE)
            parsed_data["interfaces"].extend(matches)
        
        # Extract protocols
        protocol_keywords = ['AXI', 'AHB', 'APB', 'UART', 'SPI', 'I2C', 'PCIe', 'Ethernet']
        for keyword in protocol_keywords:
            if keyword.lower() in file_content.lower():
                parsed_data["protocols"].append(keyword)
        
        # Extract parameters (looking for key-value pairs)
        param_pattern = r'(\w+)\s*[:=]\s*([^\n]+)'
        params = re.findall(param_pattern, file_content)
        for key, value in params:
            parsed_data["parameters"][key.strip()] = value.strip()
        
        return parsed_data
    
    @staticmethod
    def parse_requirements(file_content: str) -> Dict[str, Any]:
        """Parse requirements file (YAML/JSON/Markdown)"""
        
        # Try YAML first
        try:
            return yaml.safe_load(file_content)
        except:
            pass
        
        # Try JSON
        try:
            return json.loads(file_content)
        except:
            pass
        
        # Fallback to text parsing
        requirements = {}
        lines = file_content.split('\n')
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                requirements[key.strip()] = value.strip()
        
        return requirements
