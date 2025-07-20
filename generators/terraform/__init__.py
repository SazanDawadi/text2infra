# src/generators/terraform/__init__.py
import os
import json
import jinja2
from typing import Dict, Any
from pathlib import Path

class TerraformGenerator:
    def __init__(self, provider: str = "aws"):
        """
        Initialize Terraform generator for a specific cloud provider
        
        Args:
            provider: Cloud provider (aws, gcp, azure)
        """
        self.provider = provider
        self.template_dir = Path(__file__).parent / "templates" / provider
        self._init_jinja_env()
        
    def _init_jinja_env(self):
        """Initialize Jinja2 template environment"""
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
    def generate(self, requirements: Dict[str, Any], output_dir: str = "./output") -> Dict[str, str]:
        """
        Generate Terraform files from requirements
        
        Args:
            requirements: Parsed requirements from NLP engine
            output_dir: Directory to save generated files
            
        Returns:
            Dictionary mapping filenames to generated content
        """
        os.makedirs(output_dir, exist_ok=True)
        generated_files = {}
        
        # Generate each resource type
        if "compute" in requirements["configuration"]:
            content = self._generate_compute(requirements)
            filename = os.path.join(output_dir, "compute.tf")
            generated_files["compute.tf"] = content
            with open(filename, "w") as f:
                f.write(content)
                
        if "database" in requirements["configuration"]:
            content = self._generate_database(requirements)
            filename = os.path.join(output_dir, "database.tf")
            generated_files["database.tf"] = content
            with open(filename, "w") as f:
                f.write(content)
                
        # Generate variables.tf if needed
        if "variables" in requirements.get("special_requirements", []):
            content = self._generate_variables(requirements)
            filename = os.path.join(output_dir, "variables.tf")
            generated_files["variables.tf"] = content
            with open(filename, "w") as f:
                f.write(content)
                
        return generated_files
    
    def _generate_compute(self, requirements: Dict[str, Any]) -> str:
        """Generate compute resources"""
        template = self.env.get_template("compute.tf.j2")
        return template.render(config=requirements["configuration"]["compute"])
    
    def _generate_database(self, requirements: Dict[str, Any]) -> str:
        """Generate database resources"""
        template = self.env.get_template("database.tf.j2")
        return template.render(config=requirements["configuration"]["database"])
    
    def _generate_variables(self, requirements: Dict[str, Any]) -> str:
        """Generate variables file"""
        return """variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}
"""

# Factory function for easy access
def get_terraform_generator(provider: str) -> TerraformGenerator:
    if provider == "aws":
        from .aws_generator import AWSTerraformGenerator
        return AWSTerraformGenerator()
    elif provider == "gcp":
        from .gcp_generator import GCPTerraformGenerator
        return GCPTerraformGenerator()
    else:
        return TerraformGenerator(provider)