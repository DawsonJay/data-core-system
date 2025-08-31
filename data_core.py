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

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "save" and sys.argv[2] == "chat":
        save_chat()
    else:
        print("Data Core System - Portfolio Building for Canadian Express Entry")
        print("=" * 60)
        print("Available commands:")
        print("  python data_core.py save chat  - Create new chat report with content capture")
        print("\nThe chat save process will:")
        print("  ✓ Capture actual conversation content (not empty templates)")
        print("  ✓ Validate all required sections are filled")
        print("  ✓ Ensure content integrity and completeness")
        print("  ✓ Follow the Chat Report Framework")
        print("  ✓ Check for gaps with previous reports")

if __name__ == "__main__":
    main()
