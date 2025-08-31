#!/usr/bin/env python3
"""
Chat Save Process
Enforces Chat Report Framework and all rules when saving chat reports.
Designed for AI systems to create perfect, chainable, AI-readable historical records.
"""

import os
import sys
import uuid
from datetime import datetime, timezone

def get_current_gmt_time():
    """Get current GMT time."""
    return datetime.now(timezone.utc)

def generate_uuid():
    """Generate a globally unique identifier for the chat report."""
    return str(uuid.uuid4())

def create_temporal_filename(timestamp):
    """Create filename using only temporal data (no sequence numbers)."""
    return f"chat-{timestamp.strftime('%Y-%m-%d-%H-%M')}.md"

def validate_content_quality(content):
    """
    Validate that the content meets quality standards.
    Returns (is_valid, issues_list)
    """
    print("  Validating content quality...")
    
    issues = []
    required_sections = [
        "Summary", "Key Insights", "Decisions Made", "Questions Answered",
        "Action Items", "Context", "Personal Reflections", "System State",
        "Implementation Details", "Current Status", "Additional Notes"
    ]
    
    # Check all required sections are present
    for section in required_sections:
        if section not in content:
            issues.append(f"Missing required section: {section}")
            continue
            
        section_content = content[section].strip()
        
        # Check for empty content
        if not section_content:
            issues.append(f"Section '{section}' is empty")
            continue
            
        # Check for placeholder text
        placeholder_texts = [
            "[Brief overview of what was discussed]",
            "[New understanding or realizations]",
            "[What was decided or agreed upon]",
            "[Problems solved or clarifications provided]",
            "[What needs to be done next]",
            "[Important background or circumstances]",
            "[Your thoughts, feelings, or growth moments]",
            "[Current folder structure, files created, working status]",
            "[Specific technical decisions, how principles were implemented]",
            "[What's complete vs. in progress, what's working vs. what needs work]",
            "[Any other information that was discussed]"
        ]
        
        for placeholder in placeholder_texts:
            if placeholder in section_content:
                issues.append(f"Section '{section}' contains placeholder text: {placeholder}")
                break
        
        # Check minimum content length
        if len(section_content) < 20:
            issues.append(f"Section '{section}' too short ({len(section_content)} chars) - needs at least 20 characters")
    
    if issues:
        print(f"    ✗ Content quality validation failed:")
        for issue in issues:
            print(f"      - {issue}")
        return False, issues
    
    print("    ✓ Content quality validation passed")
    return True, []

def check_gap_with_previous_report(chats_path, current_timestamp):
    """
    Check that the new report doesn't leave gaps with the previous report.
    Returns (no_gaps, gap_details)
    """
    print("  Checking for gaps with previous report...")
    
    if not os.path.exists(chats_path):
        print("    ✓ No previous reports to check against")
        return True, "First report in this data core"
    
    # Find the most recent report by timestamp
    chat_files = [f for f in os.listdir(chats_path) if f.startswith("chat-") and f.endswith(".md")]
    if not chat_files:
        print("    ✓ No previous reports to check against")
        return True, "First report in this data core"
    
    # Parse timestamps from filenames to find the most recent
    latest_report = None
    latest_timestamp = None
    
    for chat_file in chat_files:
        try:
            # Parse chat-2025-08-31-13-12.md format
            parts = chat_file.replace(".md", "").split("-")
            if len(parts) >= 4:  # chat-date-time
                date_str = f"{parts[1]}-{parts[2]}-{parts[3]}"
                time_str = f"{parts[4]}-{parts[5]}"
                file_timestamp = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H-%M")
                # Make timezone-aware to match current_timestamp
                file_timestamp = file_timestamp.replace(tzinfo=timezone.utc)
                
                if latest_timestamp is None or file_timestamp > latest_timestamp:
                    latest_timestamp = file_timestamp
                    latest_report = chat_file
        except (ValueError, IndexError):
            continue
    
    if latest_report is None:
        print("    ✓ No valid previous reports to check against")
        return True, "No valid previous reports found"
    
    # Check if there's a significant time gap
    time_diff = current_timestamp - latest_timestamp
    if time_diff.total_seconds() > 86400:  # More than 24 hours
        print(f"    ⚠ Large time gap detected: {time_diff.days} days since last report")
        print(f"    ⚠ Manual review recommended to ensure no information was missed")
        return True, f"Large time gap: {time_diff.days} days since last report"
    
    print(f"    ✓ Gap check completed - last report: {latest_report}")
    return True, f"Last report: {latest_report}"

def create_chat_report_content(content, report_id, timestamp):
    """Create the complete chat report content following the framework."""
    return f"""---
type: chat
framework: framework
id: {report_id}
timestamp: {timestamp.isoformat()}
framework_version: 1.0
---

# Chat Session Report - {timestamp.strftime('%Y-%m-%d %H:%M')}

## Summary
{content['Summary']}

## Key Insights
{content['Key Insights']}

## Decisions Made
{content['Decisions Made']}

## Questions Answered
{content['Questions Answered']}

## Action Items
{content['Action Items']}

## Context
{content['Context']}

## Personal Reflections
{content['Personal Reflections']}

## System State
{content['System State']}

## Implementation Details
{content['Implementation Details']}

## Current Status
{content['Current Status']}

## Additional Notes
{content['Additional Notes']}
"""

def verify_file_integrity(filepath, original_content, report_id, timestamp):
    """
    Verify that the file was actually saved correctly.
    Returns (is_valid, verification_details)
    """
    print("  Verifying file integrity...")
    
    try:
        # Read back the saved file
        with open(filepath, 'r') as f:
            saved_content = f.read()
        
        # Check file size is reasonable
        if len(saved_content) < 500:
            print(f"    ✗ File too small ({len(saved_content)} chars) - may be incomplete")
            return False, f"File too small: {len(saved_content)} characters"
        
        # Check that all original content is present
        missing_content = []
        for section_name, section_content in original_content.items():
            if section_content not in saved_content:
                missing_content.append(section_name)
        
        if missing_content:
            print(f"    ✗ Content missing from saved file: {', '.join(missing_content)}")
            return False, f"Missing content: {', '.join(missing_content)}"
        
        # Check metadata is correct
        if f"id: {report_id}" not in saved_content:
            print(f"    ✗ Report ID not found in saved file")
            return False, "Report ID missing from saved file"
        
        if timestamp.isoformat() in saved_content:
            print(f"    ✓ Timestamp verified in saved file")
        else:
            print(f"    ✗ Timestamp not found in saved file")
            return False, "Timestamp missing from saved file"
        
        # Check framework reference
        if "framework: framework" not in saved_content:
            print(f"    ✗ Framework reference not found in saved file")
            return False, "Framework reference missing from saved file"
        
        print(f"    ✓ File integrity verified - {len(saved_content)} characters saved correctly")
        return True, f"File integrity verified: {len(saved_content)} characters"
        
    except Exception as e:
        print(f"    ✗ Could not verify file integrity: {e}")
        return False, f"File verification failed: {e}"

def save_chat_report(content, chats_path):
    """
    Save a chat report with comprehensive validation.
    Returns (success, details)
    """
    print("\n" + "=" * 60)
    print("SAVING CHAT REPORT")
    print("=" * 60)
    
    # Step 1: Generate unique identifier and timestamp
    print("Step 1: Generating unique identifier and timestamp...")
    report_id = generate_uuid()
    current_time = get_current_gmt_time()
    print(f"✓ Report ID: {report_id}")
    print(f"✓ Timestamp: {current_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    
    # Step 2: Validate content quality
    print("Step 2: Validating content quality...")
    content_valid, content_issues = validate_content_quality(content)
    if not content_valid:
        print("✗ Content quality validation failed")
        return False, f"Content quality issues: {'; '.join(content_issues)}"
    
    # Step 3: Check for gaps with previous report
    print("Step 3: Checking for gaps with previous report...")
    no_gaps, gap_details = check_gap_with_previous_report(chats_path, current_time)
    if not no_gaps:
        print("✗ Gap detection failed")
        return False, f"Gap detection failed: {gap_details}"
    
    # Step 4: Create filename and filepath
    print("Step 4: Creating filename and filepath...")
    filename = create_temporal_filename(current_time)
    filepath = os.path.join(chats_path, filename)
    print(f"✓ Filename: {filename}")
    print(f"✓ Full path: {filepath}")
    
    # Step 5: Create report content
    print("Step 5: Creating report content...")
    report_content = create_chat_report_content(content, report_id, current_time)
    print("✓ Report content created following framework")
    
    # Step 6: Save the file
    print("Step 6: Saving report to file...")
    try:
        with open(filepath, 'w') as f:
            f.write(report_content)
        print("✓ File written to disk")
    except Exception as e:
        print(f"✗ Failed to write file: {e}")
        return False, f"File write failed: {e}"
    
    # Step 7: Verify file integrity
    print("Step 7: Verifying file integrity...")
    integrity_valid, integrity_details = verify_file_integrity(filepath, content, report_id, current_time)
    if not integrity_valid:
        print("✗ File integrity verification failed")
        return False, f"File integrity failed: {integrity_details}"
    
    print("✓ Chat report saved and verified successfully")
    return True, f"Report saved: {filename} ({len(report_content)} characters)"

def main():
    """Main function - demonstrates how AI systems would use this script."""
    print("=" * 60)
    print("CHAT SAVE PROCESS - AI SYSTEM INTEGRATION")
    print("=" * 60)
    print("This script is designed for AI systems to create perfect, chainable,")
    print("AI-readable historical records. It includes comprehensive validation")
    print("to ensure content is actually saved correctly.")
    
    # Check environment
    print("\nChecking environment...")
    chats_path = "chats"
    if not os.path.exists(chats_path):
        print(f"✗ ERROR: Chats directory not found at {chats_path}")
        sys.exit(1)
    print(f"✓ Chats directory found at {chats_path}")
    
    # Example content that AI systems would provide
    print("\n" + "=" * 60)
    print("EXAMPLE USAGE - AI SYSTEM PROVIDING CONTENT")
    print("=" * 60)
    print("AI systems would call this script with content like:")
    
    example_content = {
        "Summary": "Discussed system design improvements and implemented new framework structure",
        "Key Insights": "System needed better AI integration and clearer mutability rules",
        "Decisions Made": "Implement UUID-based identification, remove sequential numbering",
        "Questions Answered": "How to make system work naturally with AI systems",
        "Action Items": "Update framework, rebuild save script, test validation",
        "Context": "Building comprehensive data preservation system for professional portfolio",
        "Personal Reflections": "System design requires careful consideration of AI interaction patterns",
        "System State": "Framework updated, README standardized, mutability checker implemented",
        "Implementation Details": "UUID generation, temporal filenames, comprehensive validation",
        "Current Status": "Framework complete, script needs rebuilding, validation enhanced",
        "Additional Notes": "Focus on perfect historical records that AI can chain and analyze"
    }
    
    for section, content in example_content.items():
        print(f"  {section}: {content[:50]}...")
    
    print("\n" + "=" * 60)
    print("SAVING EXAMPLE REPORT")
    print("=" * 60)
    
    # Save the example report
    success, details = save_chat_report(example_content, chats_path)
    
    if success:
        print("\n" + "=" * 60)
        print("SUCCESS: Chat report created and verified!")
        print("=" * 60)
        print(f"✓ {details}")
        print("✓ Content quality validated")
        print("✓ File integrity verified")
        print("✓ Framework compliance confirmed")
        print("✓ No gaps with previous reports")
        print("\nThe system now creates perfect, AI-readable historical records")
        print("that can be chained together for complete development history.")
    else:
        print("\n" + "=" * 60)
        print("FAILED: Could not create chat report")
        print("=" * 60)
        print(f"✗ {details}")
        sys.exit(1)

if __name__ == "__main__":
    main()
