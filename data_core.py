#!/usr/bin/env python3
"""
Data Core Master Script
Simple interface for data-core operations.
"""

import sys
import os
import subprocess

def save_chat():
    """Save chat using the AI-first chat save process with memory files."""
    print("=" * 60)
    print("DATA CORE - AI-FIRST CHAT SAVE PROCESS")
    print("=" * 60)
    print("Auto-extracts conversation from memory files and creates Framework v2.0 reports.")
    print("Zero manual intervention required - designed for AI systems.")
    print("\nStarting AI-first chat save process...")
    
    # Call the AI-first chat save process (no arguments needed - it auto-discovers memory files)
    script_path = os.path.join("processes", "chats", "save_chat.py")
    if os.path.exists(script_path):
        try:
            result = subprocess.run([sys.executable, script_path], 
                                 check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Chat save process failed: {e}")
    else:
        print(f"Error: Chat save script not found at {script_path}")

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
    """Commit changes with data protection using the Git commit process."""
    print("=" * 60)
    print("DATA CORE - GIT COMMIT PROCESS")
    print("=" * 60)
    print("This will save current chat, create tiered backups, then commit safely.")
    print("Data protection first - zero information loss principle maintained.")
    print("\nStarting Git commit process...")
    
    # Get live conversation context (this will be provided by AI)
    if len(sys.argv) < 3:
        print("Error: This process requires live conversation context")
        print("Usage: python data_core.py commit \"live conversation context\"")
        return
    
    live_context = sys.argv[2]
    
    # Call the git commit process
    script_path = os.path.join("processes", "git_commit.py")
    if os.path.exists(script_path):
        try:
            result = subprocess.run([sys.executable, script_path, live_context], 
                                 check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Git commit process failed: {e}")
    else:
        print(f"Error: Git commit script not found at {script_path}")

def main():
    if len(sys.argv) > 1:
        if len(sys.argv) > 1 and sys.argv[1] == "save" and len(sys.argv) > 2 and sys.argv[2] == "chat":
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
        print("  python data_core.py save chat                    - AI-first chat capture from memory files")
        print("  python data_core.py validate memory --file <path> - Validate chat memory files")
        print()
        print("🔍 HEALTH MONITORING:")
        print("  python data_core.py health [\"context\"]      - Comprehensive system health check")
        print()
        print("🔐 GIT OPERATIONS:")
        print("  python data_core.py commit \"live context\"   - Backup + commit with data protection")
        print()
        print("📊 PROCESS DETAILS:")
        print()
        print("AI-First Chat Save Process:")
        print("  ✓ Auto-extract conversation from memory files (no manual input)")
        print("  ✓ Framework v2.0 compliance with intelligent content analysis")
        print("  ✓ Comprehensive validation and file integrity verification")
        print("  ✓ Health checks and timeline analysis for continuity")
        print("  ✓ Zero information loss with gap detection")
        print("  ✓ Automatic backup creation before memory cleanup")
        print("  ✓ Verbose progress reporting for full transparency")
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
        print("  ✓ Framework v2.0 compliance verification")
        print("  ✓ Live context alignment validation (optional)")
        print("  ✓ File integrity and continuity analysis")
        print("  ✓ Detailed reporting with actionable insights")
        print("  ✓ Dual-time display: local time with GMT reference for better UX")
        print()
        print("Git Commit Process:")
        print("  ✓ Save current chat first (zero-gap principle)")
        print("  ✓ Analyze changes and suggest backup level (major/standard/minor)")
        print("  ✓ Create backup branch on GitHub before committing")
        print("  ✓ Auto-generate commit message from chat and changes")
        print("  ✓ Only commit after successful backup creation")
        print("  ✓ Keep last 5 backups of each type")
        print("  ✓ Data protection first - fail hard if chat save fails")

if __name__ == "__main__":
    main()
