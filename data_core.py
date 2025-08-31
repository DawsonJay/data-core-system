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

def git_backup_commit():
    """Perform Git backup and commit with data protection."""
    if len(sys.argv) < 4:
        print("=" * 60)
        print("DATA CORE - GIT BACKUP & COMMIT")
        print("=" * 60)
        print("Usage: python data_core.py git commit \"Your commit message\"")
        print("\nThis process will:")
        print("  ✓ Create comprehensive local backups")
        print("  ✓ Create Git branch backups")  
        print("  ✓ Create compressed archive backups")
        print("  ✓ Validate all backups before committing")
        print("  ✓ Perform Git commit with validation")
        print("  ✓ Push changes to remote repository")
        print("  ✓ Clean up old backups")
        print("\nData protection strategies ensure zero data loss.")
        return
    
    commit_message = sys.argv[3]
    script_path = os.path.join("processes", "git_backup_commit.py")
    if os.path.exists(script_path):
        try:
            result = subprocess.run([sys.executable, script_path, commit_message], 
                                 check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Git backup and commit failed: {e}")
    else:
        print(f"Error: Git backup script not found at {script_path}")

def git_backup_only():
    """Create comprehensive backups without committing."""
    if len(sys.argv) < 4:
        print("=" * 60)
        print("DATA CORE - GIT BACKUP ONLY")
        print("=" * 60)
        print("Usage: python data_core.py git backup \"Backup description\"")
        print("\nThis process will:")
        print("  ✓ Create comprehensive local backups")
        print("  ✓ Create Git branch backups")
        print("  ✓ Create compressed archive backups")
        print("  ✓ Validate all backup integrity")
        print("  ✓ Clean up old backups")
        print("\nNo Git commit will be performed - backups only.")
        return
    
    backup_description = sys.argv[3]
    script_path = os.path.join("processes", "git_backup_commit.py")
    if os.path.exists(script_path):
        try:
            result = subprocess.run([sys.executable, script_path, backup_description, "--backup-only"], 
                                 check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Git backup failed: {e}")
    else:
        print(f"Error: Git backup script not found at {script_path}")

def main():
    if len(sys.argv) > 2:
        if sys.argv[1] == "save" and sys.argv[2] == "chat":
            save_chat()
        elif sys.argv[1] == "git" and sys.argv[2] == "commit":
            git_backup_commit()
        elif sys.argv[1] == "git" and sys.argv[2] == "backup":
            git_backup_only()
        else:
            print("Unknown command")
    else:
        print("Data Core System - Portfolio Building for Canadian Express Entry")
        print("=" * 60)
        print("Available commands:")
        print()
        print("📝 DATA OPERATIONS:")
        print("  python data_core.py save chat           - Create new chat report with content capture")
        print()
        print("🔐 GIT OPERATIONS:")
        print("  python data_core.py git commit \"msg\"    - Comprehensive backup + Git commit")
        print("  python data_core.py git backup \"desc\"   - Create backups only (no commit)")
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
        print("Git Backup & Commit Process:")
        print("  ✓ Create local directory backups with timestamp")
        print("  ✓ Create Git branch backups on remote")
        print("  ✓ Create compressed archive backups")
        print("  ✓ Validate backup integrity before commit")
        print("  ✓ Perform Git commit with validation")
        print("  ✓ Push changes to remote repository")
        print("  ✓ Clean up old backups automatically")
        print("  ✓ Multiple backup strategies ensure zero data loss")

if __name__ == "__main__":
    main()
