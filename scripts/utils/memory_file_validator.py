#!/usr/bin/env python3
"""
Memory File Validator - STREAMING VALIDATION FOR GAPLESS HISTORY
Validates memory files to ensure they form a continuous, gapless conversation history.
Follows Data Core System principles: zero information loss, data immutability, perfect preservation.
"""

import os
import re
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

def validate_memory_file_creation(file_path: str, content: str) -> Tuple[bool, str]:
    """Validate that a memory file was created successfully with proper content."""
    
    # Check if file exists
    if not os.path.exists(file_path):
        return False, f"Memory file was not created: {file_path}"
    
    # Check if file is readable
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            saved_content = f.read()
    except Exception as e:
        return False, f"Memory file is not readable: {e}"
    
    # Check if content matches what was intended
    if saved_content.strip() != content.strip():
        return False, f"Memory file content does not match intended content"
    
    # Check file size
    file_size = os.path.getsize(file_path)
    if file_size < 10:  # Minimum reasonable size
        return False, f"Memory file is too small: {file_size} bytes"
    
    return True, f"Memory file creation validation passed: {file_size} bytes"

# Utility module for memory file validation
# Import and use in other processes:
# from scripts.utils.memory_file_validator import validate_memory_file_format, validate_gapless_history
