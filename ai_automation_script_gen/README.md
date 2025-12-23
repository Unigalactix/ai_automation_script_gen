# AI-Driven Automation Script Generator

## Overview
This tool automates the creation of **PowerShell** scripts for installing, verifying, and maintaining Windows desktop applications. It is designed to solve the "Application Compatibility Testing" bottleneck by eliminating manual scripting.

The system is **Microsoft Native Friendly**: providing Python-based orchestration that generates pure PowerShell/DOTNET automation artifacts.

---

## Architecture

```mermaid
graph TD
    User[User] -->|Run python main.py| Main[main.py]
    
    subgraph Selection
    Main -->|No Args| Menu[Interactive Menu]
    Menu -->|Scan| Setups[setups/ folder]
    Main -->|With Args| Input[Specific File]
    end
    
    subgraph Analysis & Generation
    Menu --> Input
    Input --> Analyzer[StaticAnalyzer (introspect.py)]
    Analyzer -->|MSI Header / EXE Strings| Props[Installer Properties]
    Props --> Generator[ScriptGenerator (generator.py)]
    
    subgraph "GUI Bridge (Phase 2)"
    Generator -->|If GUI| Automator[gui_automator.py]
    Automator -->|Executes| PSInspector[ui_inspector.ps1]
    PSInspector -->|Return .NET UI Tree| Automator
    Automator -->|Events| Generator
    end
    
    Generator -->|Synthesize| Output[PowerShell Script (.ps1)]
    end
```

---

## Prerequisites
- **OS**: Windows 10 or 11.
- **Python**: Version 3.10 or higher.
- **PowerShell**: Version 5.1 or higher (Pre-installed on Windows).

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repo_url>
    cd ai_automation_script_gen
    ```

2.  **Dependencies**:
    This project has **Zero External Pip Dependencies**. It relies solely on the standard library and native Windows binaries.

---

## How to Use

### 1. Place Installers
Put your `.exe` or `.msi` files into the `setups` folder.
*   `ai_automation_script_gen/setups/`

### 2. Run the Tool (Interactive Mode)
Simply run the script without arguments to see a menu of available installers.

```bash
python main.py
```

**Example Session:**
```text
No installer path provided.

Available Installers in '.../setups':
[1] dummy_setup.exe
[2] eclipse-inst-jre-win64.exe

Select an installer number (or 'q' to quit): 2
```

### 3. CLI Mode (Advanced)
You can still target a specific file directly:

```bash
python main.py setups/my_app.exe
```

### 4. The Output
The tool will generate a **PowerShell Script** in the current directory:
*   `install_dummy_setup.exe.ps1`
*   `install_eclipse-inst-jre-win64.exe.ps1`

You can run these scripts directly in PowerShell to perform the installation.

---

## Features

### Phase 1: Silent Install Detection
*   Analyzes MSIs for `ProductCode`.
*   Scans EXEs for known silent flags (`/S`, `/VERYSILENT`, `/qn`).
*   Generates a wrapper script that handles logging and error codes.

### Phase 2: Native GUI Automation
*   For installers that *require* clicking buttons ("Next", "I Agree").
*   Uses a custom **PowerShell Bridge** (`ui_inspector.ps1`) to access the Windows UI Automation API (System.Windows.Automation).
*   No need for `pywinauto` or other heavy Python libraries.

### Phase 3: Self-Healing (Beta)
*   The system can analyze execution logs and patch the script automatically (e.g., increasing timeouts).
*   *Note: Currently disabled while migrating healing logic to PowerShell.*

---

## Project Structure

*   `main.py`: Entry point & Interactive Menu.
*   `lib/`
    *   `introspect.py`: Static analysis engine.
    *   `generator.py`: Generates the `.ps1` code.
    *   `gui_automator.py` & `ui_inspector.ps1`: The Hybrid Python/.NET bridge for reading UI trees.
    *   `llm_client.py`: The decision engine.
*   `setups/`: Default folder for placing installers.