#!/usr/bin/env python3
"""
Data Core Master Script
Simple interface for data-core operations.
"""

import sys
import os
import subprocess

def save_chat():
    """Real-time value capture system - no save process needed."""
    print("=" * 60)
    print("DATA CORE - REAL-TIME VALUE CAPTURE SYSTEM")
    print("=" * 60)
    print("The save process has been replaced with real-time value capture.")
    print("AI automatically creates chat records when valuable content is identified.")
    print("\nNo manual save process needed - system operates automatically.")
    print("See MEMORY.md and chats/system/framework.md for details.")

def validate_memory():
    """Validate chat memory files using the validation process."""
    print("=" * 60)
    print("DATA CORE - MEMORY VALIDATION PROCESS")
    print("=" * 60)
    print("Validates chat memory files for format compliance and gapless history.")
    print("Ensures zero information loss and perfect conversation continuity.")
    print("\nStarting memory validation process...")
    
    # Get memory file path
    if len(sys.argv) < 4:
        print("Error: Memory file path required")
        print("Usage: python data_core.py validate memory --file <memory_file_path>")
        return
    
    if sys.argv[3] != "--file":
        print("Error: Invalid syntax")
        print("Usage: python data_core.py validate memory --file <memory_file_path>")
        return
    
    memory_file_path = sys.argv[4]
    
    # Call the validation process
    script_path = os.path.join("processes", "chats", "validate_memory.py")
    if os.path.exists(script_path):
        try:
            result = subprocess.run([sys.executable, script_path, memory_file_path], 
                                 check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Memory validation failed: {e}")
    else:
        print(f"Error: Validation script not found at {script_path}")

def health_check():
    """Run comprehensive health check using AI-first health monitoring process."""
    print("=" * 60)
    print("DATA CORE - AI-FIRST HEALTH CHECK PROCESS")
    print("=" * 60)
    print("Comprehensive chat system health monitoring with proactive issue detection.")
    print("Zero manual intervention required - designed for AI systems.")
    print("\nStarting AI-first health check process...")
    
    # Get live conversation context if available (optional for health checks)
    live_context = None
    if len(sys.argv) >= 3:
        live_context = sys.argv[2]
    
    # Call the AI-first health check process
    script_path = os.path.join("processes", "chats", "chat_health_check.py")
    if os.path.exists(script_path):
        try:
            if live_context:
                result = subprocess.run([sys.executable, script_path, live_context], 
                                     check=True)
            else:
                result = subprocess.run([sys.executable, script_path], 
                                     check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Health check process failed: {e}")
    else:
        print(f"Error: Health check script not found at {script_path}")

def git_commit():
    """Git commit functionality temporarily removed during system transformation."""
    print("=" * 60)
    print("DATA CORE - GIT COMMIT PROCESS")
    print("=" * 60)
    print("Git commit functionality has been temporarily removed.")
    print("Use standard git commands for now: git add, git commit, git push")
    print("\nThis will be reimplemented when the new system architecture is ready.")

def main():
    if len(sys.argv) > 1:
        if len(sys.argv) > 1 and sys.argv[1] == "save" and len(sys.argv) > 2 and sys.argv[2] == "chat":
            print("Note: Save process replaced with real-time value capture. See MEMORY.md for details.")
            save_chat()
        elif len(sys.argv) > 2 and sys.argv[1] == "validate" and sys.argv[2] == "memory":
            validate_memory()
        elif sys.argv[1] == "commit":
            git_commit()
        elif sys.argv[1] == "health":
            health_check()
        else:
            print("Unknown command")
    else:
        print("Data Core System - Portfolio Building for Canadian Express Entry")
        print("=" * 60)
        print("Available commands:")
        print()
        print("📝 DATA OPERATIONS:")
        print("  python data_core.py save chat                    - Note: Replaced with real-time value capture")
        print("  python data_core.py validate memory --file <path> - Validate chat memory files")
        print()
        print("🔍 HEALTH MONITORING:")
        print("  python data_core.py health [\"context\"]      - Comprehensive system health check")
        print()
        print("🔐 GIT OPERATIONS:")
        print("  python data_core.py commit                   - Note: Temporarily removed during system transformation")
        print()
        print("📊 PROCESS DETAILS:")
        print()
        print("Real-Time Value Capture System:")
        print("  ✓ AI automatically creates chat records when value is identified")
        print("  ✓ Framework v3.0 compliance with real-time capture")
        print("  ✓ No save process needed - immediate creation of records")
        print("  ✓ Learning system continuously improves capture quality")
        print("  ✓ Zero workflow disruption - natural conversation flow")
        print("  ✓ Gapless history maintained through validation")
        print("  ✓ Professional portfolio-ready documentation")
        print()
        print("Memory Validation Process:")
        print("  ✓ Format compliance validation (User:/Assistant: pattern)")
        print("  ✓ Gapless history verification (continuous conversation)")
        print("  ✓ Content integrity checks (file corruption detection)")
        print("  ✓ Comprehensive error reporting with recovery guidance")
        print("  ✓ System strengthening recommendations after failures")
        print()
        print("AI-First Health Check Process:")
        print("  ✓ Comprehensive chat system health monitoring")
        print("  ✓ Proactive issue detection and timeline validation")
        print("  ✓ Framework v3.0 compliance verification")
        print("  ✓ Live context alignment validation (optional)")
        print("  ✓ File integrity and continuity analysis")
        print("  ✓ Detailed reporting with actionable insights")
        print("  ✓ Dual-time display: local time with GMT reference for better UX")
        print()


if __name__ == "__main__":
    main()
