import sys
import json
import os
from lib.introspect import StaticAnalyzer
from lib.generator import ScriptGenerator
from lib.healer import SelfHealer
from lib.llm_client import LLMClient

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <installer_path> [--heal]")
        sys.exit(1)

    file_path = sys.argv[1]
    enable_healing = "--heal" in sys.argv
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    print(f"Analyzing {file_path}...")
    analyzer = StaticAnalyzer(file_path)
    results = analyzer.analyze()

    print(json.dumps(results, indent=2))

    print("Generating PowerShell script...")
    generator = ScriptGenerator(results)
    script_code = generator.generate_script()
    
    output_filename = f"install_{os.path.basename(file_path)}.ps1"
    output_path = os.path.join(os.getcwd(), output_filename)
    
    with open(output_path, "w") as f:
        f.write(script_code)
    
    print(f"SUCCESS: PowerShell Script generated at: {output_path}")

    if enable_healing:
        print("\n[WARN] Self-Healing is temporarily disabled during PowerShell migration.")
        # Future: Implement PowerShell script analysis



if __name__ == "__main__":
    main()
