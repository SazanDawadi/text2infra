# nl_engine.py
import google.generativeai as genai
import re
import json
from typing import Dict, Any

class NLPTerraformEngine:
    def __init__(self, api_key: str):
        """
        Initialize the Gemini NLP engine
        
        Args:
            api_key: Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Define our system prompt template
        self.system_prompt = """
        You are an expert cloud infrastructure architect that converts natural language requests 
        into structured infrastructure requirements. Analyze the user request and extract:

        1. Required cloud resources (e.g., compute, storage, database)
        2. Configuration details (e.g., CPU, memory, storage size)
        3. Preferred cloud provider if mentioned
        4. Any special requirements (e.g., high availability, security)

        Return ONLY valid JSON with this structure:
        {
            "resources_needed": ["ec2", "rds"],
            "configuration": {
                "compute": {"cpus": 2, "memory": "4GB"},
                "database": {"engine": "postgresql", "size": "100GB"}
            },
            "provider": "aws",
            "special_requirements": ["high availability"]
        }
        """

    def parse_infrastructure_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process natural language infrastructure request
        
        Args:
            user_input: Natural language description of desired infrastructure
            
        Returns:
            Dictionary containing structured infrastructure requirements
        """
        try:
            # Generate the prompt
            full_prompt = f"{self.system_prompt}\n\nUser request: {user_input}"
            
            # Get response from Gemini
            response = self.model.generate_content(full_prompt)
            
            # Extract JSON from response
            json_str = self._extract_json(response.text)
            
            # Parse and validate
            requirements = json.loads(json_str)
            return self._validate_requirements(requirements)
            
        except Exception as e:
            raise ValueError(f"Failed to process request: {str(e)}")

    def _extract_json(self, text: str) -> str:
        """Extract JSON string from Gemini response"""
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if not match:
            raise ValueError("No valid JSON found in response")
        return match.group()

    def _validate_requirements(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the extracted requirements"""
        required_keys = ["resources_needed", "configuration"]
        for key in required_keys:
            if key not in requirements:
                raise ValueError(f"Missing required key in response: {key}")
        
        # Set default provider if not specified
        if "provider" not in requirements:
            requirements["provider"] = "aws"
            
        return requirements