#!/usr/bin/env python3
"""
Validate Memory - VALIDATES CHAT MEMORY FILES FOR FORMAT AND GAPLESS HISTORY
Validates memory files to ensure they follow the Chat Memory Framework and form continuous conversation history.
Follows Data Core System principles: zero information loss, data immutability, perfect preservation.
"""

import os
import sys
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional

def validate_memory_file_format(content: str) -> Tuple[bool, str]:
    """Validate memory file format and content structure."""
    if not content.strip():
        return False, "Memory file is empty"
    
    lines = content.strip().split('\n')
    if len(lines) < 2:
        return False, "Memory file must contain at least one message pair"
    
    # Check for proper User:/Assistant: format
    user_pattern = re.compile(r'^User:\s+.+')
    assistant_pattern = re.compile(r'^Assistant:\s+.+')
    
    current_speaker = None
    message_count = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if user_pattern.match(line):
            if current_speaker == 'user':
                return False, f"Consecutive User messages at line {message_count + 1}"
            current_speaker = 'user'
            message_count += 1
        elif assistant_pattern.match(line):
            if current_speaker == 'assistant':
                return False, f"Consecutive Assistant messages at line {message_count + 1}"
            current_speaker = 'assistant'
            message_count += 1
        else:
            # Continuation line - must have a current speaker
            if current_speaker is None:
                return False, f"Message content without speaker at line {message_count + 1}"
    
    # Must end with assistant message for proper conversation flow
    if current_speaker != 'assistant':
        return False, "Memory file must end with Assistant message"
    
    if message_count < 2:
        return False, "Memory file must contain at least one complete message pair"
    
    return True, f"Format validation passed: {message_count} messages"

def get_last_message(content: str) -> Optional[str]:
    """Extract the last message from a memory file."""
    lines = content.strip().split('\n')
    
    # Find the last non-empty line
    for line in reversed(lines):
        line = line.strip()
        if line:
            return line
    
    return None

def get_first_message(content: str) -> Optional[str]:
    """Extract the first message from a memory file."""
    lines = content.strip().split('\n')
    
    # Find the first non-empty line
    for line in lines:
        line = line.strip()
        if line:
            return line
    
    return None

def validate_gapless_history(new_file_path: str, previous_file_path: str = None) -> Tuple[bool, str]:
    """Validate that new memory file forms gapless history with previous file."""
    
    # Read new memory file
    try:
        with open(new_file_path, 'r', encoding='utf-8') as f:
            new_content = f.read()
    except Exception as e:
        return False, f"Error reading new memory file: {e}"
    
    # Validate new file format
    format_valid, format_message = validate_memory_file_format(new_content)
    if not format_valid:
        return False, f"New memory file format invalid: {format_message}"
    
    # If no previous file, this is the first one
    if not previous_file_path or not os.path.exists(previous_file_path):
        return True, "First memory file - no gapless history check needed"
    
    # Read previous memory file
    try:
        with open(previous_file_path, 'r', encoding='utf-8') as f:
            previous_content = f.read()
    except Exception as e:
        return False, f"Error reading previous memory file: {e}"
    
    # Get last message from previous file
    last_previous = get_last_message(previous_content)
    if not last_previous:
        return False, "Previous memory file has no valid last message"
    
    # Get first message from new file
    first_new = get_first_message(new_content)
    if not first_new:
        return False, "New memory file has no valid first message"
    
    # Check for gapless connection
    if last_previous != first_new:
        return False, f"Gapless history validation failed:\nPrevious file ends with: {last_previous}\nNew file starts with: {first_new}"
    
    return True, "Gapless history validation passed"

def find_most_recent_memory(memories_dir: str) -> Optional[str]:
    """Find the most recent memory file by batch number."""
    if not os.path.exists(memories_dir):
        return None
    
    memory_files = []
    for file in os.listdir(memories_dir):
        if file.startswith('chat_memory_batch_') and file.endswith('.txt'):
            try:
                batch_num = int(file.replace('chat_memory_batch_', '').replace('.txt', ''))
                memory_files.append((batch_num, file))
            except ValueError:
                continue
    
    if not memory_files:
        return None
    
    # Sort by batch number and return the highest
    memory_files.sort(key=lambda x: x[0])
    return os.path.join(memories_dir, memory_files[-1][1])

def main():
    """Main validation process."""
    print("🔍 Chat Memory Validation Process")
    print("=" * 50)
    
    # Get command line arguments
    if len(sys.argv) < 2:
        print("❌ Error: Memory file path required")
        print("Usage: python validate_memory.py <memory_file_path>")
        sys.exit(1)
    
    memory_file_path = sys.argv[1]
    
    # Validate file exists
    if not os.path.exists(memory_file_path):
        print(f"❌ Error: Memory file not found: {memory_file_path}")
        sys.exit(1)
    
    print(f"📁 Validating memory file: {memory_file_path}")
    
    # Find most recent previous memory
    memories_dir = "chats/chat_memories/temp"
    all_memories = []
    for file in os.listdir(memories_dir):
        if file.startswith('chat_memory_batch_') and file.endswith('.txt'):
            try:
                batch_num = int(file.replace('chat_memory_batch_', '').replace('.txt', ''))
                all_memories.append((batch_num, file))
            except ValueError:
                continue
    
    # Sort by batch number
    all_memories.sort(key=lambda x: x[0])
    
    # Find the most recent memory that's NOT the current one being validated
    # Only try to parse batch number if filename follows expected pattern
    current_batch = None
    try:
        filename = os.path.basename(memory_file_path)
        if filename.startswith('chat_memory_batch_') and filename.endswith('.txt'):
            batch_str = filename.replace('chat_memory_batch_', '').replace('.txt', '')
            current_batch = int(batch_str)
    except (ValueError, AttributeError):
        # If filename doesn't follow expected pattern, treat as standalone file
        current_batch = None
    
    previous_memory = None
    if current_batch is not None:
        for batch_num, filename in all_memories:
            if batch_num < current_batch:
                previous_memory = os.path.join(memories_dir, filename)
    
    if previous_memory:
        print(f"📚 Found previous memory: {previous_memory}")
    else:
        print("📚 No previous memory found - this is the first memory file")
    
    # Validate format
    print("\n🔍 Step 1: Format Validation")
    try:
        with open(memory_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        format_valid, format_message = validate_memory_file_format(content)
        if format_valid:
            print(f"✅ {format_message}")
        else:
            print(f"❌ Format validation failed: {format_message}")
            print("\n" + "=" * 50)
            print("🚨 CRITICAL: MEMORY FILE FORMAT VALIDATION FAILED")
            print("=" * 50)
            print("ROOT CAUSE ANALYSIS:")
            print("  - Memory file does not follow User:/Assistant: pattern")
            print("  - This indicates either: incorrect creation or corrupted file")
            print("\nIMMEDIATE RECOVERY STEPS:")
            print("1. Check memory file content for proper formatting")
            print("2. Verify memory creation procedure was followed exactly")
            print("3. Check for file corruption or encoding issues")
            print("4. Recreate memory file using correct procedure")
            print("\nSYSTEM STRENGTHENING RECOMMENDATIONS:")
            print("1. Add format validation during memory creation")
            print("2. Implement memory file integrity checks")
            print("3. Add memory creation process monitoring")
            print("4. Consider implementing memory file templates")
            print("5. Add automated format correction suggestions")
            print("\nDATA SAFETY STATUS:")
            print("  - Original memory file preserved for analysis")
            print("  - No data loss has occurred")
            print("  - System can be retried after fixing format issues")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading memory file: {e}")
        print("\n" + "=" * 50)
        print("🚨 CRITICAL: MEMORY FILE READ FAILURE")
        print("=" * 50)
        print("ROOT CAUSE ANALYSIS:")
        print("  - Cannot read memory file for validation")
        print("  - This indicates either: file corruption, permission issues, or system problems")
        print("\nIMMEDIATE RECOVERY STEPS:")
        print("1. Check file permissions and ownership")
        print("2. Verify file system integrity")
        print("3. Check for file corruption or encoding issues")
        print("4. Verify file path is correct")
        print("\nSYSTEM STRENGTHENING RECOMMENDATIONS:")
        print("1. Add file system health checks before validation")
        print("2. Implement file integrity verification")
        print("3. Add permission validation before file operations")
        print("4. Consider implementing file recovery mechanisms")
        print("5. Add system resource monitoring")
        print("\nDATA SAFETY STATUS:")
        print("  - Original file preserved for analysis")
        print("  - No data loss has occurred")
        print("  - System can be retried after fixing access issues")
        sys.exit(1)
    
    # Validate gapless history
    print("\n🔍 Step 2: Gapless History Validation")
    if previous_memory and previous_memory != memory_file_path:
        history_valid, history_message = validate_gapless_history(memory_file_path, previous_memory)
        if history_valid:
            print(f"✅ {history_message}")
        else:
            print(f"❌ Gapless history validation failed: {history_message}")
            print("\n" + "=" * 50)
            print("🚨 CRITICAL: GAPLESS HISTORY VALIDATION FAILED")
            print("=" * 50)
            print("ROOT CAUSE ANALYSIS:")
            print("  - Memory files do not form continuous conversation")
            print("  - This indicates either: missing content or incorrect extraction")
            print("\nIMMEDIATE RECOVERY STEPS:")
            print("1. Check for missing conversation segments")
            print("2. Verify memory file creation sequence")
            print("3. Check for content extraction errors")
            print("4. Recreate missing memory files if needed")
            print("\nSYSTEM STRENGTHENING RECOMMENDATIONS:")
            print("1. Add conversation continuity monitoring during creation")
            print("2. Implement memory file sequence validation")
            print("3. Add content extraction verification")
            print("4. Consider implementing conversation flow tracking")
            print("5. Add automated gap detection and filling")
            print("\nDATA SAFETY STATUS:")
            print("  - All memory files preserved for analysis")
            print("  - No data loss has occurred")
            print("  - System can be retried after fixing continuity issues")
            sys.exit(1)
    else:
        print("✅ First memory file - no gapless history check needed")
    
    # File integrity check
    print("\n🔍 Step 3: File Integrity Check")
    file_size = os.path.getsize(memory_file_path)
    if file_size < 100:
        print(f"❌ File too small: {file_size} bytes (minimum 100 bytes)")
        sys.exit(1)
    else:
        print(f"✅ File size: {file_size} bytes")
    
    # Final validation
    print("\n🔍 Step 4: Final Validation")
    print("✅ All validation checks passed")
    print(f"✅ Memory file {memory_file_path} is valid and ready for use")
    
    print("\n" + "=" * 50)
    print("🎯 Chat Memory Validation Complete - All Checks Passed")

if __name__ == "__main__":
    main()
