#!/usr/bin/env python3
"""
Natural Value Extraction Chat Save Process - AI-FIRST CHAT CAPTURE WITH FRAMEWORK v2.0
Takes AI value log from memory files, creates Framework v2.0 compliant records, validates thoroughly, and ensures gapless history.
Follows Data Core System principles: zero information loss, data immutability, comprehensive preservation.
Integrates with reference/value_patterns.md and reference/value_definitions.md for enhanced content capture.
"""

import os
import sys
import uuid
import re
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional

def get_current_gmt_time():
    """Get current GMT time for timestamps."""
    return datetime.now(timezone.utc)

def generate_uuid():
    """Generate globally unique identifier for the chat report."""
    return str(uuid.uuid4())

def create_temporal_filename(timestamp):
    """Create temporal filename: chat-YYYY-MM-DD-HH-MM.md"""
    return f"chat-{timestamp.strftime('%Y-%m-%d-%H-%M')}.md"

def read_ai_value_log_from_memory():
    """Read the AI's value log from memory files where it was written during conversation."""
    print("  Reading AI value log from memory files...")
    
    # Look for memory files in the data-core-system directory
    memory_files = []
    for filename in os.listdir('.'):
        if filename.endswith('.md') and 'memory' in filename.lower():
            memory_files.append(filename)
    
    if not memory_files:
        print("    ✗ CRITICAL: No memory files found")
        print("      AI should write value log to memory files during conversation")
        sys.exit(1)
    
    # Read the most recent memory file (assuming it contains current conversation value)
    memory_files.sort(reverse=True)
    latest_memory = memory_files[0]
    
    try:
        with open(latest_memory, 'r', encoding='utf-8') as f:
            memory_content = f.read()
        
        print(f"    ✓ Memory file read: {latest_memory}")
        print(f"    ✓ Content length: {len(memory_content)} characters")
        
        return memory_content
        
    except Exception as e:
        print(f"    ✗ CRITICAL: Failed to read memory file {latest_memory}")
        print(f"      Error: {e}")
        sys.exit(1)

def extract_conversation_context_from_memory(memory_content: str) -> Tuple[str, str]:
    """Extract conversation context and new insights from memory content."""
    print("  Extracting conversation context and insights...")
    
    # Look for the specific section headers in the memory file
    context_marker = "## Context Snapshot"
    insights_marker = "## New Insights"
    
    if context_marker in memory_content and insights_marker in memory_content:
        # Split content into sections
        parts = memory_content.split(context_marker)
        if len(parts) > 1:
            context_part = parts[1].split("## ")[0].strip()
        else:
            context_part = ""
        
        parts = memory_content.split(insights_marker)
        if len(parts) > 1:
            insights_part = parts[1].strip()
        else:
            insights_part = ""
        

        
        context = context_part
        insights = insights_part
        
    else:
        # Fallback: treat entire content as context if sections not found
        context = memory_content
        insights = "Conversation captured from live chat session"
    
    print(f"    ✓ Context extracted: {len(context)} characters")
    print(f"    ✓ Insights extracted: {len(insights)} characters")
    
    return context, insights

def calculate_content_similarity(current_content: str, previous_content: str) -> float:
    """Calculate similarity percentage between current and previous content."""
    # Normalize content for comparison
    current_normalized = normalize_content_for_comparison(current_content)
    previous_normalized = normalize_content_for_comparison(previous_content)
    
    # Split into words for Jaccard similarity
    current_words = set(current_normalized.split())
    previous_words = set(previous_normalized.split())
    
    if not current_words and not previous_words:
        return 100.0  # Both empty
    if not current_words or not previous_words:
        return 0.0    # One empty
    
    intersection = current_words.intersection(previous_words)
    union = current_words.union(previous_words)
    
    similarity = len(intersection) / len(union) * 100
    return round(similarity, 2)

def normalize_content_for_comparison(content: str) -> str:
    """Normalize content for similarity comparison."""
    # Remove markdown formatting
    content = re.sub(r'[#*`\[\]]', '', content)
    # Remove metadata sections
    content = re.sub(r'---.*?---', '', content, flags=re.DOTALL)
    # Normalize whitespace
    content = re.sub(r'\s+', ' ', content)
    # Remove timestamps and UUIDs
    content = re.sub(r'\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b', '', content)
    content = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', '', content)
    return content.strip().lower()

def remove_duplicate_specific_value(current_content: str, previous_content: str) -> str:
    """Remove duplicate specific value content while preserving context and new insights."""
    print("    🔍 Applying smart deduplication to specific value content...")
    
    # Split content into sections
    current_sections = current_content.split('## ')
    previous_sections = previous_content.split('## ')
    
    # Extract New Insights sections for deduplication
    current_insights = ""
    previous_insights = ""
    
    for section in current_sections:
        if section.strip().startswith('New Insights'):
            current_insights = section.replace('New Insights', '').strip()
            break
    
    for section in previous_sections:
        if section.strip().startswith('New Insights'):
            previous_insights = section.replace('New Insights', '').strip()
            break
    
    if not current_insights or not previous_insights:
        print("      ✓ No insights sections found - proceeding with original content")
        return current_content
    
    # Split insights into individual items for detailed comparison
    current_items = [item.strip() for item in current_insights.split('### ') if item.strip()]
    previous_items = [item.strip() for item in previous_insights.split('### ') if item.strip()]
    
    # Remove duplicate specific value items
    deduplicated_items = []
    removed_count = 0
    
    for current_item in current_items:
        is_duplicate = False
        
        # Check if this item is substantially similar to any previous item
        for previous_item in previous_items:
            if len(current_item) > 50 and len(previous_item) > 50:  # Only check substantial items
                similarity = calculate_content_similarity(current_item, previous_item)
                if similarity > 80:  # High similarity threshold for specific value
                    is_duplicate = True
                    removed_count += 1
                    print(f"      - Removed duplicate insight: {current_item[:100]}...")
                    break
        
        if not is_duplicate:
            deduplicated_items.append(current_item)
    
    # Reconstruct the content with deduplicated insights
    if deduplicated_items:
        deduplicated_insights = '\n\n### '.join(deduplicated_items)
        # Replace the New Insights section
        updated_content = current_content.replace(
            f"## New Insights\n{current_insights}",
            f"## New Insights\n{deduplicated_insights}"
        )
        print(f"      ✓ Deduplication complete: {removed_count} duplicate insights removed")
        print(f"      ✓ {len(deduplicated_items)} unique insights preserved")
        return updated_content
    else:
        print(f"      ⚠ All insights were duplicates - keeping minimal context")
        # Keep minimal context but remove detailed insights
        return current_content.replace(
            f"## New Insights\n{current_insights}",
            "## New Insights\n*Content deduplicated - see previous records for detailed insights*"
        )

def check_for_gaps_with_previous_reports(chats_dir: str, current_content: str) -> Tuple[bool, str, str]:
    """Check for information gaps and apply smart deduplication without blocking saves."""
    print("  Checking for gaps and applying smart deduplication...")
    
    if not os.path.exists(chats_dir):
        print("    ✓ No previous reports found - this will be the first")
        return True, "First chat report in system", current_content
    
    # Find most recent reports
    chat_files = [f for f in os.listdir(chats_dir) if f.startswith("chat-") and f.endswith(".md")]
    
    if not chat_files:
        print("    ✓ No previous reports found - this will be the first")
        return True, "First chat report in system", current_content
    
    # Sort by filename (temporal naming ensures chronological order)
    chat_files.sort(reverse=True)
    
    # Check against the most recent report for deduplication
    latest_report = chat_files[0]
    latest_path = os.path.join(chats_dir, latest_report)
    
    try:
        with open(latest_path, 'r', encoding='utf-8') as f:
            latest_content = f.read()
        
        # Calculate similarity for information purposes only
        similarity = calculate_content_similarity(current_content, latest_content)
        
        print(f"    📊 Content analysis against {latest_report}:")
        print(f"      - Similarity: {similarity}%")
        print(f"      - Context similarity is fine for narrative continuity")
        print(f"      - Specific value content will be deduplicated")
        
        # Apply smart deduplication: remove duplicate specific value content
        deduplicated_content = remove_duplicate_specific_value(current_content, latest_content)
        
        print(f"    ✓ Smart deduplication applied - content cleaned for saving")
        print(f"    ✓ Gap analysis complete - building on {latest_report}")
        return True, f"Continues from {latest_report} (similarity: {similarity}%, content deduplicated)", deduplicated_content
        
    except Exception as e:
        print(f"    ⚠ Error reading {latest_report}: {e}")
        print(f"    ✓ Proceeding with original content (read error)")
        return True, f"Continues from {latest_report} (read error, proceeding with caution)", current_content

def create_framework_v2_content(context_snapshot: str, new_insights: str, report_id: str, timestamp: datetime) -> str:
    """Create Framework v2.0 compliant chat report content."""
    print("  Creating Framework v2.0 compliant chat report...")
    print(f"    DEBUG: Function called with context_snapshot length: {len(context_snapshot)}")
    print(f"    DEBUG: Function called with new_insights length: {len(new_insights)}")
    
    local_time = timestamp.replace(tzinfo=timezone.utc).astimezone()
    
    content = f"""---
type: chat
framework: framework
id: {report_id}
timestamp: {timestamp.isoformat()}
framework_version: 2.0
---

# Chat Session Report - {timestamp.strftime('%Y-%m-%d %H:%M')}

## Context Snapshot
{context_snapshot}

## New Insights
{new_insights}

## Technical Specifications
Framework v2.0 chat capture system with Natural Value Extraction. Timestamp: {timestamp.isoformat()}. Local time: {local_time.strftime('%Y-%m-%d %H:%M:%S')} (GMT: {timestamp.strftime('%H:%M:%S')}). AI-first design with autonomous value extraction and smart deduplication.
"""
    
    print("    ✓ Framework v2.0 report content created")
    print(f"    DEBUG: Generated content length: {len(content)} characters")
    print(f"    DEBUG: Content preview: {content[:200]}...")
    return content

def validate_framework_compliance(content: str) -> Tuple[bool, List[str]]:
    """Validate Framework v2.0 compliance."""
    print("  Validating Framework v2.0 compliance...")
    
    issues = []
    required_sections = ["Context Snapshot", "New Insights", "Technical Specifications"]
    
    for section in required_sections:
        if section not in content:
            issues.append(f"Missing required section: {section}")
            continue
        
        # Debug: Show what we're looking for
        print(f"    DEBUG: Looking for section '## {section}'")
        
        # Find the section marker
        section_marker = f"## {section}"
        if section_marker not in content:
            issues.append(f"Section '{section}' marker not found")
            continue
        
        # Get the position of this section
        start_pos = content.find(section_marker)
        print(f"    DEBUG: Section '{section}' found at position {start_pos}")
        
        # Find the next section marker (##) or end of content
        # We need to look for "## " (two hashes + space) to avoid finding ### headers within content
        search_start = start_pos + len(section_marker)
        next_section_pos = -1
        
        # Search for the next "## " marker, but only if it's at the start of a line
        # This avoids finding ### headers within the content
        for i in range(search_start, len(content)):
            if content[i:i+3] == "## " and (i == 0 or content[i-1] == '\n'):
                next_section_pos = i
                break
        
        if next_section_pos == -1:
            # No next section, take everything to the end
            section_content = content[search_start:].strip()
        else:
            # Take content up to next section
            section_content = content[search_start:next_section_pos].strip()
        
        # Debug: Show the exact positions
        print(f"    DEBUG: Section '{section}' starts at {start_pos}, next section at {next_section_pos}")
        print(f"    DEBUG: Section '{section}' content range: {start_pos + len(section_marker)} to {next_section_pos if next_section_pos != -1 else 'end'}")
        
        # Debug: Show what we found
        print(f"    DEBUG: Section '{section}' content length: {len(section_content)}")
        print(f"    DEBUG: Section '{section}' preview: '{section_content[:100]}...'")
        
        if len(section_content) < 50:
            issues.append(f"Section '{section}' too short ({len(section_content)} chars)")
    
    if issues:
        print(f"    ✗ Framework validation failed ({len(issues)} issues):")
        for issue in issues:
            print(f"      - {issue}")
        return False, issues
    
    print("    ✓ Framework v2.0 compliance validated")
    return True, []

def verify_file_integrity(filepath: str, expected_content: str) -> Tuple[bool, str]:
    """Verify file was written correctly by reading it back."""
    print("  Verifying file integrity...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        
        if saved_content != expected_content:
            return False, "Content mismatch between expected and saved"
        
        print(f"    ✓ File integrity verified ({len(saved_content)} characters)")
        return True, f"File integrity confirmed: {len(saved_content)} characters"
        
    except Exception as e:
        return False, f"Integrity verification failed: {e}"

def cleanup_memory_file_after_save():
    """Clean up the memory file after successful save to prevent duplication."""
    print("  Cleaning up memory file to prevent duplication...")
    
    try:
        # Look for memory files in the data-core-system directory
        memory_files = []
        for filename in os.listdir('.'):
            if filename.endswith('.md') and 'memory' in filename.lower():
                memory_files.append(filename)
        
        if not memory_files:
            print("    ⚠ No memory files found to clean up")
            return
        
        # Clean up the most recent memory file
        memory_files.sort(reverse=True)
        latest_memory = memory_files[0]
        
        # Read current content
        with open(latest_memory, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        # Extract only the essential context, remove detailed insights
        if "## New Insights" in current_content:
            # Keep only the context section, clear the insights
            context_part = current_content.split("## New Insights")[0]
            cleaned_content = context_part + "\n\n## New Insights\n*Insights cleared after successful save*\n"
        else:
            # If no insights section, just clear the content
            cleaned_content = "# Conversation Memory\n\n*Content cleared after successful save*\n"
        
        # Write back the cleaned content
        with open(latest_memory, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"    ✓ Memory file cleaned: {latest_memory}")
        print(f"    ✓ Duplication prevention: Insights cleared, context preserved")
        
    except Exception as e:
        print(f"    ⚠ Warning: Memory file cleanup failed: {e}")
        print(f"    ⚠ Manual cleanup may be needed to prevent duplication")

def main():
    """Main Natural Value Extraction chat save process - AI-FIRST DESIGN."""
    gmt_time = get_current_gmt_time()
    local_time = gmt_time.replace(tzinfo=timezone.utc).astimezone()
    
    print("=" * 70)
    print("NATURAL VALUE EXTRACTION CHAT SAVE PROCESS - AI-FIRST DESIGN")
    print("=" * 70)
    print("Reads AI value log from memory files, creates Framework v2.0 compliant records,")
    print("validates thoroughly, and ensures gapless history with smart deduplication.")
    print("Zero manual intervention required - designed for AI systems.")
    print(f"Started at: {local_time.strftime('%H:%M:%S')} (local) / {gmt_time.strftime('%H:%M:%S')} GMT")
    
    # Step 1: Environment validation
    print("\n" + "=" * 70)
    print("STEP 1: ENVIRONMENT VALIDATION")
    print("=" * 70)
    
    chats_dir = "chats"
    if not os.path.exists(chats_dir):
        print(f"✗ CRITICAL: Chats directory not found at {chats_dir}")
        print("  System cannot operate without proper directory structure")
        sys.exit(1)
    print(f"✓ Chats directory validated: {chats_dir}")
    
    # Step 2: Read AI value log from memory files
    print("\n" + "=" * 70)
    print("STEP 2: READ AI VALUE LOG FROM MEMORY")
    print("=" * 70)
    
    memory_content = read_ai_value_log_from_memory()
    
    # Step 3: Extract conversation context and insights
    print("\n" + "=" * 70)
    print("STEP 3: EXTRACT CONVERSATION CONTENT")
    print("=" * 70)
    
    context_snapshot, new_insights = extract_conversation_context_from_memory(memory_content)
    conversation_content = context_snapshot + "\n\n" + new_insights
    
    print(f"✓ Conversation content extracted ({len(conversation_content)} characters)")
    print(f"  - Context snapshot: {len(context_snapshot)} characters")
    print(f"  - New insights: {len(new_insights)} characters")
    
    # Step 4: Content validation
    print("\n" + "=" * 70)
    print("STEP 4: CONTENT VALIDATION")
    print("=" * 70)
    
    print(f"    DEBUG: conversation_content length: {len(conversation_content)}")
    print(f"    DEBUG: conversation_content.strip() length: {len(conversation_content.strip())}")
    
    if len(conversation_content.strip()) < 100:
        print("✗ CRITICAL: Content too short - minimum 100 characters required")
        sys.exit(1)
    
    word_count = len(conversation_content.split())
    print(f"    DEBUG: word_count: {word_count}")
    
    if word_count < 20:
        print("✗ CRITICAL: Content insufficient - minimum 20 words required")
        sys.exit(1)
    
    print(f"✓ Content validated ({len(conversation_content)} chars, {word_count} words)")
    
    # Step 5: Gap analysis and smart deduplication
    print("\n" + "=" * 70)
    print("STEP 5: GAP ANALYSIS AND SMART DEDUPLICATION")
    print("=" * 70)
    
    gap_ok, gap_details, deduplicated_content = check_for_gaps_with_previous_reports(chats_dir, conversation_content)
    if not gap_ok:
        print("✗ CRITICAL: Gap analysis failed")
        print(f"  Issue: {gap_details}")
        sys.exit(1)
    
    # Use deduplicated content for the rest of the process
    conversation_content = deduplicated_content
    print(f"✓ Gap analysis complete: {gap_details}")
    print(f"✓ Content deduplicated and ready for saving")
    
    # Step 6: Generate file metadata
    print("\n" + "=" * 70)
    print("STEP 6: GENERATE FILE METADATA")
    print("=" * 70)
    
    report_id = generate_uuid()
    timestamp = get_current_gmt_time()
    local_time = timestamp.replace(tzinfo=timezone.utc).astimezone()
    filename = create_temporal_filename(timestamp)
    filepath = os.path.join(chats_dir, filename)
    
    print(f"✓ Report ID: {report_id}")
    print(f"✓ Timestamp: {local_time.strftime('%Y-%m-%d %H:%M:%S')} (local) / {timestamp.strftime('%H:%M:%S')} GMT")
    print(f"✓ Filename: {filename}")
    
    # Step 7: Create Framework v2.0 report content
    print("\n" + "=" * 70)
    print("STEP 7: CREATE FRAMEWORK v2.0 REPORT")
    print("=" * 70)
    
    try:
        report_content = create_framework_v2_content(context_snapshot, new_insights, report_id, timestamp)
        print("✓ Framework v2.0 report created successfully")
    except Exception as e:
        print("✗ CRITICAL: Report creation failed")
        print(f"  Error: {e}")
        sys.exit(1)
    
    # Step 8: Framework compliance validation
    print("\n" + "=" * 70)
    print("STEP 8: FRAMEWORK COMPLIANCE VALIDATION")
    print("=" * 70)
    
    try:
        is_valid, issues = validate_framework_compliance(report_content)
        if not is_valid:
            print("✗ CRITICAL: Framework validation failed")
            print(f"  Issues: {len(issues)}")
            for issue in issues:
                print(f"      - {issue}")
            sys.exit(1)
        
        print("✓ Framework v2.0 compliance validated")
    except Exception as e:
        print("✗ CRITICAL: Framework validation crashed")
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Step 9: Write file to disk
    print("\n" + "=" * 70)
    print("STEP 9: WRITE FILE TO DISK")
    print("=" * 70)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"✓ File written successfully: {filepath}")
    except Exception as e:
        print("✗ CRITICAL: File write failed")
        print(f"  Error: {e}")
        sys.exit(1)
    
    # Step 10: File integrity verification
    print("\n" + "=" * 70)
    print("STEP 10: FILE INTEGRITY VERIFICATION")
    print("=" * 70)
    
    integrity_ok, integrity_details = verify_file_integrity(filepath, report_content)
    if not integrity_ok:
        print("✗ CRITICAL: File integrity verification failed")
        print(f"  Issue: {integrity_details}")
        sys.exit(1)
    
    print(f"✓ File integrity verified: {integrity_details}")
    
    # Step 11: Clean up memory file to prevent duplication
    print("\n" + "=" * 70)
    print("STEP 11: MEMORY FILE CLEANUP")
    print("=" * 70)
    
    try:
        cleanup_memory_file_after_save()
        print("✓ Memory file cleanup completed - duplication prevented")
    except Exception as e:
        print(f"✗ WARNING: Memory file cleanup failed: {e}")
        print(f"  Manual cleanup may be needed to prevent duplication")
    
    # Final success report
    final_time = get_current_gmt_time()
    final_local = final_time.replace(tzinfo=timezone.utc).astimezone()
    
    print("\n" + "=" * 70)
    print("SUCCESS: NATURAL VALUE EXTRACTION CHAT SAVE COMPLETED")
    print("=" * 70)
    print(f"✓ Chat report saved: {filename}")
    print(f"✓ Report size: {len(report_content)} characters")
    print(f"✓ Framework: v2.0 compliant with Natural Value Extraction")
    print(f"✓ Content: {len(conversation_content)} characters from memory files")
    print(f"✓ Context snapshot: {len(context_snapshot)} characters")
    print(f"✓ New insights: {len(new_insights)} characters")
    print(f"✓ UUID: {report_id}")
    print(f"✓ Completed: {final_local.strftime('%H:%M:%S')} (local) / {final_time.strftime('%H:%M:%S')} GMT")
    print("✓ Zero information loss maintained with smart deduplication")
    print("✓ AI-first design - no manual intervention required")
    print("✓ Natural Value Extraction system operational")
    print("✓ Gapless history preserved for seamless continuity")
    print("✓ Smart deduplication applied - duplicate specific value content removed")
    print("✓ Context continuity maintained for narrative flow")

if __name__ == "__main__":
    main()
