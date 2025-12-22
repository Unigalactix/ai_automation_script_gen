
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
        subprocess.run("ping 127.0.0.1 -n 3", shell=True, timeout=1200) 
    except subprocess.TimeoutExpired:
        print("FAIL: Installation timed out.")
        sys.exit(1)
        
    print("PASS: Install done.")
    sys.exit(0)

if __name__ == "__main__":
    run()
