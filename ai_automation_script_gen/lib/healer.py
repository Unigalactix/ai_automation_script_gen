import logging
import os
import sys
from lib.verifier import verify_script

class SelfHealer:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.max_retries = 3

    def attempt_heal(self, script_path):
        """
        Tries to run the script. If it fails, attempts to fix it and re-run.
        """
        current_script_path = script_path
        
        for attempt in range(1, self.max_retries + 1):
            print(f"\n--- Execution Attempt {attempt}/{self.max_retries} ---")
            success, output = verify_script(current_script_path)
            
            if success:
                print("SUCCESS: Script executed successfully.")
                return True, current_script_path
            
            print(f"FAILURE: Script failed with error.")
            # In real world, 'output' contains stderr and stdout
            
            # Analyze error
            with open(current_script_path, 'r') as f:
                content = f.read()
            
            fix = self.llm.analyze_error(output, content)
            
            if not fix:
                print("AI could not determine a fix. Aborting.")
                return False, current_script_path
                
            # Apply fix
            new_content = self.llm.apply_fix(content, fix)
            
            # Save new version
            new_path = current_script_path.replace(".py", f"_v{attempt}.py")
            with open(new_path, 'w') as f:
                f.write(new_content)
                
            print(f"Created patched script: {new_path}")
            current_script_path = new_path
            
        return False, current_script_path
