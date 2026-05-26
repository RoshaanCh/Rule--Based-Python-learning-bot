#!/usr/bin/env python3
"""
My Python Buddy - Cross-platform Launcher
Works on Windows, macOS, and Linux
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def run_command(command, shell=False):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(
            command if isinstance(command, list) else command.split(),
            shell=shell,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def main():
    print("""
╔════════════════════════════════════════╗
║   My Python Buddy - Launcher Script    ║
╚════════════════════════════════════════╝
    """)
    
    # Check Python version
    print("[*] Checking Python version...")
    if sys.version_info < (3, 8):
        print(f"[ERROR] Python 3.8+ required. You have {sys.version}")
        sys.exit(1)
    print(f"[OK] Python {sys.version.split()[0]} detected")
    print()
    
    # Get project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Create virtual environment
    venv_path = project_root / "venv"
    if not venv_path.exists():
        print("[*] Creating virtual environment...")
        success, output = run_command([sys.executable, "-m", "venv", "venv"])
        if not success:
            print(f"[ERROR] Failed to create virtual environment:\n{output}")
            sys.exit(1)
        print("[OK] Virtual environment created")
        print()
    
    # Get Python executable in venv
    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else:
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
    
    # Install dependencies
    print("[*] Installing dependencies...")
    success, output = run_command([str(pip_exe), "install", "-q", "-r", "requirements.txt"])
    if not success:
        print(f"[ERROR] Failed to install dependencies:\n{output}")
        sys.exit(1)
    print("[OK] Dependencies installed")
    print()
    
    # Start the application
    print("""
╔════════════════════════════════════════╗
║   Backend Server Running               ║
╚════════════════════════════════════════╝

  API Server: http://127.0.0.1:5000
  Frontend:   Open index.html in your browser

  Press Ctrl+C to stop the server

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    # Run Flask app
    subprocess.run([str(python_exe), "app.py"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
