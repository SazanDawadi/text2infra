# src/generators/terraform/gcp_generator.py
from . import TerraformGenerator
from typing import Dict, Any

class GCPTerraformGenerator(TerraformGenerator):
    def __init__(self):
        super().__init__("gcp")
        
    def _generate_compute(self, requirements: Dict[str, Any]) -> str:
        """Generate GCP-specific compute resources"""
        config = requirements["configuration"]["compute"]
        
        # Set GCP-specific defaults
        config.setdefault("machine_type", f"e2-standard-{config.get('cpus', 2)}")
        config.setdefault("image", "debian-cloud/debian-10")
        
        return super()._generate_compute(requirements)