import sys
import json
import os
from lib.introspect import StaticAnalyzer
from lib.generator import ScriptGenerator
from lib.healer import SelfHealer
from lib.llm_client import LLMClient

def select_from_setups():
    # Helper to find setups relative to this script or CWD
    candidates = [
        "setups",
        os.path.join(os.path.dirname(__file__), "setups"),
        os.path.join(os.getcwd(), "ai_automation_script_gen", "setups")
    ]
    setups_dir = None
    for c in candidates:
        if os.path.exists(c) and os.path.isdir(c):
            setups_dir = c
            break
            
    if not setups_dir:
        print("No 'setups' folder found.")
        return None

    files = [f for f in os.listdir(setups_dir) if f.endswith('.exe') or f.endswith('.msi')]
    if not files:
        print(f"No installers found in {setups_dir}")
        return None

    print(f"\nAvailable Installers in '{setups_dir}':")
    for idx, f in enumerate(files):
        print(f"[{idx+1}] {f}")
    
    while True:
        try:
            choice = input("\nSelect an installer number (or 'q' to quit): ")
            if choice.lower() == 'q':
                sys.exit(0)
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                return os.path.join(setups_dir, files[idx])
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")

def main():
    file_path = None
    enable_healing = False

    # Check args
    if len(sys.argv) >= 2 and not sys.argv[1].startswith("--"):
        file_path = sys.argv[1]
    
    if "--heal" in sys.argv:
        enable_healing = True

    # Interactive mode if no file provided
    if not file_path:
        print("No installer path provided.")
        file_path = select_from_setups()
        if not file_path:
            sys.exit(1)

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    print(f"\nAnalyzing {file_path}...")
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
