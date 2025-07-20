# main.py

from nl_engine import NLPTerraformEngine
from generators.terraform import get_terraform_generator
import json
import os
from dotenv import load_dotenv

# Load .env variables (for API key)
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("Please set GEMINI_API_KEY in your .env file")

# Initialize NLP Engine with Gemini API key
nlp_engine = NLPTerraformEngine(api_key=API_KEY)

# Example infrastructure requests (add your own for testing)
requests = [
    "I need a web server with 2 CPUs, 4GB RAM and a PostgreSQL database with 100GB storage on AWS",
    "Create a Kubernetes cluster with 3 worker nodes and 2 CPU cores each in Google Cloud",
    "Set up a simple static website with cloud storage and CDN"
]

# Directory to save Terraform files
output_base_dir = "./output"

for i, request in enumerate(requests):
    print(f"\nProcessing request [{i+1}]: '{request}'")
    try:
        # Step 1: Parse Infra Requirements
        requirements = nlp_engine.parse_infrastructure_request(request)
        print("Extracted requirements:")
        print(json.dumps(requirements, indent=2))

        # Step 2: Get provider-specific Terraform generator
        provider = requirements.get("provider")
        if not provider:
            raise ValueError("Provider not specified in extracted requirements.")

        generator = get_terraform_generator(provider)

        # Step 3: Generate Terraform files
        output_dir = os.path.join(output_base_dir, f"{provider}_example_{i+1}")
        generated_files = generator.generate(requirements, output_dir=output_dir)

        # Step 4: Print generated files
        print("Generated Terraform files:")
        for filename, content in generated_files.items():
            print(f"\n--- {filename} ---")
            print(content)

    except Exception as e:
        print(f"❌ Error processing request: {str(e)}")
