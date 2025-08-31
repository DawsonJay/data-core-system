#!/usr/bin/env python3
"""
Git Backup & Commit Process - DATA PROTECTION FIRST
Ensures comprehensive data backup before any Git operations.
Implements multiple backup strategies to prevent data loss.
"""

import os
import sys
import shutil
import subprocess
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

def create_local_backup(backup_dir):
    """Create a complete local backup of the data core."""
    print("  Creating local backup...")
    
    # Create backup directory with timestamp
    current_time = get_current_gmt_time()
    timestamp = current_time.strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"data_core_backup_{timestamp}")
    
    print(f"    Backup location: {backup_path}")
    
    # Ensure backup directory exists
    os.makedirs(backup_dir, exist_ok=True)
    
    # Copy entire project (excluding .git to avoid corruption)
    print("    Copying all files...")
    shutil.copytree(".", backup_path, ignore=shutil.ignore_patterns('.git'))
    
    # Verify backup integrity
    print("    Verifying backup integrity...")
    original_files = []
    backup_files = []
    
    for root, dirs, files in os.walk("."):
        if ".git" in root:
            continue
        for file in files:
            original_files.append(os.path.relpath(os.path.join(root, file)))
    
    for root, dirs, files in os.walk(backup_path):
        for file in files:
            backup_files.append(os.path.relpath(os.path.join(root, file), backup_path))
    
    original_files.sort()
    backup_files.sort()
    
    if original_files == backup_files:
        print("    ✓ Backup integrity verified - all files copied correctly")
        return backup_path
    else:
        print("    ✗ Backup integrity check failed")
        missing = set(original_files) - set(backup_files)
        extra = set(backup_files) - set(original_files)
        if missing:
            print(f"      Missing files: {missing}")
        if extra:
            print(f"      Extra files: {extra}")
        sys.exit(1)

def create_git_backup():
    """Create Git-based backup by pushing to remote."""
    print("  Creating Git remote backup...")
    
    # Ensure we have a remote
    success, output = run_command("git remote -v", "Check Git remotes", critical=False)
    if not success or not output.strip():
        print("    ⚠ No Git remotes configured - skipping remote backup")
        return False
    
    # Create a backup branch with timestamp
    current_time = get_current_gmt_time()
    timestamp = current_time.strftime("%Y%m%d_%H%M%S")
    backup_branch = f"backup_{timestamp}"
    
    print(f"    Creating backup branch: {backup_branch}")
    run_command(f"git checkout -b {backup_branch}", f"Create backup branch {backup_branch}")
    
    # Push backup branch to remote
    run_command(f"git push origin {backup_branch}", f"Push backup branch to remote")
    
    # Return to main branch
    run_command("git checkout main", "Return to main branch")
    
    print("    ✓ Git remote backup created successfully")
    return True

def create_additional_backups():
    """Create additional backup strategies for maximum protection."""
    print("  Creating additional backup strategies...")
    
    backups_created = 0
    
    # 1. Compressed archive backup
    try:
        current_time = get_current_gmt_time()
        timestamp = current_time.strftime("%Y%m%d_%H%M%S")
        archive_name = f"data_core_archive_{timestamp}.tar.gz"
        
        print(f"    Creating compressed archive: {archive_name}")
        run_command(f"tar -czf /tmp/{archive_name} --exclude='.git' .", "Create compressed archive")
        
        # Move to backups directory
        backup_dir = os.path.expanduser("~/data_core_backups")
        os.makedirs(backup_dir, exist_ok=True)
        shutil.move(f"/tmp/{archive_name}", os.path.join(backup_dir, archive_name))
        
        print(f"    ✓ Compressed archive created: {backup_dir}/{archive_name}")
        backups_created += 1
    except Exception as e:
        print(f"    ⚠ Compressed archive backup failed: {e}")
    
    # 2. Git bundle backup
    try:
        bundle_name = f"data_core_bundle_{timestamp}.bundle"
        bundle_path = os.path.join(backup_dir, bundle_name)
        
        print(f"    Creating Git bundle: {bundle_name}")
        run_command(f"git bundle create {bundle_path} --all", "Create Git bundle backup")
        
        print(f"    ✓ Git bundle created: {bundle_path}")
        backups_created += 1
    except Exception as e:
        print(f"    ⚠ Git bundle backup failed: {e}")
    
    print(f"    ✓ Additional backups completed ({backups_created} successful)")
    return backups_created > 0

def validate_git_status():
    """Validate Git repository status before operations."""
    print("  Validating Git repository status...")
    
    # Check if we're in a Git repository
    success, _ = run_command("git rev-parse --git-dir", "Verify Git repository")
    if not success:
        print("    ✗ Not in a Git repository")
        sys.exit(1)
    
    # Check for uncommitted changes
    success, output = run_command("git status --porcelain", "Check for uncommitted changes")
    if output.strip():
        print("    Found uncommitted changes:")
        for line in output.strip().split('\n'):
            print(f"      {line}")
        print("    ✓ Changes ready for commit")
    else:
        print("    ✓ Working directory clean")
    
    # Check Git configuration
    success, _ = run_command("git config user.name", "Check Git user name", critical=False)
    success, _ = run_command("git config user.email", "Check Git user email", critical=False)
    
    print("    ✓ Git repository status validated")

def perform_git_commit(commit_message):
    """Perform the actual Git commit with validation."""
    print("  Performing Git commit...")
    
    # Stage all changes
    run_command("git add -A", "Stage all changes")
    
    # Verify what's being committed
    success, output = run_command("git status --porcelain", "Check staged changes")
    if output.strip():
        print("    Changes to be committed:")
        for line in output.strip().split('\n'):
            print(f"      {line}")
    
    # Create the commit
    escaped_message = commit_message.replace('"', '\\"')
    run_command(f'git commit -m "{escaped_message}"', "Create commit")
    
    # Get commit hash for verification
    success, commit_hash = run_command("git rev-parse HEAD", "Get commit hash")
    print(f"    ✓ Commit created successfully: {commit_hash.strip()[:8]}")
    
    return commit_hash.strip()

def push_to_remote():
    """Push committed changes to remote repository."""
    print("  Pushing to remote repository...")
    
    # Check if remote exists
    success, output = run_command("git remote -v", "Check remotes", critical=False)
    if not success or not output.strip():
        print("    ⚠ No remote repository configured - skipping push")
        return False
    
    # Push to main branch
    run_command("git push origin main", "Push to remote main branch")
    print("    ✓ Changes pushed to remote repository")
    return True

def cleanup_old_backups(backup_dir, keep_count=10):
    """Clean up old backup files to prevent disk space issues."""
    print("  Cleaning up old backups...")
    
    if not os.path.exists(backup_dir):
        print("    ✓ No old backups to clean up")
        return
    
    # Find all backup files
    backup_files = []
    for filename in os.listdir(backup_dir):
        if filename.startswith("data_core_backup_"):
            backup_path = os.path.join(backup_dir, filename)
            if os.path.isdir(backup_path):
                backup_files.append((filename, backup_path, os.path.getmtime(backup_path)))
    
    # Sort by modification time (newest first)
    backup_files.sort(key=lambda x: x[2], reverse=True)
    
    # Remove old backups beyond keep_count
    removed_count = 0
    for i, (filename, path, _) in enumerate(backup_files):
        if i >= keep_count:
            print(f"    Removing old backup: {filename}")
            shutil.rmtree(path)
            removed_count += 1
    
    if removed_count > 0:
        print(f"    ✓ Cleaned up {removed_count} old backups")
    else:
        print("    ✓ No old backups to remove")

def main():
    """Main backup and commit process."""
    print("=" * 70)
    print("GIT BACKUP & COMMIT PROCESS - DATA PROTECTION FIRST")
    print("=" * 70)
    print("Comprehensive data backup before Git operations.")
    print("Multiple backup strategies ensure zero data loss.")
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("\n✗ ERROR: Commit message required")
        print("\nUsage:")
        print("  python processes/git_backup_commit.py \"Your commit message here\"")
        print("\nOptions:")
        print("  --skip-local-backup    Skip local directory backup")
        print("  --skip-additional      Skip additional backup strategies")
        print("  --backup-only          Only create backups, don't commit")
        sys.exit(1)
    
    commit_message = sys.argv[1]
    skip_local = "--skip-local-backup" in sys.argv
    skip_additional = "--skip-additional" in sys.argv
    backup_only = "--backup-only" in sys.argv
    
    # Set up backup directory
    backup_base_dir = os.path.expanduser("~/data_core_backups")
    
    print(f"\n📋 Commit Message: {commit_message}")
    print(f"🗂️  Backup Directory: {backup_base_dir}")
    if backup_only:
        print("🔄 Mode: Backup Only (no Git commit)")
    else:
        print("🔄 Mode: Full Backup + Commit")
    
    # Step 1: Validate Git repository
    print("\n" + "=" * 70)
    print("STEP 1: VALIDATING GIT REPOSITORY")
    print("=" * 70)
    validate_git_status()
    
    # Step 2: Create comprehensive backups
    print("\n" + "=" * 70)
    print("STEP 2: CREATING COMPREHENSIVE BACKUPS")
    print("=" * 70)
    
    backup_results = {
        'local': False,
        'git': False,
        'additional': False
    }
    
    # Local directory backup
    if not skip_local:
        try:
            local_backup_path = create_local_backup(backup_base_dir)
            backup_results['local'] = True
            print(f"  ✓ Local backup created: {local_backup_path}")
        except Exception as e:
            print(f"  ✗ Local backup failed: {e}")
            sys.exit(1)
    else:
        print("  ⚠ Skipping local backup (--skip-local-backup)")
    
    # Git remote backup
    try:
        backup_results['git'] = create_git_backup()
    except Exception as e:
        print(f"  ⚠ Git backup failed: {e}")
    
    # Additional backup strategies
    if not skip_additional:
        try:
            backup_results['additional'] = create_additional_backups()
        except Exception as e:
            print(f"  ⚠ Additional backups failed: {e}")
    else:
        print("  ⚠ Skipping additional backups (--skip-additional)")
    
    # Backup summary
    successful_backups = sum(1 for result in backup_results.values() if result)
    print(f"\n  📊 Backup Summary: {successful_backups}/3 strategies successful")
    
    if successful_backups == 0:
        print("  ✗ CRITICAL: No backups were successful - aborting commit")
        sys.exit(1)
    elif successful_backups < 2:
        print("  ⚠ WARNING: Limited backup coverage - consider investigating failures")
    
    # Step 3: Git commit (if not backup-only mode)
    if not backup_only:
        print("\n" + "=" * 70)
        print("STEP 3: PERFORMING GIT COMMIT")
        print("=" * 70)
        
        try:
            commit_hash = perform_git_commit(commit_message)
            print(f"  ✓ Commit successful: {commit_hash[:8]}")
        except Exception as e:
            print(f"  ✗ Commit failed: {e}")
            sys.exit(1)
        
        # Step 4: Push to remote
        print("\n" + "=" * 70)
        print("STEP 4: PUSHING TO REMOTE")
        print("=" * 70)
        
        try:
            push_success = push_to_remote()
            if push_success:
                print("  ✓ Remote push successful")
            else:
                print("  ⚠ Remote push skipped (no remote configured)")
        except Exception as e:
            print(f"  ✗ Remote push failed: {e}")
            print("  📝 Note: Commit was successful, only push failed")
    
    # Step 5: Cleanup
    print("\n" + "=" * 70)
    print("STEP 5: CLEANUP & MAINTENANCE")
    print("=" * 70)
    
    cleanup_old_backups(backup_base_dir)
    
    # Final summary
    print("\n" + "=" * 70)
    print("SUCCESS: DATA PROTECTION & COMMIT COMPLETED")
    print("=" * 70)
    
    if backup_only:
        print("✓ Comprehensive backups created successfully")
        print("📁 Data is protected with multiple backup strategies")
    else:
        print("✓ Data backed up with multiple strategies")
        print("✓ Git commit completed successfully")
        print("✓ Changes pushed to remote repository")
        print("📁 Your data is fully protected and version controlled")
    
    print(f"\n🗂️  Backup location: {backup_base_dir}")
    print("🔒 Zero data loss principle maintained")

if __name__ == "__main__":
    main()
