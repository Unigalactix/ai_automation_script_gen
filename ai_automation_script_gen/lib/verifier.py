
import subprocess
import sys
import os

def verify_script(script_path):
    """
    Runs the generated script in a subprocess to verify it works.
    In a real scenario, this would run inside a Sandbox.
    """
    if not os.path.exists(script_path):
        return False, "Script file not found"
        
    print(f"Verifying script: {script_path}")
    try:
        # We run it with python
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, f"Output: {result.stdout}\nError: {result.stderr}"
            
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verifier.py <generated_script_path>")
        sys.exit(1)
        
    success, output = verify_script(sys.argv[1])
    if success:
        print("VERIFICATION PASSED")
        print(output)
        sys.exit(0)
    else:
        print("VERIFICATION FAILED")
        print(output)
        sys.exit(1)
