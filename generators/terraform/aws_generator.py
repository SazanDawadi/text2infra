# src/generators/terraform/aws_generator.py
import os
import json
from pathlib import Path
import jinja2
from typing import Dict, Any

class AWSTerraformGenerator:
    def __init__(self):
        self.template_dir = Path(__file__).parent / "templates" / "aws"
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
    def generate(self, requirements: Dict[str, Any], output_dir: str = "./terraform") -> Dict[str, str]:
        """
        Generate complete Terraform project structure
        
        Args:
            requirements: Parsed infrastructure requirements
            output_dir: Root directory for Terraform project
            
        Returns:
            Dictionary mapping file paths to generated content
        """
        # Create directory structure
        Path(output_dir).mkdir(exist_ok=True)
        modules_dir = Path(output_dir) / "modules"
        modules_dir.mkdir(exist_ok=True)
        
        generated_files = {}
        
        # Generate main configuration files
        generated_files.update(self._generate_main(requirements, output_dir))
        generated_files.update(self._generate_variables(requirements, output_dir))
        generated_files.update(self._generate_outputs(requirements, output_dir))
        
        # Generate modules if needed
        if "compute" in requirements["configuration"]:
            generated_files.update(
                self._generate_compute_module(requirements, modules_dir))
            
        if "database" in requirements["configuration"]:
            generated_files.update(
                self._generate_database_module(requirements, modules_dir))
            
        return generated_files
    
    def _generate_main(self, requirements: Dict[str, Any], output_dir: str) -> Dict[str, str]:
        """Generate main.tf with module calls"""
        template = self.env.get_template("main.tf.j2")
        content = template.render(
            requirements=requirements,
            has_compute="compute" in requirements["configuration"],
            has_database="database" in requirements["configuration"]
        )
        
        filepath = Path(output_dir) / "main.tf"
        with open(filepath, "w") as f:
            f.write(content)
            
        return {str(filepath): content}
    
    def _generate_variables(self, requirements: Dict[str, Any], output_dir: str) -> Dict[str, str]:
        """Generate variables.tf"""
        template = self.env.get_template("variables.tf.j2")
        content = template.render(
            compute_config=requirements["configuration"].get("compute", {}),
            database_config=requirements["configuration"].get("database", {})
        )
        
        filepath = Path(output_dir) / "variables.tf"
        with open(filepath, "w") as f:
            f.write(content)
            
        return {str(filepath): content}
    
    def _generate_outputs(self, requirements: Dict[str, Any], output_dir: str) -> Dict[str, str]:
        """Generate outputs.tf"""
        template = self.env.get_template("outputs.tf.j2")
        content = template.render(
            has_compute="compute" in requirements["configuration"],
            has_database="database" in requirements["configuration"]
        )
        
        filepath = Path(output_dir) / "outputs.tf"
        with open(filepath, "w") as f:
            f.write(content)
            
        return {str(filepath): content}
    
    def _generate_compute_module(self, requirements: Dict[str, Any], modules_dir: Path) -> Dict[str, str]:
        """Generate compute module"""
        module_dir = modules_dir / "compute"
        module_dir.mkdir(exist_ok=True)
        
        # Main module file
        template = self.env.get_template("modules/compute/main.tf.j2")
        content = template.render(config=requirements["configuration"]["compute"])
        
        main_tf = module_dir / "main.tf"
        with open(main_tf, "w") as f:
            f.write(content)
            
        # Module variables
        template = self.env.get_template("modules/compute/variables.tf.j2")
        vars_content = template.render(config=requirements["configuration"]["compute"])
        
        vars_tf = module_dir / "variables.tf"
        with open(vars_tf, "w") as f:
            f.write(vars_content)
            
        return {
            str(main_tf): content,
            str(vars_tf): vars_content
        }
    
    def _generate_database_module(self, requirements: Dict[str, Any], modules_dir: Path) -> Dict[str, str]:
        """Generate database module"""
        module_dir = modules_dir / "database"
        module_dir.mkdir(exist_ok=True)
        
        # Main module file
        template = self.env.get_template("modules/database/main.tf.j2")
        content = template.render(config=requirements["configuration"]["database"])
        
        main_tf = module_dir / "main.tf"
        with open(main_tf, "w") as f:
            f.write(content)
            
        # Module variables
        template = self.env.get_template("modules/database/variables.tf.j2")
        vars_content = template.render(config=requirements["configuration"]["database"])
        
        vars_tf = module_dir / "variables.tf"
        with open(vars_tf, "w") as f:
            f.write(vars_content)
            
        return {
            str(main_tf): content,
            str(vars_tf): vars_content
        }