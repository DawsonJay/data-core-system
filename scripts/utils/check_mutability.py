#!/usr/bin/env python3
"""
Folder Mutability Checker
Utility script to check the mutability status of any folder in the data-core system.
"""

import os
import sys

def check_folder_mutability(folder_path):
    """
    Check folder mutability status from README.md
    
    Returns:
        'fixed' - Can create files, cannot modify/delete existing files  
        'unfixed' - Can create, modify, delete files
    
    Raises SystemExit with specific error if status cannot be determined.
    """
    readme_path = os.path.join(folder_path, "README.md")
    
    if not os.path.exists(readme_path):
        print(f"[CRITICAL] README.md missing in folder: {folder_path}")
        print(f"Current working directory: {os.getcwd()}")
        print("This folder must have a README.md with clear mutability status.")
        sys.exit(1)
    
    try:
        with open(readme_path, 'r') as f:
            content = f.read()
            
        # Check for explicit status indicators
        if "Status: FIXED" in content:
            return 'fixed'
        elif "Status: UNFIXED" in content or "Status: NOT FINALIZED" in content or "MUTABLE" in content:
            return 'unfixed'
        else:
            print(f"[CRITICAL] Unclear mutability status in README: {readme_path}")
            print(f"README content does not contain clear 'Status: FIXED' or 'Status: UNFIXED'")
            print("Please add explicit status to README.md")
            sys.exit(1)
                
    except Exception as e:
        print(f"[CRITICAL] Cannot read README.md in folder: {folder_path}")
        print(f"Error: {e}")
        print(f"Current working directory: {os.getcwd()}")
        print("This indicates a file system or permissions problem.")
        sys.exit(1)

def validate_folder_operations(folder_path, operation_type):
    """
    Validate if an operation is allowed in the given folder.
    
    Args:
        folder_path: Path to the folder
        operation_type: 'create', 'modify', or 'delete'
    
    Returns:
        (bool, str): (is_allowed, reason)
    """
    mutability = check_folder_mutability(folder_path)
    
    if mutability == 'fixed':
        if operation_type == 'create':
            return True, f"Folder is FIXED - creating files is allowed"
        else:
            return False, f"Folder is FIXED - {operation_type} operations not allowed on existing files"
    else:  # unfixed
        return True, f"Folder is UNFIXED - {operation_type} operations allowed"

def main():
    """Main function for command line usage."""
    if len(sys.argv) < 2:
        print("Usage: python check_mutability.py <folder_path> [operation_type]")
        print("\nExamples:")
        print("  python check_mutability.py chats")
        print("  python check_mutability.py chats create")
        print("  python check_mutability.py frameworks modify")
        return
    
    folder_path = sys.argv[1]
    operation_type = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(folder_path):
        print(f"✗ ERROR: Folder '{folder_path}' does not exist")
        return
    
    print(f"Checking mutability for folder: {folder_path}")
    print("=" * 50)
    
    try:
        mutability = check_folder_mutability(folder_path)
        print(f"Status: {mutability.upper()}")
        
        if operation_type:
            print(f"\nOperation: {operation_type}")
            can_do, op_reason = validate_folder_operations(folder_path, operation_type)
            if can_do:
                print(f"✓ ALLOWED: {op_reason}")
            else:
                print(f"✗ DENIED: {op_reason}")
        
        print(f"\nRules for {mutability.upper()} folders:")
        if mutability == 'unfixed':
            print("  ✓ Create files")
            print("  ✓ Modify existing files")
            print("  ✓ Delete files")
        else:  # fixed
            print("  ✓ Create files")
            print("  ✗ Modify existing files")
            print("  ✗ Delete files")
            
    except SystemExit:
        # Error already displayed and system exited
        pass

if __name__ == "__main__":
    main()
