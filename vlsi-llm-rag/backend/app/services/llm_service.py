import google.generativeai as genai
import os
from typing import List, Dict, Any
from ...config import settings

class LLMService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    async def generate_rtl(self, spec_text: str, context: List[str] = None) -> Dict[str, Any]:
        """Generate RTL code from specification"""
        if not self.model:
            return self._get_fallback_rtl()
        
        prompt = self._build_rtl_prompt(spec_text, context)
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_llm_response(response.text)
        except Exception as e:
            print(f"LLM Error: {e}")
            return self._get_fallback_rtl()
    
    def _build_rtl_prompt(self, spec_text: str, context: List[str]) -> str:
        context_text = "\n".join(context) if context else ""
        
        prompt = f"""
        You are an expert VLSI design engineer. Generate optimized, synthesizable Verilog RTL code based on the specification.
        
        CONTEXT FROM KNOWLEDGE BASE:
        {context_text}
        
        SPECIFICATION:
        {spec_text}
        
        REQUIREMENTS:
        1. Generate complete, synthesizable Verilog code
        2. Focus on PPA optimization (Power, Performance, Area)
        3. Include proper module declaration with ports
        4. Implement efficient FSM if needed
        5. Add comments for key functionality
        6. Ensure code follows industry best practices
        
        Please provide the response in this exact format:
        MODULE_NAME: [module_name_here]
        CODE:
        ```verilog
        [verilog code here]
        ```
        EXPLANATION: [brief explanation of the design]
        """
        return prompt
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured data"""
        lines = response.split('\n')
        module_name = "unknown_module"
        code = ""
        explanation = ""
        in_code_block = False
        
        for line in lines:
            if line.startswith("MODULE_NAME:"):
                module_name = line.replace("MODULE_NAME:", "").strip()
            elif line.startswith("```verilog"):
                in_code_block = True
            elif line.startswith("```") and in_code_block:
                in_code_block = False
            elif in_code_block:
                code += line + "\n"
            elif line.startswith("EXPLANATION:"):
                explanation = line.replace("EXPLANATION:", "").strip()
        
        return {
            "module_name": module_name,
            "code": code.strip(),
            "explanation": explanation
        }
    
    def _get_fallback_rtl(self) -> Dict[str, Any]:
        """Fallback RTL when LLM is not available"""
        return {
            "module_name": "sample_module",
            "code": """
module sample_module (
    input wire clk,
    input wire rst_n,
    input wire [7:0] data_in,
    output reg [7:0] data_out,
    output reg valid
);
    // Sample implementation
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            data_out <= 8'b0;
            valid <= 1'b0;
        end else begin
            data_out <= data_in;
            valid <= 1'b1;
        end
    end
endmodule
            """.strip(),
            "explanation": "Fallback implementation - basic register with valid signal"
        }

llm_service = LLMService()
