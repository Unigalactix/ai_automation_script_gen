import logging
import time
try:
    from pywinauto import Desktop, Application
except ImportError:
    Desktop = None
    Application = None
    logging.warning("pywinauto not installed. GUI automation features disabled.")

class GuiAutomator:
    def __init__(self, exe_path):
        self.exe_path = exe_path
        self.app = None

    def launch(self):
        if not Application:
            raise RuntimeError("pywinauto is required for GUI automation")
        
        logging.info(f"Launching GUI installer: {self.exe_path}")
        try:
            self.app = Application(backend="uia").start(self.exe_path)
            # wait for window to appear
            time.sleep(2) 
            return True
        except Exception as e:
            logging.error(f"Failed to launch app: {e}")
            return False

    def get_ui_hierarchy(self):
        """
        Captures the current state of the active window.
        Returns a simplified JSON-like dict of controls.
        """
        if not self.app:
            return {}

        hierarchy = []
        try:
            # Connect to the likely top window
            dlg = self.app.top_window()
            
            # Simple recursive dumper or just list interactive elements
            # For AI context, we need labels (text), control types, and identifiers
            for child in dlg.descendants():
                try:
                    element_info = {
                        "title": child.window_text(),
                        "class": child.friendly_class_name(),
                        "control_type": child.element_info.control_type,
                        "enabled": child.is_enabled(),
                        "visible": child.is_visible()
                    }
                    if element_info["visible"]: # Filter out invisible noise
                        hierarchy.append(element_info)
                except Exception:
                    continue
                    
        except Exception as e:
            logging.error(f"Error reading UI hierarchy: {e}")

        return hierarchy

    def perform_action(self, action_type, selector):
        """
        Executes an action based on AI decision.
        action_type: 'click', 'type'
        selector: {'title': 'Next', 'control_type': 'Button'}
        """
        if not self.app: 
            return False
            
        try:
            dlg = self.app.top_window()
            # Simple title matching for MVP
            if 'title' in selector:
                ctrl = dlg.child_window(title=selector['title'], control_type=selector.get('control_type'))
                if action_type == 'click':
                    ctrl.click_input()
                    return True
        except Exception as e:
            logging.error(f"Action failed: {e}")
            return False
        return False
