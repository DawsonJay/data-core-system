#!/usr/bin/env python3
"""
Data Core Master Script
Simple interface for data-core operations.
"""

import sys
import os
import subprocess

def save_chat():
    """Save a chat report using AI-first chat process with auto-extraction."""
    print("=" * 60)
    print("DATA CORE - AI-FIRST CHAT SAVE PROCESS")
    print("=" * 60)
    print("Auto-extracts live conversation and creates Framework v2.0 reports.")
    print("Zero manual intervention required - designed for AI systems.")
    print("\nStarting AI-first chat save process...")
    
    # Check for file input or direct conversation context
    if len(sys.argv) < 3:
        print("Error: This process requires live conversation context")
        print("Usage: python data_core.py save chat \"live conversation context\"")
        print("   or: python data_core.py save chat --file conversation.txt")
        return
    
    # Check if using file input
    if len(sys.argv) >= 4 and sys.argv[3] == "--file":
        if len(sys.argv) < 5:
            print("Error: --file requires a file path")
            print("Usage: python data_core.py save chat --file conversation.txt")
            return
        
        file_path = sys.argv[4]
        if not os.path.exists(file_path):
            print(f"Error: Conversation file not found: {file_path}")
            return
        
        try:
            with open(file_path, 'r') as f:
                live_context = f.read()
            print(f"✓ Loaded conversation from file: {file_path}")
        except Exception as e:
            print(f"Error reading conversation file: {e}")
            return
    else:
        # Direct conversation context (backward compatibility)
        live_context = sys.argv[3]
    
    # Call the AI-first chat save process
    script_path = os.path.join("processes", "chats", "save_chat.py")
    if os.path.exists(script_path):
        try:
            result = subprocess.run([sys.executable, script_path, live_context], 
                                 check=True)
            
            # Clean up temp file if it was used
            if len(sys.argv) >= 4 and sys.argv[3] == "--file":
                try:
                    os.remove(file_path)
                    print(f"✓ Cleaned up temp file: {file_path}")
                except Exception as e:
                    print(f"⚠ Warning: Could not clean up temp file {file_path}: {e}")
                    
        except subprocess.CalledProcessError as e:
            print(f"Error: Chat save process failed: {e}")
    else:
        print(f"Error: Chat save script not found at {script_path}")

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
        if len(sys.argv) > 2 and sys.argv[1] == "save" and sys.argv[2] == "chat":
            save_chat()
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
        print("  python data_core.py save chat \"User: [msg]\\nAssistant: [response]...\"  - AI-first chat capture")
        print("  python data_core.py save chat --file conversation.txt                    - AI-first chat capture from file")
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
        print("  ✓ Auto-extract live conversation context (no manual input)")
        print("  ✓ Framework v1.1 compliance with intelligent content analysis")
        print("  ✓ Comprehensive validation and file integrity verification")
        print("  ✓ Health checks and timeline analysis for continuity")
        print("  ✓ Zero information loss with gap detection")
        print("  ✓ Verbose progress reporting for full transparency")
        print()
        print("AI-First Health Check Process:")
        print("  ✓ Comprehensive chat system health monitoring")
        print("  ✓ Proactive issue detection and timeline validation")
        print("  ✓ Framework v1.1 compliance verification")
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
