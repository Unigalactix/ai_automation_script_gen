import os
import time
from lib.healer import SelfHealer
from lib.llm_client import LLMClient

# 1. Create a "Bad" Script that times out
bad_script_name = "broken_install.py"
bad_script_content = """
import time
import subprocess
import sys

def run():
    print("Starting installation...")
    # Simulate a process that takes 2 seconds
    time.sleep(2)
    
    # But we set a timeout of 1 second
    try:
        # We rely on an external command for timeout simulation
        # Ping is a simple cross-platform delayer
        subprocess.run("ping 127.0.0.1 -n 3", shell=True, timeout=1) 
    except subprocess.TimeoutExpired:
        print("FAIL: Installation timed out.")
        sys.exit(1)
        
    print("PASS: Install done.")
    sys.exit(0)

if __name__ == "__main__":
    run()
"""

with open(bad_script_name, "w") as f:
    f.write(bad_script_content)

print(f"Created {bad_script_name} with intentional timeout bug.")

# 2. Run Healer
print("\n--- Starting Healer Demo ---")
llm = LLMClient()
healer = SelfHealer(llm)

success, fixed_script = healer.attempt_heal(bad_script_name)

if success:
    print(f"\n[DEMO SUCCESS] The script was fixed! New file: {fixed_script}")
    with open(fixed_script, "r") as f:
        print("-" * 20)
        print(f.read())
        print("-" * 20)
else:
    print("\n[DEMO FAIL] Healer could not fix it.")
