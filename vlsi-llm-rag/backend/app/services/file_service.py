import os
import shutil
import aiofiles
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import yaml
from pathlib import Path
import hashlib
from ...config import settings

class FileService:
    """
    Service for handling file operations including uploads, storage management,
    and project organization for VLSI design files.
    """
    
    def __init__(self):
        self.base_upload_dir = settings.UPLOAD_DIR
        self.allowed_extensions = {
            '.txt', '.md', '.yaml', '.yml', '.json', 
            '.v', '.vh', '.sv', '.vhd', '.vhdl',  # Verilog/VHDL files
            '.pdf', '.doc', '.docx'  # Documentation
        }
        self.max_file_size = settings.MAX_FILE_SIZE
        
        # Create directory structure
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directory structure"""
        directories = [
            self.base_upload_dir,
            f"{self.base_upload_dir}/specs",
            f"{self.base_upload_dir}/rtl",
            f"{self.base_upload_dir}/testbenches",
            f"{self.base_upload_dir}/reports",
            f"{self.base_upload_dir}/temp",
            f"{self.base_upload_dir}/projects"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    async def save_uploaded_file(self, file, project_id: str = None) -> Dict[str, Any]:
        """
        Save uploaded file with proper organization
        
        Args:
            file: Uploaded file object
            project_id: Optional project identifier for organization
            
        Returns:
            Dictionary with file metadata
        """
        try:
            # Validate file size
            content = await file.read()
            if len(content) > self.max_file_size:
                raise ValueError(f"File size exceeds maximum limit of {self.max_file_size} bytes")
            
            # Validate file extension
            file_extension = Path(file.filename).suffix.lower()
            if file_extension not in self.allowed_extensions:
                raise ValueError(f"File type {file_extension} not allowed")
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_hash = hashlib.md5(content).hexdigest()[:8]
            safe_filename = Path(file.filename).stem.replace(' ', '_')
            unique_filename = f"{timestamp}_{file_hash}_{safe_filename}{file_extension}"
            
            # Determine save path based on file type and project
            if project_id:
                project_dir = f"{self.base_upload_dir}/projects/{project_id}"
                os.makedirs(project_dir, exist_ok=True)
                save_path = f"{project_dir}/{unique_filename}"
            else:
                # Categorize by file type
                if file_extension in ['.v', '.vh', '.sv', '.vhd', '.vhdl']:
                    save_path = f"{self.base_upload_dir}/rtl/{unique_filename}"
                elif file_extension in ['.txt', '.md', '.yaml', '.yml', '.json']:
                    save_path = f"{self.base_upload_dir}/specs/{unique_filename}"
                else:
                    save_path = f"{self.base_upload_dir}/temp/{unique_filename}"
            
            # Save file
            async with aiofiles.open(save_path, 'wb') as f:
                await f.write(content)
            
            # Return file metadata
            return {
                "filename": file.filename,
                "saved_filename": unique_filename,
                "file_path": save_path,
                "file_size": len(content),
                "file_type": file_extension,
                "project_id": project_id,
                "upload_time": datetime.now().isoformat(),
                "file_hash": file_hash
            }
            
        except Exception as e:
            raise Exception(f"Failed to save file: {str(e)}")
    
    async def read_file_content(self, file_path: str) -> str:
        """
        Read file content as text
        
        Args:
            file_path: Path to the file
            
        Returns:
            File content as string
        """
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            return content
        except UnicodeDecodeError:
            # Try different encoding if UTF-8 fails
            async with aiofiles.open(file_path, 'r', encoding='latin-1') as f:
                content = await f.read()
            return content
        except Exception as e:
            raise Exception(f"Failed to read file: {str(e)}")
    
    async def save_generated_rtl(self, rtl_code: str, module_name: str, 
                               project_id: str = None, metadata: Dict = None) -> Dict[str, Any]:
        """
        Save generated RTL code to file
        
        Args:
            rtl_code: Generated RTL code
            module_name: Name of the module
            project_id: Optional project identifier
            metadata: Additional metadata about the generation
            
        Returns:
            Dictionary with file information
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{module_name}.v"
            
            if project_id:
                project_dir = f"{self.base_upload_dir}/projects/{project_id}/rtl"
                os.makedirs(project_dir, exist_ok=True)
                file_path = f"{project_dir}/{filename}"
            else:
                file_path = f"{self.base_upload_dir}/rtl/{filename}"
            
            # Save RTL code
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(rtl_code)
            
            # Save metadata if provided
            if metadata:
                metadata_file = file_path.replace('.v', '_metadata.json')
                async with aiofiles.open(metadata_file, 'w', encoding='utf-8') as f:
                    await f.write(json.dumps(metadata, indent=2))
            
            return {
                "filename": filename,
                "file_path": file_path,
                "module_name": module_name,
                "saved_at": datetime.now().isoformat(),
                "file_size": len(rtl_code)
            }
            
        except Exception as e:
            raise Exception(f"Failed to save RTL file: {str(e)}")
    
    async def save_testbench(self, testbench_code: str, module_name: str,
                           project_id: str = None) -> Dict[str, Any]:
        """
        Save generated testbench code
        
        Args:
            testbench_code: Generated testbench code
            module_name: Name of the module under test
            project_id: Optional project identifier
            
        Returns:
            Dictionary with file information
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_tb_{module_name}.sv"
            
            if project_id:
                project_dir = f"{self.base_upload_dir}/projects/{project_id}/testbenches"
                os.makedirs(project_dir, exist_ok=True)
                file_path = f"{project_dir}/{filename}"
            else:
                file_path = f"{self.base_upload_dir}/testbenches/{filename}"
            
            # Save testbench code
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(testbench_code)
            
            return {
                "filename": filename,
                "file_path": file_path,
                "module_name": f"tb_{module_name}",
                "saved_at": datetime.now().isoformat(),
                "file_size": len(testbench_code)
            }
            
        except Exception as e:
            raise Exception(f"Failed to save testbench file: {str(e)}")
    
    async def create_project(self, project_name: str, description: str = "") -> Dict[str, Any]:
        """
        Create a new project directory structure
        
        Args:
            project_name: Name of the project
            description: Project description
            
        Returns:
            Project information
        """
        try:
            project_id = hashlib.md5(f"{project_name}_{datetime.now()}".encode()).hexdigest()[:12]
            project_dir = f"{self.base_upload_dir}/projects/{project_id}"
            
            # Create project structure
            subdirs = ['specs', 'rtl', 'testbenches', 'reports', 'logs']
            for subdir in subdirs:
                os.makedirs(f"{project_dir}/{subdir}", exist_ok=True)
            
            # Create project info file
            project_info = {
                "project_id": project_id,
                "project_name": project_name,
                "description": description,
                "created_at": datetime.now().isoformat(),
                "directories": subdirs
            }
            
            info_file = f"{project_dir}/project_info.json"
            async with aiofiles.open(info_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(project_info, indent=2))
            
            return project_info
            
        except Exception as e:
            raise Exception(f"Failed to create project: {str(e)}")
    
    async def get_project_files(self, project_id: str) -> Dict[str, List[Dict]]:
        """
        Get all files in a project organized by type
        
        Args:
            project_id: Project identifier
            
        Returns:
            Dictionary of files organized by type
        """
        try:
            project_dir = f"{self.base_upload_dir}/projects/{project_id}"
            if not os.path.exists(project_dir):
                raise ValueError(f"Project {project_id} not found")
            
            file_categories = {
                'specifications': [],
                'rtl': [],
                'testbenches': [],
                'reports': [],
                'logs': []
            }
            
            for category in file_categories.keys():
                category_dir = f"{project_dir}/{category}"
                if os.path.exists(category_dir):
                    for filename in os.listdir(category_dir):
                        file_path = f"{category_dir}/{filename}"
                        if os.path.isfile(file_path):
                            stat = os.stat(file_path)
                            file_categories[category].append({
                                'filename': filename,
                                'file_path': file_path,
                                'size': stat.st_size,
                                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                            })
            
            return file_categories
            
        except Exception as e:
            raise Exception(f"Failed to get project files: {str(e)}")
    
    async def save_analysis_report(self, report_data: Dict[str, Any], 
                                 report_type: str, project_id: str = None) -> Dict[str, Any]:
        """
        Save analysis reports (synthesis, timing, verification results)
        
        Args:
            report_data: Report data to save
            report_type: Type of report (synthesis, timing, coverage, etc.)
            project_id: Optional project identifier
            
        Returns:
            Report file information
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{report_type}_report.json"
            
            if project_id:
                report_dir = f"{self.base_upload_dir}/projects/{project_id}/reports"
                os.makedirs(report_dir, exist_ok=True)
                file_path = f"{report_dir}/{filename}"
            else:
                file_path = f"{self.base_upload_dir}/reports/{filename}"
            
            # Save report as JSON
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(report_data, indent=2))
            
            return {
                "filename": filename,
                "file_path": file_path,
                "report_type": report_type,
                "saved_at": datetime.now().isoformat(),
                "size": len(json.dumps(report_data))
            }
            
        except Exception as e:
            raise Exception(f"Failed to save analysis report: {str(e)}")
    
    async def cleanup_old_files(self, max_age_hours: int = 24):
        """
        Clean up temporary files older than specified age
        
        Args:
            max_age_hours: Maximum age of files in hours
        """
        try:
            temp_dir = f"{self.base_upload_dir}/temp"
            if not os.path.exists(temp_dir):
                return
            
            current_time = datetime.now().timestamp()
            max_age_seconds = max_age_hours * 3600
            
            for filename in os.listdir(temp_dir):
                file_path = f"{temp_dir}/{filename}"
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > max_age_seconds:
                        os.remove(file_path)
                        
        except Exception as e:
            print(f"Cleanup warning: {str(e)}")
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get detailed information about a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            File information dictionary
        """
        try:
            if not os.path.exists(file_path):
                raise ValueError("File does not exist")
            
            stat = os.stat(file_path)
            file_extension = Path(file_path).suffix.lower()
            
            return {
                'filename': Path(file_path).name,
                'file_path': file_path,
                'size': stat.st_size,
                'size_human': self._bytes_to_human(stat.st_size),
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'extension': file_extension,
                'type': self._get_file_type(file_extension)
            }
            
        except Exception as e:
            raise Exception(f"Failed to get file info: {str(e)}")
    
    def _get_file_type(self, extension: str) -> str:
        """Map file extension to human-readable type"""
        type_mapping = {
            '.v': 'Verilog Source',
            '.sv': 'SystemVerilog Source',
            '.vhd': 'VHDL Source',
            '.vhdl': 'VHDL Source',
            '.txt': 'Text Document',
            '.md': 'Markdown Document',
            '.yaml': 'YAML Configuration',
            '.yml': 'YAML Configuration',
            '.json': 'JSON Data',
            '.pdf': 'PDF Document',
            '.doc': 'Word Document',
            '.docx': 'Word Document'
        }
        return type_mapping.get(extension, 'Unknown')
    
    def _bytes_to_human(self, bytes_size: int) -> str:
        """Convert bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} TB"
    
    async def search_files(self, query: str, project_id: str = None) -> List[Dict[str, Any]]:
        """
        Search for files containing specific text
        
        Args:
            query: Search query
            project_id: Optional project scope
            
        Returns:
            List of matching files
        """
        try:
            results = []
            search_dirs = []
            
            if project_id:
                project_dir = f"{self.base_upload_dir}/projects/{project_id}"
                if os.path.exists(project_dir):
                    search_dirs.append(project_dir)
            else:
                search_dirs = [
                    f"{self.base_upload_dir}/specs",
                    f"{self.base_upload_dir}/rtl",
                    f"{self.base_upload_dir}/testbenches"
                ]
            
            for search_dir in search_dirs:
                if os.path.exists(search_dir):
                    for root, dirs, files in os.walk(search_dir):
                        for file in files:
                            if file.endswith(('.txt', '.md', '.v', '.sv', '.vhd', '.json', '.yaml', '.yml')):
                                file_path = os.path.join(root, file)
                                try:
                                    content = await self.read_file_content(file_path)
                                    if query.lower() in content.lower():
                                        results.append(self.get_file_info(file_path))
                                except:
                                    continue  # Skip files that can't be read
            
            return results
            
        except Exception as e:
            raise Exception(f"Search failed: {str(e)}")

# Global file service instance
file_service = FileService()
