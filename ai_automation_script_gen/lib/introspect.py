import os
import logging
import re
try:
    import msilib
except ImportError:
    msilib = None
    # Can't log yet if logging isn't configured, but usually it works if imported.
    # Actually, let's just use print or ignore since we are at top level.
    pass

class StaticAnalyzer:
    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path)
        self.file_type = self._detect_type()

    def _detect_type(self):
        if self.file_path.lower().endswith(".msi"):
            return "msi"
        elif self.file_path.lower().endswith(".exe"):
            return "exe"
        else:
            return "unknown"

    def analyze(self):
        results = {
            "type": self.file_type,
            "path": self.file_path,
            "properties": {},
            "silent_flags": []
        }

        if self.file_type == "msi":
            results.update(self._analyze_msi())
        elif self.file_type == "exe":
            results.update(self._analyze_exe())
        
        return results

    def _analyze_msi(self):
        props = {}
        if msilib:
            try:
                db = msilib.OpenDatabase(self.file_path, msilib.MSIDBOPEN_READONLY)
                view = db.OpenView("SELECT Property, Value FROM Property")
                view.Execute(None)
                record = view.Fetch()
                while record:
                    props[record.GetString(1)] = record.GetString(2)
                    record = view.Fetch()
            except Exception as e:
                logging.error(f"Failed to analyze MSI: {e}")
                return {"error": str(e)}
        else:
             props = {"Note": "Deep introspection unavailable (msilib missing)"}
        
        # MSI always supports standard flags
        return {
            "properties": props, 
            "silent_flags": ["/qn", "/norestart"],
            "install_cmd": f'msiexec /i "{self.file_path}" /qn /norestart'
        }

    def _analyze_exe(self):
        # Static analysis: Search for common flag patterns in the binary strings
        # This is safer than executing an unknown generic installer
        
        possible_flags = [
            "/S", "/silent", "/q", "/quiet", "-q", "--silent", "/verysilent", "/supressmsgboxes"
        ]
        found_flags = []
        
        try:
            with open(self.file_path, 'rb') as f:
                # Read first 5MB is usually enough for header/strings
                content = f.read(5 * 1024 * 1024) 
                
                # Check for ASCII and UTF-16LE encoding of flags
                for flag in possible_flags:
                    # Some installers like NSIS use /S (case sensitive)
                    # Others might be case insensitive. 
                    if flag.encode('ascii') in content or flag.encode('utf-16le') in content:
                        found_flags.append(flag)
                        
        except Exception as e:
            logging.error(f"Failed to read EXE: {e}")

        # Heuristic for command construction
        cmd = f'"{self.file_path}"'
        if found_flags:
            # Pick the most "standard" looking one or just the first found
            # NSIS usually prefers /S. InstallShield /s /v"/qn". Inno Setup /VERYSILENT
            
            # Priority logic
            if "/S" in found_flags: # NSIS strong signal
                cmd += " /S"
            elif "/VERYSILENT" in found_flags: # Inno Setup
                cmd += " /VERYSILENT /SUPPRESSMSGBOXES /NORESTART"
            else:
                cmd += f" {found_flags[0]}"
        
        return {"silent_flags": found_flags, "install_cmd": cmd}
