# AI-Driven Automation Script Generator

## Overview
This tool automates the creation of Python scripts for installing, verifying, and maintaining Windows desktop applications. It is designed to solve the "Application Compatibility Testing" bottleneck by eliminating manual scripting.

The system uses a 3-phase approach:
1.  **Introspection**: Analyzes the installer file to detect if it's an MSI or EXE and finds "silent install" switches (like `/qn` or `/S`).
2.  **Generation**: Automatically writes a Python script that handles the installation process, including error checking and logging.
3.  **Self-Healing**: If a script fails during execution (e.g., due to a timeout), the system attempts to diagnose and patch the script automatically.

---

## Prerequisites
- **OS**: Windows 10 or 11 (Required for `pywinauto` and `msilib`).
- **Python**: Version 3.10 or higher.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repo_url>
    cd ai_automation_script_gen
    ```

2.  **Install Dependencies**:
    The only external dependency is `pywinauto` for GUI automation.
    ```bash
    pip install -r requirements.txt
    ```

---

## How to Use

### 1. Where to put your installers
You can place your `.exe` or `.msi` installer files anywhere, but for simplicity, we recommend creating a `setups` folder in this directory.
*   `C:\Path\To\Repo\setups\installer.exe`

### 2. Generating a Script
Open your terminal (PowerShell or Command Prompt) and run:

```bash
python main.py <path_to_installer>
```

**Example:**
```bash
python main.py setups/7zip.msi
```

**What happens?**
*   The tool inspects `7zip.msi`.
*   It detects it is an MSI.
*   It generates a file named `install_7zip.msi.py` in the current directory.
*   It prints the analysis to the console.

### 3. Running the Generated Script
You can now use the generated script in your automation pipeline or run it manually to install the app:

```bash
python install_7zip.msi.py
```

### 4. Using Self-Healing Mode
If you are developing a script and it is failing (e.g., timing out), use the `--heal` flag.

```bash
python main.py setups/heavy_app.exe --heal
```

**What happens?**
1.  Generates the script.
2.  Immediately runs the script.
3.  If it fails, it analyzes the error log.
4.  It patches the code (e.g., increases timeout) and retries.
5.  Saves the fixed version if successful.

---

## Demo: Try it right now
The project comes with a `dummy_setup.exe` and a `demo_healing.py` to show you how it works without needing a real installer.

**Step 1: Analyze the dummy installer**
```bash
python main.py dummy_setup.exe
```
*Output: detects the `/S` flag inside the dummy file and writes `install_dummy_setup.exe.py`.*

**Step 2: Watch Self-Healing in action**
```bash
python demo_healing.py
```
*Output: Simulates a broken script, catches the timeout, fixes it, and verify the fix works.*

---

## Customization (For Developers)

### Adding new "Silent Flags"
If you find an installer that uses a weird flag (e.g., `/very-quiet`) that isn't detecting:
1.  Open `lib/introspect.py`.
2.  Add the string to the `possible_flags` list in the `_analyze_exe` method.

### Tweaking GUI Logic
If you want to change which buttons are clicked during GUI automation:
1.  Open `lib/llm_client.py`.
2.  Edit the `decide_next_action` method.
3.  Add new keywords to the `priorities` list (e.g., "Install Now").

---

## Project Structure

*   `main.py`: The entry point for the tool.
*   `lib/`
    *   `introspect.py`: Static analysis engine (looks inside files).
    *   `generator.py`: Writes the Python code.
    *   `healer.py`: Logic for the run-fail-fix loop.
    *   `gui_automator.py`: `pywinauto` wrapper for driving UI.
    *   `llm_client.py`: The decision engine (Brain).
*   `requirements.txt`: List of python packages.