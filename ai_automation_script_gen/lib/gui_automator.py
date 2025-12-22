import logging
import subprocess
import json
import os

class GuiAutomator:
    def __init__(self, exe_path):
        self.exe_path = exe_path
        self.ps_script = os.path.join(os.path.dirname(__file__), "ui_inspector.ps1")

    def launch(self):
        # We don't maintain a persistent python object anymore
        # The logic is handled per-inspection in the PS script for this hybrid MVP
        pass

    def get_ui_hierarchy(self):
        """
        Calls the PowerShell script to get the UI tree.
        """
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", self.ps_script, "-ProcessPath", self.exe_path]
        
        print(f"DEBUG: Running PowerShell introspection...")
        
        try:
            # Run PowerShell
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            # Parse output. The PS script prints JSON lines. 
            # We need to clean up the output to make it valid JSON list
            output_lines = result.stdout.strip().split('\n')
            
            # Simple parser for the MVP output format
            hierarchy = []
            for line in output_lines:
                line = line.strip()
                if line.startswith("{"):
                    try:
                        data = json.loads(line)
                        hierarchy.append(data)
                    except json.JSONDecodeError:
                        pass
            
            return hierarchy

        except Exception as e:
            logging.error(f"Error reading UI hierarchy: {e}")
            return []

    def perform_action(self, action_type, selector):
        # In a generic PS implementation, current MVP doesn't support interactive driving from Python
        # It generates the full PS script at once.
        pass
