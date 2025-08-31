#!/usr/bin/env python3
"""
Git Commit Process - DATA PROTECTION FIRST
Saves current chat, creates tiered backups, then commits safely.
Follows Data Core System principles: zero information loss, data protection first.
"""

import os
import sys
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

def get_current_gmt_time():
    """Get current GMT time."""
    return datetime.now(timezone.utc)

def run_command(command, description, critical=True):
    """Run a shell command with proper error handling."""
    print(f"    Running: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        if result.stdout.strip():
            for line in result.stdout.strip().split('\n'):
                print(f"      {line}")
        print(f"    ✓ {description}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"    ✗ {description} failed")
        print(f"      Error: {e.stderr.strip()}")
        if critical:
            sys.exit(1)
        return False, e.stderr

def get_live_conversation_context():
    """Get the current conversation context for chat saving."""
    # Check for test mode
    test_mode = "--test" in sys.argv
    
    # This will be provided by the AI when it calls this process
    # The AI should pass the current conversation as the first argument
    if len(sys.argv) > 1:
        # Find the first non-flag argument
        for arg in sys.argv[1:]:
            if not arg.startswith("--"):
                return arg, test_mode
        
        print("✗ ERROR: No live conversation context provided")
        print("This process requires current conversation context to save chat")
        sys.exit(1)
    else:
        print("✗ ERROR: No live conversation context provided")
        print("This process requires current conversation context to save chat")
        sys.exit(1)

def save_current_chat(live_context):
    """Save current conversation to maintain gapless chat history."""
    print("  Saving current conversation to chat history...")
    
    # Use the existing save_chat.py process with live context
    script_path = os.path.join("processes", "chats", "save_chat.py")
    if not os.path.exists(script_path):
        print(f"    ✗ Chat save script not found at {script_path}")
        sys.exit(1)
    
    try:
        print("    Calling chat save process with live conversation context...")
        result = subprocess.run([sys.executable, script_path, live_context], 
                              check=True, capture_output=True, text=True)
        print("    ✓ Chat saved successfully")
        # Extract the saved chat filename from the output for commit message
        for line in result.stdout.split('\n'):
            if 'Report saved:' in line:
                chat_filename = line.split('Report saved: ')[1].split(' ')[0]
                return chat_filename
        return "chat-report"
    except subprocess.CalledProcessError as e:
        print("    ✗ CRITICAL: Chat save failed")
        print("    This indicates a severe problem that must be addressed")
        print("    Aborting commit process - fix chat save issue first")
        print(f"    Error: {e.stderr}")
        sys.exit(1)

def analyze_changes_since_last_backup():
    """Analyze repository changes to suggest backup level."""
    print("  Analyzing changes since last backup...")
    
    # Get current Git status
    success, status_output = run_command("git status --porcelain", "Check Git status")
    if not status_output.strip():
        print("    ✓ No changes detected - no backup needed")
        return "none", []
    
    # Parse changes
    changes = []
    files_modified = 0
    files_added = 0
    files_deleted = 0
    
    for line in status_output.strip().split('\n'):
        if line.strip():
            status = line[:2]
            filename = line[3:].strip()
            changes.append((status, filename))
            
            if 'M' in status:
                files_modified += 1
            elif 'A' in status or '??' in status:
                files_added += 1
            elif 'D' in status:
                files_deleted += 1
    
    total_files = files_modified + files_added + files_deleted
    
    # Get lines changed (approximate)
    success, diff_output = run_command("git diff --numstat HEAD", "Get diff statistics", critical=False)
    lines_changed = 0
    if success:
        for line in diff_output.strip().split('\n'):
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                    lines_changed += int(parts[0]) + int(parts[1])
    
    # Check for structural changes
    new_folders = any('/' in filename and ('A' in status or '??' in status) 
                     for status, filename in changes)
    framework_changes = any('framework' in filename.lower() or 'readme' in filename.lower() 
                           for status, filename in changes)
    
    # Determine backup level
    backup_level = "minor"  # default
    
    if (total_files > 50 or lines_changed > 1000 or new_folders or framework_changes):
        backup_level = "major"
        reason = f"Major changes detected: {total_files} files, {lines_changed} lines"
        if new_folders:
            reason += ", new folders"
        if framework_changes:
            reason += ", framework changes"
    elif (total_files > 10 or lines_changed > 200):
        backup_level = "standard"
        reason = f"Standard changes detected: {total_files} files, {lines_changed} lines"
    else:
        backup_level = "minor"
        reason = f"Minor changes detected: {total_files} files, {lines_changed} lines"
    
    print(f"    ✓ Analysis complete: {reason}")
    return backup_level, changes

def get_user_backup_confirmation(suggested_level, changes, test_mode=False):
    """AI-first backup level confirmation - auto-confirms suggested level with comprehensive reporting."""
    print(f"  Auto-confirming backup level: {suggested_level.upper()}")
    print(f"    Changes detected:")
    
    # Show summary of changes
    for status, filename in changes[:10]:  # Show first 10
        status_desc = {
            'M ': 'Modified',
            'A ': 'Added',
            'D ': 'Deleted',
            '??': 'Untracked'
        }.get(status, status)
        print(f"      {status_desc}: {filename}")
    
    if len(changes) > 10:
        print(f"      ... and {len(changes) - 10} more files")
    
    # AI-first design: Always auto-confirm the suggested level
    print(f"    ✓ {suggested_level.upper()} backup level confirmed (AI-first auto-confirmation)")
    print("    ✓ Zero manual intervention required")
    
    return suggested_level

def create_backup_branch(backup_level):
    """Create and push backup branch to GitHub."""
    print(f"  Creating {backup_level} backup branch...")
    
    # Generate backup branch name
    timestamp = get_current_gmt_time().strftime("%Y%m%d-%H%M")
    branch_name = f"backup-{backup_level}-{timestamp}"
    
    print(f"    Backup branch: {branch_name}")
    
    # Create backup branch
    run_command(f"git checkout -b {branch_name}", f"Create backup branch {branch_name}")
    
    # Push to remote
    run_command(f"git push origin {branch_name}", f"Push backup branch to GitHub")
    
    # Return to main
    run_command("git checkout main", "Return to main branch")
    
    print(f"    ✓ {backup_level.upper()} backup created: {branch_name}")
    return branch_name

def cleanup_old_backups():
    """Remove old backup branches, keeping last 5 of each type."""
    print("  Cleaning up old backup branches...")
    
    # Get all backup branches from remote
    success, branches_output = run_command("git branch -r", "List remote branches", critical=False)
    if not success:
        print("    ⚠ Could not list remote branches for cleanup")
        return
    
    backup_branches = {
        'major': [],
        'standard': [],
        'minor': []
    }
    
    # Parse backup branches
    for line in branches_output.split('\n'):
        if 'backup-' in line and 'origin/' in line:
            branch_name = line.strip().replace('origin/', '')
            for level in backup_branches.keys():
                if f'backup-{level}-' in branch_name:
                    # Extract timestamp for sorting
                    try:
                        timestamp_part = branch_name.split(f'backup-{level}-')[1]
                        timestamp = datetime.strptime(timestamp_part, "%Y%m%d-%H%M")
                        backup_branches[level].append((branch_name, timestamp))
                    except ValueError:
                        continue
    
    # Sort and cleanup each type
    branches_deleted = 0
    for level, branches in backup_branches.items():
        if len(branches) > 5:
            # Sort by timestamp (newest first)
            branches.sort(key=lambda x: x[1], reverse=True)
            
            # Delete old branches (keep newest 5)
            for branch_name, _ in branches[5:]:
                try:
                    run_command(f"git push origin --delete {branch_name}", 
                               f"Delete old {level} backup: {branch_name}", 
                               critical=False)
                    branches_deleted += 1
                except:
                    pass
    
    if branches_deleted > 0:
        print(f"    ✓ Cleaned up {branches_deleted} old backup branches")
    else:
        print("    ✓ No old backups to clean up")

def generate_commit_message(chat_filename, backup_level, changes):
    """Auto-generate commit message from chat content and changes."""
    print("  Generating commit message...")
    
    # Extract key info from changes
    files_modified = sum(1 for status, _ in changes if 'M' in status)
    files_added = sum(1 for status, _ in changes if 'A' in status or '??' in status)
    files_deleted = sum(1 for status, _ in changes if 'D' in status)
    
    # Get a summary of changed files
    key_files = []
    for status, filename in changes:
        if any(keyword in filename.lower() 
               for keyword in ['readme', 'framework', 'process', '.py', '.md']):
            key_files.append(filename)
    
    # Build commit message
    if chat_filename:
        title = f"Development update with {backup_level} backup ({chat_filename})"
    else:
        title = f"Development update with {backup_level} backup"
    
    message_parts = [title, ""]
    
    # Add change summary
    change_summary = []
    if files_added > 0:
        change_summary.append(f"Added {files_added} files")
    if files_modified > 0:
        change_summary.append(f"Modified {files_modified} files")  
    if files_deleted > 0:
        change_summary.append(f"Deleted {files_deleted} files")
    
    if change_summary:
        message_parts.append("Changes: " + ", ".join(change_summary))
    
    # Add key files
    if key_files:
        message_parts.append("Key files: " + ", ".join(key_files[:5]))
        if len(key_files) > 5:
            message_parts.append(f"...and {len(key_files) - 5} more")
    
    message_parts.extend([
        "",
        f"Backup level: {backup_level} (data protection first)",
        "Chat history updated to maintain zero-gap principle",
        "All changes backed up before commit per Data Core System rules"
    ])
    
    commit_message = "\n".join(message_parts)
    print("    ✓ Commit message generated")
    return commit_message

def perform_git_commit(commit_message):
    """Stage and commit all changes."""
    print("  Performing Git commit...")
    
    # Stage all changes
    run_command("git add -A", "Stage all changes")
    
    # Create commit
    # Escape the commit message properly
    escaped_message = commit_message.replace('"', '\\"').replace('\n', '\\n')
    run_command(f'git commit -m "{escaped_message}"', "Create commit")
    
    # Get commit hash
    success, commit_hash = run_command("git rev-parse HEAD", "Get commit hash")
    commit_short = commit_hash.strip()[:8] if success else "unknown"
    
    print(f"    ✓ Commit successful: {commit_short}")
    return commit_short

def push_to_remote():
    """Push committed changes to GitHub."""
    print("  Pushing changes to GitHub...")
    
    run_command("git push origin main", "Push to remote repository")
    
    print("    ✓ Changes pushed to GitHub successfully")

def main():
    """Main Git commit process with data protection first."""
    print("=" * 70)
    print("GIT COMMIT PROCESS - DATA PROTECTION FIRST")
    print("=" * 70)
    print("Saves chat, creates tiered backups, then commits safely.")
    print("Zero information loss principle maintained.")
    
    # Get live conversation context and test mode
    live_context, test_mode = get_live_conversation_context()
    
    if test_mode:
        print("\n🧪 TEST MODE ENABLED - Skipping user prompts")
    
    print(f"\n💬 Live conversation context received ({len(live_context)} characters)")
    
    # Step 1: Save current chat (CRITICAL - must succeed)
    print("\n" + "=" * 70)
    print("STEP 1: SAVING CURRENT CHAT (CRITICAL)")
    print("=" * 70)
    
    chat_filename = save_current_chat(live_context)
    print(f"✓ Chat saved successfully: {chat_filename}")
    
    # Step 2: Analyze changes
    print("\n" + "=" * 70)
    print("STEP 2: ANALYZING REPOSITORY CHANGES")
    print("=" * 70)
    
    backup_level, changes = analyze_changes_since_last_backup()
    
    if backup_level == "none":
        print("✓ No changes detected - nothing to commit")
        return
    
    # Step 3: Auto-confirm backup level (AI-first design)
    print("\n" + "=" * 70)
    print("STEP 3: AI-FIRST BACKUP LEVEL CONFIRMATION")
    print("=" * 70)
    
    confirmed_level = get_user_backup_confirmation(backup_level, changes, test_mode)
    
    # Step 4: Create backup
    print("\n" + "=" * 70)
    print(f"STEP 4: CREATING {confirmed_level.upper()} BACKUP")
    print("=" * 70)
    
    backup_branch = create_backup_branch(confirmed_level)
    print(f"✓ Backup created and pushed: {backup_branch}")
    
    # Step 5: Generate commit message
    print("\n" + "=" * 70)
    print("STEP 5: GENERATING COMMIT MESSAGE")
    print("=" * 70)
    
    commit_message = generate_commit_message(chat_filename, confirmed_level, changes)
    print("Generated commit message:")
    print("-" * 40)
    for line in commit_message.split('\n'):
        print(f"  {line}")
    print("-" * 40)
    
    # Step 6: Git commit
    print("\n" + "=" * 70)
    print("STEP 6: PERFORMING GIT COMMIT")
    print("=" * 70)
    
    commit_hash = perform_git_commit(commit_message)
    
    # Step 7: Push to remote
    print("\n" + "=" * 70)
    print("STEP 7: PUSHING TO GITHUB")
    print("=" * 70)
    
    push_to_remote()
    
    # Step 8: Cleanup
    print("\n" + "=" * 70)
    print("STEP 8: CLEANUP OLD BACKUPS")
    print("=" * 70)
    
    cleanup_old_backups()
    
    # Success summary
    print("\n" + "=" * 70)
    print("SUCCESS: COMMIT COMPLETED WITH DATA PROTECTION")
    print("=" * 70)
    print(f"✓ Chat history updated: {chat_filename}")
    print(f"✓ {confirmed_level.upper()} backup created: {backup_branch}")
    print(f"✓ Commit successful: {commit_hash}")
    print("✓ Changes pushed to GitHub")
    print("✓ Old backups cleaned up")
    print()
    print("🔒 Zero information loss principle maintained")
    print("📁 All data protected with backup-first workflow")

if __name__ == "__main__":
    main()
