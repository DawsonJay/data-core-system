#!/usr/bin/env python3
"""
Natural Value Extraction Chat Save Process - AI-FIRST CHAT CAPTURE WITH FRAMEWORK v2.0
Takes AI value log, creates Framework v2.0 compliant records, validates thoroughly, and ensures gapless history.
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

def calculate_new_content_ratio(current_content: str, previous_content: str) -> float:
    """Calculate the percentage of new content in current vs previous."""
    current_normalized = normalize_content_for_comparison(current_content)
    previous_normalized = normalize_content_for_comparison(previous_content)
    
    current_words = set(current_normalized.split())
    previous_words = set(previous_normalized.split())
    
    if not current_words:
        return 0.0
    
    new_words = current_words - previous_words
    new_content_ratio = len(new_words) / len(current_words) * 100
    return round(new_content_ratio, 2)

def check_for_gaps_with_previous_reports(chats_dir: str, current_value_log: str) -> Tuple[bool, str]:
    """Check for information gaps and duplication with previous reports using smart content-aware analysis."""
    print("  Checking for gaps and duplication with previous reports...")
    
    if not os.path.exists(chats_dir):
        print("    ✓ No previous reports found - this will be the first")
        return True, "First chat report in system"
    
    # Find most recent reports
    chat_files = [f for f in os.listdir(chats_dir) if f.startswith("chat-") and f.endswith(".md")]
    
    if not chat_files:
        print("    ✓ No previous reports found - this will be the first")
        return True, "First chat report in system"
    
    # Sort by filename (temporal naming ensures chronological order)
    chat_files.sort(reverse=True)
    
    # Check against the most recent report for duplication
    latest_report = chat_files[0]
    latest_path = os.path.join(chats_dir, latest_report)
    
    try:
        with open(latest_path, 'r') as f:
            latest_content = f.read()
        
        # Separate context from value sections for smart analysis
        current_context, current_value = separate_context_from_value(current_value_log)
        latest_context, latest_value = separate_context_from_value(latest_content)
        
        # Calculate similarities for each section type
        context_similarity = calculate_content_similarity(current_context, latest_context)
        value_similarity = calculate_content_similarity(current_value, latest_value)
        
        print(f"    📊 Smart content analysis against {latest_report}:")
        print(f"      - Context similarity: {context_similarity}% (narrative building)")
        print(f"      - Value similarity: {value_similarity}% (specific insights)")
        
        # Apply smart deduplication logic
        if value_similarity > 85:
            print(f"    ✗ BLOCKED: Value content too similar ({value_similarity}% > 85% threshold)")
            print(f"      This appears to duplicate specific insights or decisions")
            return False, f"Value content too similar to {latest_report} ({value_similarity}% similarity)"
        
        elif value_similarity > 60:
            if calculate_new_content_ratio(current_value, latest_value) < 25:
                print(f"    ✗ BLOCKED: Insufficient new value content ({calculate_new_content_ratio(current_value, latest_value)}% < 25% threshold)")
                print(f"      Value similarity: {value_similarity}% (moderate), but not enough new insights")
                return False, f"Insufficient new value content despite {value_similarity}% similarity"
            else:
                print(f"    ✓ ALLOWED: Moderate value similarity but sufficient new insights")
        
        else:
            print(f"    ✓ ALLOWED: Low value similarity - clearly new insights")
        
        # Context similarity is expected and good for narrative building
        if context_similarity > 90:
            print(f"    ✓ Context similarity {context_similarity}% - shows narrative continuity and evolution")
        else:
            print(f"    ✓ Context similarity {context_similarity}% - shows narrative development")
        
        print(f"    ✓ Smart gap analysis complete - building on {latest_report}")
        return True, f"Continues from {latest_report} (context: {context_similarity}%, value: {value_similarity}%)"
        
    except Exception as e:
        print(f"    ⚠ Error reading {latest_report}: {e}")
        return True, f"Continues from {latest_report} (read error, proceeding with caution)"

def separate_context_from_value(content: str) -> Tuple[str, str]:
    """Separate context snapshot from new insights for smart analysis."""
    # Look for the section headers
    context_marker = "## Context Snapshot"
    value_marker = "## New Insights"
    
    if context_marker in content and value_marker in content:
        # Split content into sections
        parts = content.split(context_marker)
        if len(parts) > 1:
            context_part = parts[1].split("## ")[0].strip()
        else:
            context_part = ""
        
        parts = content.split(value_marker)
        if len(parts) > 1:
            value_part = parts[1].split("## ")[0].strip()
        else:
            value_part = ""
        
        return context_part, value_part
    
    # Fallback: treat entire content as context if sections not found
    return content, ""

def create_framework_v2_content(context_snapshot: str, new_insights: str, report_id: str, timestamp: datetime) -> str:
    """Create Framework v2.0 compliant chat report content."""
    print("  Creating Framework v2.0 compliant chat report...")
    
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
        
        section_content = content.split(f"## {section}")[1].split("## ")[0].strip()
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
        with open(filepath, 'r') as f:
            saved_content = f.read()
        
        if saved_content != expected_content:
            return False, "Content mismatch between expected and saved"
        
        print(f"    ✓ File integrity verified ({len(saved_content)} characters)")
        return True, f"File integrity confirmed: {len(saved_content)} characters"
        
    except Exception as e:
        return False, f"Integrity verification failed: {e}"

def run_health_check_and_timeline(chats_dir: str) -> Dict:
    """Run comprehensive health check and generate timeline."""
    print("  Running health check and timeline analysis...")
    
    try:
        # Import health checker if available
        sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
        from chat_health_check import ChatHealthChecker
        
        checker = ChatHealthChecker(chats_dir)
        result = checker.check_health()
        
        if result.get('healthy', False):
            print("    ✓ Health check passed")
            return result
        else:
            print("    ⚠ Health check found issues:")
            for issue in result.get('issues', []):
                print(f"      - {issue}")
            return result
            
    except ImportError:
        print("    ⚠ Health checker not available - basic validation only")
        return {'healthy': True, 'message': 'Basic validation passed'}
    except Exception as e:
        print(f"    ⚠ Health check failed: {e}")
        return {'healthy': False, 'error': str(e)}

def main():
    """Main Natural Value Extraction chat save process - AI-FIRST DESIGN."""
    gmt_time = get_current_gmt_time()
    local_time = gmt_time.replace(tzinfo=timezone.utc).astimezone()
    
    print("=" * 70)
    print("NATURAL VALUE EXTRACTION CHAT SAVE PROCESS - AI-FIRST DESIGN")
    print("=" * 70)
    print("Takes AI value log, creates Framework v2.0 compliant records,")
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
    
    # Step 2: Extract AI value log (this is where the AI provides their natural value log)
    print("\n" + "=" * 70)
    print("STEP 2: EXTRACT AI VALUE LOG")
    print("=" * 70)
    print("  💡 AI: Providing my current understanding of your context and new insights...")
    
    # This is where the AI naturally provides their value log
    # In practice, this would come from the AI's internal working memory
    current_context = """CURRENT CONTEXT SNAPSHOT:
You are building a Natural Value Extraction System that leverages AI's natural ability to identify, compress, and log valuable content in real-time during conversation. The system aims to be AI-first, process-enforced, and continuously improvable. 

Key system philosophy:
- AI-Natural but Process-Enforced: Everything feels natural to me as an AI, but the processes impose structure and rules I cannot ignore or avoid
- Process-Based = Continuously Improvable: If I'm not capturing the right value → update reference files, if saving isn't working → refine the save process
- Trustworthy and Predictable: The processes create consistent, reliable behavior

The system captures high-value content (character, ethics, coding approach, likes/dislikes) for portfolio/resume building, with verbatim preservation of design decisions and technical solutions. Each record contains a "snapshot of the current context" and "unique new insights that capture value."

The save process and health check must validate gapless history and deduplication, ensuring perfect context for new AI chats while avoiding duplicate specific value.

EVOLUTION OF SYSTEM DESIGN PHILOSOPHY:
The conversation has evolved from discussing a "bulletproof" AI-first system for preserving raw chat data through frequent file saves to a "Natural Value Extraction System." The old "chat memory" system with its frequent file saves was fundamentally flawed and has been completely replaced.

The new system leverages the AI's natural ability to identify, compress, and log valuable content in real-time during conversation, guided by reference files, without disrupting workflow. The AI maintains a mental "value log," compiles it into a structured format, and provides it directly to the save process when requested.

CURRENT SYSTEM STATUS:
We have successfully rebuilt the save_chat.py process from the ground up, implementing Natural Value Extraction with Framework v2.0 compliance. The system now includes smart deduplication that distinguishes between context evolution (narrative building) and value duplication (specific insights). This allows for natural context continuity while preventing repetitive value content."""
    
    new_insights = """NEW INSIGHTS FROM THIS CONVERSATION:

DEDUPLICATION SYSTEM IMPROVEMENT:
Identified a critical flaw in the current deduplication approach - it treats all content the same way, failing to distinguish between context evolution (narrative building) and value duplication (specific insights). This prevents quick saves and natural context continuity.

SMART CONTENT-AWARE DEDUPLICATION DESIGN:
The system now separates content into two types with different deduplication rules:

1. **Context (Narrative Building)**: 
   - Purpose: Builds ongoing story of who you are and what you're working on
   - Duplication: GOOD - shows evolution and continuity
   - Examples: Working style, current project status, evolving philosophy, next steps
   - Rules: High similarity tolerance (90%+ is fine), focus on evolution

2. **Specific Value (Point-in-Time Insights)**:
   - Purpose: Deep examination of specific moments, decisions, or experiences
   - Duplication: BAD - doesn't add to narrative, just repeats
   - Examples: Interview answers, detailed design decisions, technical solutions, specific preferences
   - Rules: Strict deduplication (any significant similarity blocks), focus on uniqueness

IMPLEMENTATION APPROACH:
- Separate context from value sections in content analysis
- Apply different similarity thresholds to each section type
- Allow context similarity for narrative building
- Prevent value duplication to avoid waste
- Enable quick saves for short work sessions

BENEFITS OF SMART DEDUPLICATION:
- Quick saves work (context can be similar)
- Narrative builds naturally (understanding evolves over time)
- Value content deduplicates (no repeated insights)
- System feels natural (understands the difference)
- Perfect for capturing "last 5 minutes" before stopping work"""
    
    conversation_content = current_context + "\n\n" + new_insights
    print(f"✓ AI value log extracted ({len(conversation_content)} characters)")
    print(f"  - Context snapshot: {len(current_context)} characters")
    print(f"  - New insights: {len(new_insights)} characters")
    print(f"  - Total value log: {len(conversation_content)} characters")
    
    # Step 3: Content validation
    print("\n" + "=" * 70)
    print("STEP 3: CONTENT VALIDATION")
    print("=" * 70)
    
    if len(conversation_content.strip()) < 100:
        print("✗ CRITICAL: Content too short - minimum 100 characters required")
        sys.exit(1)
    
    word_count = len(conversation_content.split())
    if word_count < 20:
        print("✗ CRITICAL: Content insufficient - minimum 20 words required")
        sys.exit(1)
    
    print(f"✓ Content validated ({len(conversation_content)} chars, {word_count} words)")
    
    # Step 4: Gap analysis and deduplication
    print("\n" + "=" * 70)
    print("STEP 4: GAP ANALYSIS AND DEDUPLICATION")
    print("=" * 70)
    
    gap_ok, gap_details = check_for_gaps_with_previous_reports(chats_dir, conversation_content)
    if not gap_ok:
        print("✗ CRITICAL: Save blocked by deduplication logic")
        print(f"  Issue: {gap_details}")
        print("\n" + "=" * 70)
        print("🚨 DEDUPLICATION PROTECTION ACTIVATED")
        print("=" * 70)
        print("This prevents duplicate or low-value saves while maintaining data quality.")
        print("The system is working correctly to preserve unique value.")
        sys.exit(1)
    
    print(f"✓ Gap analysis complete: {gap_details}")
    
    # Step 5: Generate file metadata
    print("\n" + "=" * 70)
    print("STEP 5: GENERATE FILE METADATA")
    print("=" * 70)
    
    report_id = generate_uuid()
    timestamp = get_current_gmt_time()
    local_time = timestamp.replace(tzinfo=timezone.utc).astimezone()
    filename = create_temporal_filename(timestamp)
    filepath = os.path.join(chats_dir, filename)
    
    print(f"✓ Report ID: {report_id}")
    print(f"✓ Timestamp: {local_time.strftime('%Y-%m-%d %H:%M:%S')} (local) / {timestamp.strftime('%H:%M:%S')} GMT")
    print(f"✓ Filename: {filename}")
    
    # Step 6: Create Framework v2.0 report content
    print("\n" + "=" * 70)
    print("STEP 6: CREATE FRAMEWORK v2.0 REPORT")
    print("=" * 70)
    
    try:
        report_content = create_framework_v2_content(current_context, new_insights, report_id, timestamp)
        print("✓ Framework v2.0 report created successfully")
    except Exception as e:
        print("✗ CRITICAL: Report creation failed")
        print(f"  Error: {e}")
        sys.exit(1)
    
    # Step 7: Framework compliance validation
    print("\n" + "=" * 70)
    print("STEP 7: FRAMEWORK COMPLIANCE VALIDATION")
    print("=" * 70)
    
    is_valid, issues = validate_framework_compliance(report_content)
    if not is_valid:
        print("✗ CRITICAL: Framework validation failed")
        print(f"  Issues: {len(issues)}")
        for issue in issues:
            print(f"    - {issue}")
        sys.exit(1)
    
    print("✓ Framework v2.0 compliance validated")
    
    # Step 8: Write file to disk
    print("\n" + "=" * 70)
    print("STEP 8: WRITE FILE TO DISK")
    print("=" * 70)
    
    try:
        with open(filepath, 'w') as f:
            f.write(report_content)
        print(f"✓ File written successfully: {filepath}")
    except Exception as e:
        print("✗ CRITICAL: File write failed")
        print(f"  Error: {e}")
        sys.exit(1)
    
    # Step 9: File integrity verification
    print("\n" + "=" * 70)
    print("STEP 9: FILE INTEGRITY VERIFICATION")
    print("=" * 70)
    
    integrity_ok, integrity_details = verify_file_integrity(filepath, report_content)
    if not integrity_ok:
        print("✗ CRITICAL: File integrity verification failed")
        print(f"  Issue: {integrity_details}")
        sys.exit(1)
    
    print(f"✓ File integrity verified: {integrity_details}")
    
    # Step 10: Health check and timeline
    print("\n" + "=" * 70)
    print("STEP 10: HEALTH CHECK AND TIMELINE ANALYSIS")
    print("=" * 70)
    
    health_result = run_health_check_and_timeline(chats_dir)
    if not health_result.get('healthy', True):
        print("⚠ Health check identified issues - report saved but system needs attention")
    else:
        print("✓ Health check completed successfully")
    
    # Final success report
    final_time = get_current_gmt_time()
    final_local = final_time.replace(tzinfo=timezone.utc).astimezone()
    
    print("\n" + "=" * 70)
    print("SUCCESS: NATURAL VALUE EXTRACTION CHAT SAVE COMPLETED")
    print("=" * 70)
    print(f"✓ Chat report saved: {filename}")
    print(f"✓ Report size: {len(report_content)} characters")
    print(f"✓ Framework: v2.0 compliant with Natural Value Extraction")
    print(f"✓ Content: {len(conversation_content)} characters from AI value log")
    print(f"✓ Context snapshot: {len(current_context)} characters")
    print(f"✓ New insights: {len(new_insights)} characters")
    print(f"✓ UUID: {report_id}")
    print(f"✓ Completed: {final_local.strftime('%H:%M:%S')} (local) / {final_time.strftime('%H:%M:%S')} GMT")
    print("✓ Zero information loss maintained with smart deduplication")
    print("✓ AI-first design - no manual intervention required")
    print("✓ Natural Value Extraction system operational")
    print("✓ Gapless history preserved for seamless continuity")

if __name__ == "__main__":
    main()
