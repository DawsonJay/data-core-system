#!/usr/bin/env python3
"""
Data Core Master Script
Simple interface for data-core operations.
"""

import sys
import os
import subprocess

def save_chat():
    """Save a chat report using the chat process."""
    print("=" * 60)
    print("DATA CORE - CHAT SAVE PROCESS")
    print("=" * 60)
    print("This will create a new chat report with ACTUAL CONTENT capture.")
    print("The script will guide you through entering content for each section.")
    print("All content will be validated and integrity-checked before saving.")
    print("\nStarting chat save process...")
    
    # Call the chat save process
    script_path = os.path.join("processes", "chats", "save_chat.py")
    if os.path.exists(script_path):
        try:
            result = subprocess.run([sys.executable, script_path], 
                                 capture_output=True, text=True, check=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}")
    else:
        print(f"Error: Chat save script not found at {script_path}")

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
    if len(sys.argv) > 2:
        if sys.argv[1] == "save" and sys.argv[2] == "chat":
            save_chat()
        elif sys.argv[1] == "commit":
            git_commit()
        else:
            print("Unknown command")
    else:
        print("Data Core System - Portfolio Building for Canadian Express Entry")
        print("=" * 60)
        print("Available commands:")
        print()
        print("📝 DATA OPERATIONS:")
        print("  python data_core.py save chat               - Create new chat report")
        print()
        print("🔐 GIT OPERATIONS:")
        print("  python data_core.py commit \"live context\"   - Backup + commit with data protection")
        print()
        print("📊 PROCESS DETAILS:")
        print()
        print("Chat Save Process:")
        print("  ✓ Capture actual conversation content (not empty templates)")
        print("  ✓ Validate all required sections are filled")
        print("  ✓ Ensure content integrity and completeness")
        print("  ✓ Follow the Chat Report Framework")
        print("  ✓ Check for gaps with previous reports")
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
