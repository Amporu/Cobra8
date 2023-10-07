class SelectPython:
    import tkinter as tk
from tkinter import ttk
import subprocess
import platform
class SelectPython:
    def get_python_versions():
        python_versions = set()
        
        # Determine the appropriate command to list Python versions based on the OS
        system_name = platform.system()
        if system_name == 'Linux':
            # Linux default Python versions
            python_versions.update(["/usr/bin/python2.7", "/usr/bin/python3"])
            
            # Check Homebrew installations (if Homebrew is installed)
            try:
                homebrew_python_versions = subprocess.getoutput("brew list --formula | grep python").splitlines()
                python_versions.update(homebrew_python_versions)
            except:
                pass
        elif system_name == 'Windows':
            # Check for Python installations in common locations on Windows
            windows_python_versions = subprocess.getoutput("dir C:\\Python* /B /AD").splitlines()
            python_versions.update(windows_python_versions)
        elif system_name == 'Darwin':
            # macOS default Python versions
            python_versions.update(["/usr/bin/python2.7", "/usr/bin/python3"])
            
            # Check Homebrew installations (if Homebrew is installed)
            try:
                homebrew_python_versions = subprocess.getoutput("brew list --formula | grep python").splitlines()
                python_versions.update(homebrew_python_versions)
            except:
                pass
        
    

        # Remove "@" character from all Python versions
        python_versions = [version.replace("@", "") for version in python_versions]
        
        return sorted(python_versions)

