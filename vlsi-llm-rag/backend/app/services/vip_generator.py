from typing import Dict, Any
from .llm_service import llm_service

class VIPGenerator:
    def __init__(self):
        self.llm_service = llm_service
    
    async def generate_testbench(self, rtl_code: str, module_name: str) -> Dict[str, Any]:
        """Generate testbench for the given RTL"""
        
        prompt = f"""
        Generate a comprehensive SystemVerilog testbench for the following RTL module:
        
        MODULE: {module_name}
        CODE:
        {rtl_code}
        
        Requirements:
        1. Include proper clock generation and reset sequence
        2. Add basic test cases covering normal operation
        3. Include error injection tests if applicable
        4. Add simple scoreboard/checker for basic functionality
        5. Include waveform dump commands
        6. Make it self-checking where possible
        
        Format:
        CODE:
        ```systemverilog
        [testbench code]
        ```
        """
        
        try:
            response = await self.llm_service.generate_rtl(prompt, [])
            return {
                "testbench_code": response["code"],
                "module_name": f"tb_{module_name}"
            }
        except Exception as e:
            return self._get_fallback_testbench(module_name)
    
    def _get_fallback_testbench(self, module_name: str) -> Dict[str, Any]:
        """Fallback testbench implementation"""
        return {
            "testbench_code": f"""
`timescale 1ns/1ps

module tb_{module_name};
    reg clk;
    reg rst_n;
    
    // Clock generation
    always #5 clk = ~clk;
    
    // Test sequence
    initial begin
        $dumpfile("waves.vcd");
        $dumpvars(0, tb_{module_name});
        
        clk = 0;
        rst_n = 0;
        
        #20 rst_n = 1;
        
        // Add test cases here
        
        #100 $finish;
    end
    
    // Instantiate DUT
    {module_name} dut (
        .clk(clk),
        .rst_n(rst_n)
        // Connect other ports
    );
    
endmodule
            """.strip(),
            "module_name": f"tb_{module_name}"
        }

vip_generator = VIPGenerator()
