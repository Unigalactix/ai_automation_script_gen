import logging
import json
import re

class LLMClient:
    def __init__(self, model_name="dummy-model"):
        self.model_name = model_name

    def decide_next_action(self, ui_context, history):
        """
        Simulates an LLM API call.
        Inputs: 
            ui_context (list): List of UI elements on screen.
            history (list): List of previous actions taken.
        Returns:
            dict: The recommended action (e.g., {"action": "click", "target": "Next"})
            or None if finished.
        """
        
        # Heuristic Logic (Mocking the AI)
        # In production, this would be a prompt to OpenAI/Gemini:
        # "Visible elements are {ui_context}. Goal is to install. What is the next step?"
        
        print(f"[AI Reasoning] Analyzing {len(ui_context)} UI elements...")
        
        # Priority list for standard installers
        priorities = [
            "I agree", "I accept", "Agree", 
            "Next", "Next >", "Install", "Finish", "Close"
        ]
        
        # 1. Check for blocking "Agree" checkboxes first
        for item in ui_context:
            text = item.get('title', '').lower()
            if "agree" in text and item.get('control_type') in ['CheckBox', 'RadioButton']:
                 if not item.get("toggle_state", "off") == "on": # hypothetical state check
                     return {"action": "click", "selector": {"title": item['title'], "control_type": item['control_type']}, "reason": "Accepting Terms"}

        # 2. Check for Navigation Buttons
        for keyword in priorities:
            for item in ui_context:
                text = item.get('title', '').strip()
                if text.lower() == keyword.lower():
                    # Avoid clicking "Cancel"
                    return {"action": "click", "selector": {"title": text, "control_type": item['control_type']}, "reason": f"Clicking navigation button '{text}'"}
        
        return None

    def analyze_error(self, error_log, current_script):
        """
        Analyzes an execution error and suggests a fix.
        In a real system, this sends the error + script to an LLM.
        """
        print("[AI Healing] Analyzing error log...")
        
        # Heuristic fixes for MVP
        if "TimeoutExpired" in error_log or "timed out" in error_log:
             return {
                 "type": "modify_param",
                 "param": "timeout",
                 "value": 1200,
                 "reason": "Installation took longer than expected."
             }
        
        if "ElementNotFoundError" in error_log:
             # Assume we missed a pop-up or timing issue
             return {
                 "type": "insert_step",
                 "code": "time.sleep(5) # adaptive wait for slow UI",
                 "location": "before_failure",
                 "reason": "Element not found, likely timing issue."
             }

        # Generic retry
        return {
            "type": "retry", 
            "reason": "Transient error suspected."
        }

    def apply_fix(self, script_content, fix):
        """
        Applies a suggested fix to the script content.
        This is a crude string manipulator for the MVP.
        """
        if not fix:
            return script_content
            
        print(f"[AI Healing] Applying fix: {fix['reason']}")
        
        if fix['type'] == 'modify_param' and fix['param'] == 'timeout':
            # Regex replace timeout=NUM with timeout=NEW_VAL
            # Matches timeout=1, timeout= 600, etc.
            pattern = r"timeout\s*=\s*\d+"
            replacement = f"timeout={fix['value']}"
            return re.sub(pattern, replacement, script_content)
        
        elif fix['type'] == 'insert_step':
            # Insert before the failing line (simulated by just adding to top of install for now)
            # In real life, we'd need line numbers from the stack trace
            lines = script_content.splitlines()
            # Naive injection
            for i, line in enumerate(lines):
                if "subprocess.run" in line:
                     lines.insert(i, "    " + fix['code'])
                     break
            return "\n".join(lines)
            
        return script_content

    def generate_step_code(self, decision):
        """
        Converts the decision into pywinauto code for the script generator.
        """
        if not decision: 
            return "# No action determined"
            
        action = decision['action']
        title = decision['selector']['title']
        ctype = decision['selector'].get('control_type')
        
        if action == 'click':
            return f"dlg.child_window(title='{title}', control_type='{ctype}').click_input()"
            
        return "# Unknown action"
