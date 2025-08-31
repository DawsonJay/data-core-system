#!/usr/bin/env python3
"""
Chat Health Check Process - AI-FIRST HEALTH MONITORING
Continuously monitors chat system health with comprehensive validation and reporting.
Follows Data Core System principles: zero information loss, data immutability, proactive monitoring.
"""

import os
import sys
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Tuple, Optional

def get_current_gmt_time():
    """Get current GMT time for timestamps."""
    return datetime.now(timezone.utc)

def auto_extract_context_if_available():
    """
    AUTO-EXTRACT conversation context if available for enhanced validation.
    This is optional for health checks - system can validate without it.
    """
    print("  Auto-extracting conversation context if available...")
    
    try:
        # Method 1: Check if conversation context was passed as argument
        if len(sys.argv) > 1:
            context = sys.argv[1]
            print(f"    ✓ Live conversation context found ({len(context)} chars)")
            return context
            
        # Method 2: Environment variable (for AI systems that can set this)
        env_context = os.environ.get('CHAT_CONTEXT')
        if env_context:
            print(f"    ✓ Conversation context found in environment ({len(env_context)} chars)")
            return env_context
            
        # Method 3: Attempt to read from stdin (for piped input)
        if not sys.stdin.isatty():
            context = sys.stdin.read().strip()
            if context:
                print(f"    ✓ Conversation context read from stdin ({len(context)} chars)")
                return context
        
        # No context available - this is fine for health checks
        print("    ⚠ No live conversation context available (health check will proceed without enhanced validation)")
        return None
        
    except Exception as e:
        print(f"    ⚠ Context extraction failed: {e} (proceeding without enhanced validation)")
        return None

def validate_chats_directory(chats_dir: str) -> Tuple[bool, str]:
    """Validate chats directory exists and is accessible."""
    print("  Validating chats directory structure...")
    
    if not os.path.exists(chats_dir):
        print(f"    ✗ Chats directory not found: {chats_dir}")
        return False, f"Chats directory not found: {chats_dir}"
    
    if not os.path.isdir(chats_dir):
        print(f"    ✗ Chats path is not a directory: {chats_dir}")
        return False, f"Chats path is not a directory: {chats_dir}"
    
    try:
        # Test read access
        os.listdir(chats_dir)
        print(f"    ✓ Chats directory validated: {chats_dir}")
        return True, f"Directory accessible at {chats_dir}"
    except PermissionError:
        print(f"    ✗ Permission denied accessing: {chats_dir}")
        return False, f"Permission denied accessing: {chats_dir}"
    except Exception as e:
        print(f"    ✗ Error accessing directory: {e}")
        return False, f"Error accessing directory: {e}"

def discover_chat_files(chats_dir: str) -> Tuple[bool, List[str], str]:
    """Discover and validate chat files in the directory."""
    print("  Discovering chat files...")
    
    try:
        all_files = os.listdir(chats_dir)
        chat_files = [f for f in all_files if f.startswith("chat-") and f.endswith(".md")]
        
        if not chat_files:
            print("    ✗ No chat files found matching pattern chat-*.md")
            return False, [], "No chat files found"
        
        # Sort chronologically (newest first for health check focus)
        chat_files.sort(reverse=True)
        print(f"    ✓ Discovered {len(chat_files)} chat files")
        
        return True, chat_files, f"Found {len(chat_files)} chat files"
        
    except Exception as e:
        print(f"    ✗ Error discovering files: {e}")
        return False, [], f"Discovery error: {e}"

def analyze_chat_file(filepath: str, filename: str) -> Dict:
    """Analyze a single chat file with comprehensive validation."""
    print(f"    Analyzing {filename}...")
    
    analysis = {
        'filename': filename,
        'valid': True,
        'issues': [],
        'timestamp': None,
        'summary': '',
        'size': 0,
        'framework_compliant': False,
        'sections_found': 0
    }
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        analysis['size'] = len(content)
        
        # Parse timestamp from filename
        timestamp = parse_temporal_filename(filename)
        if timestamp:
            analysis['timestamp'] = timestamp
            print(f"      ✓ Timestamp parsed: {timestamp.strftime('%Y-%m-%d %H:%M')} GMT")
        else:
            analysis['issues'].append("Invalid timestamp format in filename")
            analysis['valid'] = False
            print(f"      ✗ Invalid timestamp format")
        
        # Check file size
        if len(content) < 1000:
            analysis['issues'].append(f"File too small ({len(content)} chars) - minimum 1000 expected")
            analysis['valid'] = False
            print(f"      ✗ File too small: {len(content)} characters")
        else:
            print(f"      ✓ File size adequate: {len(content)} characters")
        
        # Check Framework v1.1 compliance
        if "framework_version: 1.1" in content:
            analysis['framework_compliant'] = True
            print("      ✓ Framework v1.1 compliant")
        else:
            analysis['issues'].append("Missing Framework v1.1 compliance")
            analysis['valid'] = False
            print("      ✗ Not Framework v1.1 compliant")
        
        # Count required sections
        required_sections = [
            "## Summary", "## Key Insights", "## Decisions Made", "## Questions Answered",
            "## Action Items", "## Context", "## Personal Reflections", "## System State",
            "## Implementation Details", "## Current Status", "## Additional Notes", "## Technical Specifications"
        ]
        
        sections_found = sum(1 for section in required_sections if section in content)
        analysis['sections_found'] = sections_found
        
        if sections_found >= 12:  # All sections present
            print(f"      ✓ All required sections present ({sections_found}/12)")
        else:
            missing_count = 12 - sections_found
            analysis['issues'].append(f"Missing {missing_count} required Framework v1.1 sections")
            analysis['valid'] = False
            print(f"      ✗ Missing sections: {sections_found}/12 found")
        
        # Extract summary for timeline
        analysis['summary'] = extract_summary_from_content(content)
        
        if analysis['valid']:
            print(f"      ✓ Analysis complete - file validated")
        else:
            print(f"      ✗ Analysis complete - {len(analysis['issues'])} issues found")
            
    except Exception as e:
        analysis['valid'] = False
        analysis['issues'].append(f"Error reading file: {e}")
        print(f"      ✗ Error analyzing file: {e}")
    
    return analysis

def parse_temporal_filename(filename: str) -> Optional[datetime]:
    """Parse timestamp from filename format: chat-YYYY-MM-DD-HH-MM.md"""
    try:
        # Remove .md extension and split on hyphens
        parts = filename.replace('.md', '').split('-')
        if len(parts) >= 5 and parts[0] == 'chat':
            year, month, day, hour, minute = parts[1:6]
            return datetime(int(year), int(month), int(day), int(hour), int(minute), tzinfo=timezone.utc)
    except (ValueError, IndexError):
        pass
    return None

def extract_summary_from_content(content: str) -> str:
    """Extract comprehensive summary from file content for timeline verification."""
    try:
        # Try to extract the Summary section first (most reliable)
        if '## Summary' in content:
            start = content.find('## Summary') + len('## Summary')
            end = content.find('##', start)
            if end == -1:
                end = start + 300  # Allow more content for better verification
            summary = content[start:end].strip()
            
            # Clean up the summary content
            summary = ' '.join(summary.split())  # Normalize whitespace
            
            if len(summary) > 20:  # If we got meaningful content
                return summary
        
        # Fallback: Try to extract from Key Insights if Summary is empty
        if '## Key Insights' in content:
            start = content.find('## Key Insights') + len('## Key Insights')
            end = content.find('##', start)
            if end == -1:
                end = start + 300
            insights = content[start:end].strip()
            insights = ' '.join(insights.split())
            
            if len(insights) > 20:
                return f"Key Insights: {insights}"
        
        # Final fallback: Try to extract from the beginning of content after metadata
        lines = content.split('\n')
        content_started = False
        extracted_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('#') and not line.startswith('##'):  # Found main title
                content_started = True
                continue
            elif content_started and line and not line.startswith('#'):
                extracted_lines.append(line)
                if len(' '.join(extracted_lines)) > 200:
                    break
        
        if extracted_lines:
            fallback_summary = ' '.join(extracted_lines)
            return f"Content: {fallback_summary}"
            
    except Exception as e:
        return f"Summary extraction error: {str(e)[:50]}"
    
    return "No meaningful summary content found"

def validate_timeline_continuity(analyses: List[Dict]) -> Tuple[bool, List[str]]:
    """Validate timeline continuity and detect gaps."""
    print("  Validating timeline continuity...")
    
    if not analyses:
        print("    ⚠ No files to validate")
        return True, []
    
    # Sort chronologically
    valid_analyses = [a for a in analyses if a['timestamp']]
    valid_analyses.sort(key=lambda x: x['timestamp'])
    
    issues = []
    
    # Check for gaps between consecutive files
    for i in range(len(valid_analyses) - 1):
        current = valid_analyses[i]
        next_file = valid_analyses[i + 1]
        
        time_diff = next_file['timestamp'] - current['timestamp']
        
        # Check for overlaps (impossible timestamps)
        if time_diff.total_seconds() < 0:
            issues.append(f"Timeline overlap: {current['filename']} after {next_file['filename']}")
            print(f"    ✗ Timeline overlap detected")
        
        # Check for large gaps (>6 hours suggests missing sessions)
        elif time_diff.total_seconds() > 21600:  # 6 hours
            hours = time_diff.total_seconds() / 3600
            issues.append(f"Large gap: {hours:.1f} hours between {current['filename']} and {next_file['filename']}")
            print(f"    ⚠ Large gap detected: {hours:.1f} hours")
    
    if not issues:
        print("    ✓ Timeline continuity validated - no significant gaps")
    
    return len(issues) == 0, issues

def validate_against_live_context(analyses: List[Dict], live_context: str) -> Tuple[bool, List[str]]:
    """Validate recent analyses against live conversation context."""
    print("  Validating against live conversation context...")
    
    if not live_context:
        print("    ⚠ No live context provided - skipping enhanced validation")
        return True, []
    
    if not analyses:
        print("    ⚠ No chat files to validate against")
        return True, []
    
    issues = []
    
    # Check if this might be a continuing session
    recent_files = analyses[:2] if len(analyses) > 1 else analyses  # Check first 2 files (most recent)
    current_time = get_current_gmt_time()
    
    # Check temporal alignment
    if recent_files:
        latest_timestamp = max(a['timestamp'] for a in recent_files if a['timestamp'])
        time_since_latest = current_time - latest_timestamp
        
        # If latest file is very recent (< 2 hours), expect some content alignment
        if time_since_latest.total_seconds() < 7200:  # 2 hours
            # Display time difference in user-friendly format
            minutes_ago = time_since_latest.total_seconds() / 60
            if minutes_ago < 60:
                time_display = f"{minutes_ago:.0f} minutes ago"
            else:
                hours_ago = time_since_latest.total_seconds() / 3600
                time_display = f"{hours_ago:.1f}h ago"
            print(f"    ⚠ Recent session detected ({time_display})")
            
            # Look for any content overlap (soft validation)
            live_lower = live_context.lower()
            content_found = False
            
            for analysis in recent_files:
                if analysis['summary']:
                    summary_words = [w for w in analysis['summary'].lower().split() if len(w) > 5]
                    for word in summary_words[:5]:  # Check first few meaningful words
                        if word in live_lower:
                            content_found = True
                            break
                if content_found:
                    break
            
            if not content_found:
                issues.append("Recent chat files don't appear to reflect current conversation context")
                print("    ⚠ Limited content alignment with recent files")
            else:
                print("    ✓ Content alignment detected with recent files")
        else:
            print(f"    ✓ No recent session detected - no context alignment expected")
    
    return len(issues) == 0, issues

def generate_comprehensive_report(analyses: List[Dict], timeline_issues: List[str], context_issues: List[str]) -> Dict:
    """Generate comprehensive health report."""
    print("  Generating comprehensive health report...")
    
    if not analyses:
        return {
            'healthy': False,
            'total_files': 0,
            'valid_files': 0,
            'issues': ['No chat files found for analysis'],
            'timeline': [],
            'summary': 'No data available'
        }
    
    # Calculate statistics
    valid_files = [a for a in analyses if a['valid']]
    invalid_files = [a for a in analyses if not a['valid']]
    
    # Generate timeline (most recent files first)
    timeline = []
    for analysis in analyses[:5]:  # Show 5 most recent
        if analysis['timestamp']:
            timeline.append({
                'timestamp': analysis['timestamp'],
                'filename': analysis['filename'],
                'summary': analysis['summary'],
                'valid': analysis['valid'],
                'size': analysis['size']
            })
    
    # Collect all issues
    all_issues = []
    for analysis in invalid_files:
        for issue in analysis['issues']:
            all_issues.append(f"{analysis['filename']}: {issue}")
    
    all_issues.extend(timeline_issues)
    all_issues.extend(context_issues)
    
    # Calculate time span (display in local time for user readability)
    timestamps = [a['timestamp'] for a in analyses if a['timestamp']]
    time_span = "Unknown"
    duration = "Unknown"
    
    if timestamps:
        timestamps.sort()
        earliest = timestamps[0]
        latest = timestamps[-1]
        
        # Convert to local time for display
        earliest_local = earliest.replace(tzinfo=timezone.utc).astimezone()
        latest_local = latest.replace(tzinfo=timezone.utc).astimezone()
        time_span = f"{earliest_local.strftime('%H:%M')} - {latest_local.strftime('%H:%M')} (local)"
        
        diff = latest - earliest
        if diff.total_seconds() < 3600:
            duration = f"{int(diff.total_seconds() / 60)} minutes"
        else:
            hours = int(diff.total_seconds() / 3600)
            minutes = int((diff.total_seconds() % 3600) / 60)
            duration = f"{hours}h {minutes}m"
    
    # Determine overall health
    healthy = (len(valid_files) == len(analyses) and 
              len(timeline_issues) == 0 and 
              len(context_issues) == 0)
    
    report = {
        'healthy': healthy,
        'total_files': len(analyses),
        'valid_files': len(valid_files),
        'invalid_files': len(invalid_files),
        'framework_compliant': sum(1 for a in analyses if a.get('framework_compliant', False)),
        'issues': all_issues,
        'timeline': timeline,
        'summary': {
            'files_checked': len(analyses),
            'time_span': time_span,
            'total_duration': duration,
            'health_status': 'HEALTHY' if healthy else 'ISSUES DETECTED'
        }
    }
    
    print(f"    ✓ Health report generated - {len(analyses)} files analyzed")
    return report

def display_health_results(report: Dict) -> None:
    """Display comprehensive health check results."""
    print("  Displaying comprehensive health results...")
    
    # Summary Statistics
    print(f"\n    📊 HEALTH SUMMARY:")
    print(f"       Files analyzed: {report['total_files']}")
    print(f"       Valid files: {report['valid_files']}")
    if report['invalid_files'] > 0:
        print(f"       Invalid files: {report['invalid_files']}")
    print(f"       Framework v1.1 compliant: {report['framework_compliant']}")
    
    if report['summary']:
        print(f"       Time span: {report['summary']['time_span']}")
        print(f"       Total duration: {report['summary']['total_duration']}")
        print(f"       Status: {report['summary']['health_status']}")
    
    # Detailed Recent Timeline for User Verification
    if report['timeline']:
        print(f"\n    📅 DETAILED TIMELINE - LAST 5 RECORDS:")
        print(f"       (Showing detailed content for manual verification)")
        print()
        
        for i, item in enumerate(report['timeline'], 1):
            status = "✅" if item['valid'] else "❌"
            
            # Display timestamp in local time for user readability
            # (while keeping all stored data in GMT)
            gmt_timestamp = item['timestamp']
            local_timestamp = gmt_timestamp.replace(tzinfo=timezone.utc).astimezone()
            timestamp_display = f"{local_timestamp.strftime('%H:%M')} (GMT: {gmt_timestamp.strftime('%H:%M')})"
            size = f"{item['size']} chars"
            
            # Show more detailed summary (up to 200 chars for better context)
            summary = item['summary']
            if len(summary) > 200:
                summary = summary[:200] + '...'
            
            print(f"       {i}. {status} {timestamp_display} ({size})")
            print(f"          {summary}")
            print()
    
    # Issues Found
    if report['issues']:
        print(f"    ⚠️  ISSUES DETECTED:")
        for issue in report['issues']:
            print(f"       - {issue}")
        print()
    
    print("    ✓ Detailed health results displayed for manual verification")

def main():
    """Main AI-first health check process."""
    print("=" * 70)
    print("CHAT HEALTH CHECK PROCESS - AI-FIRST SYSTEM MONITORING")
    print("=" * 70)
    print("Comprehensive chat system health monitoring with proactive issue detection.")
    print("Zero manual intervention required - designed for AI systems.")
    
    # Step 1: Environment validation
    print("\n" + "=" * 70)
    print("STEP 1: ENVIRONMENT VALIDATION")
    print("=" * 70)
    
    chats_dir = "chats"
    dir_valid, dir_message = validate_chats_directory(chats_dir)
    if not dir_valid:
        print("✗ CRITICAL: Environment validation failed")
        print(f"  Issue: {dir_message}")
        print("  Health check cannot proceed without accessible chats directory")
        sys.exit(1)
    print("✓ Environment validation complete")
    
    # Step 2: Context extraction (optional for health checks)
    print("\n" + "=" * 70)
    print("STEP 2: AUTO-EXTRACT CONVERSATION CONTEXT (OPTIONAL)")
    print("=" * 70)
    
    live_context = auto_extract_context_if_available()
    print("✓ Context extraction complete")
    
    # Step 3: File discovery
    print("\n" + "=" * 70)
    print("STEP 3: CHAT FILE DISCOVERY")
    print("=" * 70)
    
    files_found, chat_files, discovery_message = discover_chat_files(chats_dir)
    if not files_found:
        print("✗ CRITICAL: No chat files found for health monitoring")
        print(f"  Issue: {discovery_message}")
        print("  System cannot monitor health without chat files")
        sys.exit(1)
    print(f"✓ File discovery complete: {discovery_message}")
    
    # Step 4: File analysis
    print("\n" + "=" * 70)
    print("STEP 4: COMPREHENSIVE FILE ANALYSIS")
    print("=" * 70)
    
    analyses = []
    for filename in chat_files[:10]:  # Analyze 10 most recent files
        filepath = os.path.join(chats_dir, filename)
        analysis = analyze_chat_file(filepath, filename)
        analyses.append(analysis)
    
    print(f"✓ File analysis complete - {len(analyses)} files analyzed")
    
    # Step 5: Timeline validation
    print("\n" + "=" * 70)
    print("STEP 5: TIMELINE CONTINUITY VALIDATION")
    print("=" * 70)
    
    timeline_valid, timeline_issues = validate_timeline_continuity(analyses)
    if timeline_valid:
        print("✓ Timeline continuity validated")
    else:
        print(f"⚠ Timeline issues detected: {len(timeline_issues)} issues")
    
    # Step 6: Live context validation (if available)
    print("\n" + "=" * 70)
    print("STEP 6: LIVE CONTEXT VALIDATION")
    print("=" * 70)
    
    context_valid, context_issues = validate_against_live_context(analyses, live_context)
    if context_valid:
        print("✓ Live context validation complete")
    else:
        print(f"⚠ Context alignment issues detected: {len(context_issues)} issues")
    
    # Step 7: Generate comprehensive report
    print("\n" + "=" * 70)
    print("STEP 7: COMPREHENSIVE REPORT GENERATION")
    print("=" * 70)
    
    health_report = generate_comprehensive_report(analyses, timeline_issues, context_issues)
    print("✓ Health report generation complete")
    
    # Step 8: Display results
    print("\n" + "=" * 70)
    print("STEP 8: HEALTH RESULTS DISPLAY")
    print("=" * 70)
    
    display_health_results(health_report)
    print("✓ Health results display complete")
    
    # Final health status report
    print("\n" + "=" * 70)
    if health_report['healthy']:
        print("SUCCESS: CHAT SYSTEM HEALTH CHECK PASSED")
        print("=" * 70)
        print("✓ All chat files validated successfully")
        print("✓ Timeline continuity confirmed")
        print("✓ Framework v1.1 compliance verified")
        print("✓ Zero critical issues detected")
        print("✓ System ready for continued operation")
        exit_code = 0
    else:
        print("WARNING: CHAT SYSTEM HEALTH ISSUES DETECTED")
        print("=" * 70)
        print(f"⚠ {len(health_report['issues'])} issues require attention")
        print(f"⚠ {health_report['invalid_files']} invalid files detected")
        print("⚠ System operational but monitoring required")
        print("⚠ Review issues above for data integrity")
        exit_code = 1
    
    # Show completion time in both local and GMT for clarity
    gmt_time = get_current_gmt_time()
    local_time = gmt_time.replace(tzinfo=timezone.utc).astimezone()
    print(f"✓ Health check completed at {local_time.strftime('%Y-%m-%d %H:%M:%S')} (local) / {gmt_time.strftime('%H:%M:%S')} GMT")
    print("✓ AI-first design - no manual intervention required")
    
    return exit_code == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
