#!/usr/bin/env python3
"""
Chat Health Checker - Clean and Simple
Validates chat records and shows timeline of work accomplished.
"""

import os
from datetime import datetime, timezone, timedelta
from typing import Dict, List

class ChatHealthChecker:
    """Simple, focused health checker for chat records."""
    
    def __init__(self, chats_path: str = "chats"):
        self.chats_path = chats_path
    
    def check_health(self, count: int = 5, live_chat_context: str = None) -> Dict:
        """
        Check recent chat records and return health status.
        Automatically validates against live chat if provided.
        Returns: {'healthy': bool, 'timeline': list, 'issues': list}
        """
        result = {
            'healthy': True,
            'timeline': [],
            'issues': [],
            'summary': {},
            'live_chat_aligned': False
        }
        
        # Get chat files
        if not os.path.exists(self.chats_path):
            result['healthy'] = False
            result['issues'].append(f"Chats directory not found: {self.chats_path}")
            return result
        
        chat_files = [f for f in os.listdir(self.chats_path) 
                     if f.startswith("chat-") and f.endswith(".md")]
        
        if not chat_files:
            result['issues'].append("No chat files found")
            return result
        
        # Get recent files
        chat_files.sort(reverse=True)
        recent_files = chat_files[:count]
        
        # Analyze each file
        timeline = []
        for filename in recent_files:
            file_data = self._analyze_file(filename)
            if file_data:
                timeline.append(file_data)
                # Check for issues
                if not file_data['valid']:
                    result['healthy'] = False
                    result['issues'].extend(file_data['issues'])
        
        # Sort chronologically
        timeline.sort(key=lambda x: x['timestamp'])
        result['timeline'] = timeline
        
        # Check for gaps
        gap_issues = self._check_gaps(timeline)
        result['issues'].extend(gap_issues)
        if gap_issues:
            result['healthy'] = False
        
        # Validate against live chat if provided
        if live_chat_context and timeline:
            alignment_result = self._validate_live_chat_alignment(timeline, live_chat_context)
            result['live_chat_aligned'] = alignment_result['aligned']
            if not alignment_result['aligned']:
                result['issues'].extend(alignment_result['issues'])
                result['healthy'] = False
        
        # Create summary
        if timeline:
            result['summary'] = {
                'files_checked': len(timeline),
                'time_span': f"{timeline[0]['timestamp'].strftime('%H:%M')} - {timeline[-1]['timestamp'].strftime('%H:%M')}",
                'total_duration': self._calculate_duration(timeline[0]['timestamp'], timeline[-1]['timestamp'])
            }
        
        return result
    
    def _analyze_file(self, filename: str) -> Dict:
        """Analyze a single chat file."""
        try:
            filepath = os.path.join(self.chats_path, filename)
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Parse timestamp from filename
            timestamp = self._parse_timestamp(filename)
            if not timestamp:
                return {'valid': False, 'issues': [f"{filename}: Invalid timestamp format"]}
            
            # Extract key information
            summary = self._extract_summary(content)
            decisions = self._extract_decisions(content)
            actions = self._extract_actions(content)
            
            # Basic validation
            issues = []
            if len(content) < 1000:
                issues.append(f"{filename}: File too small ({len(content)} chars)")
            
            if "framework_version: 1.1" not in content:
                issues.append(f"{filename}: Missing Framework v1.1")
            
            return {
                'filename': filename,
                'timestamp': timestamp,
                'summary': summary,
                'decisions': decisions,
                'actions': actions,
                'valid': len(issues) == 0,
                'issues': issues
            }
            
        except Exception as e:
            return {'valid': False, 'issues': [f"{filename}: Error reading file - {e}"]}
    
    def _parse_timestamp(self, filename: str) -> datetime:
        """Parse timestamp from filename like chat-2025-08-31-14-40.md"""
        try:
            parts = filename.replace(".md", "").split("-")
            if len(parts) >= 5:
                year, month, day, hour, minute = parts[1:6]
                return datetime(int(year), int(month), int(day), int(hour), int(minute), tzinfo=timezone.utc)
        except:
            pass
        return None
    
    def _extract_summary(self, content: str) -> str:
        """Extract summary from content."""
        if '## Summary' in content:
            start = content.find('## Summary') + len('## Summary')
            end = content.find('##', start)
            if end == -1:
                end = start + 200
            summary = content[start:end].strip()
            return summary[:150] + "..." if len(summary) > 150 else summary
        return "No summary found"
    
    def _extract_decisions(self, content: str) -> str:
        """Extract key decisions from content."""
        if '## Decisions Made' in content:
            start = content.find('## Decisions Made') + len('## Decisions Made')
            end = content.find('##', start)
            if end == -1:
                end = start + 200
            decisions = content[start:end].strip()
            return decisions[:100] + "..." if len(decisions) > 100 else decisions
        return ""
    
    def _extract_actions(self, content: str) -> str:
        """Extract action items from content."""
        if '## Action Items' in content:
            start = content.find('## Action Items') + len('## Action Items')
            end = content.find('##', start)
            if end == -1:
                end = start + 200
            actions = content[start:end].strip()
            return actions[:100] + "..." if len(actions) > 100 else actions
        return ""
    
    def _check_gaps(self, timeline: List[Dict]) -> List[str]:
        """Check for gaps in timeline."""
        issues = []
        for i in range(len(timeline) - 1):
            current = timeline[i]
            next_record = timeline[i + 1]
            
            time_diff = next_record['timestamp'] - current['timestamp']
            
            # Check for overlaps
            if time_diff.total_seconds() < 0:
                issues.append(f"Timeline overlap: {current['filename']} after {next_record['filename']}")
            
            # Check for large gaps (>4 hours)
            elif time_diff.total_seconds() > 14400:
                hours = time_diff.total_seconds() / 3600
                issues.append(f"Large gap: {hours:.1f} hours between {current['filename']} and {next_record['filename']}")
        
        return issues
    
    def _calculate_duration(self, start: datetime, end: datetime) -> str:
        """Calculate duration between timestamps."""
        diff = end - start
        if diff.total_seconds() < 3600:
            return f"{int(diff.total_seconds() / 60)} minutes"
        else:
            hours = int(diff.total_seconds() / 3600)
            minutes = int((diff.total_seconds() % 3600) / 60)
            return f"{hours}h {minutes}m"
    
    def _validate_live_chat_alignment(self, timeline: List[Dict], live_chat_context: str) -> Dict:
        """
        Validate that saved records align with live chat context.
        Focuses on temporal consistency and topic continuity, not exact content match.
        """
        result = {'aligned': True, 'issues': []}
        
        if not timeline:
            return result
        
        # Check temporal consistency first - most important validation
        temporal_alignment = self._check_temporal_alignment(timeline, live_chat_context)
        if not temporal_alignment['valid']:
            result['aligned'] = False
            result['issues'].extend(temporal_alignment['issues'])
            return result  # If temporal alignment fails, don't check content
        
        # For content alignment, focus on the most recent records (trailing end)
        # This handles scenarios where live chat has evolved beyond saved records
        recent_records = timeline[-2:] if len(timeline) > 1 else timeline
        
        # Check if this might be a new chat session
        if self._detect_new_chat_session(timeline, live_chat_context):
            # In a new chat, we only validate that the timeline is internally consistent
            # We don't expect content alignment with current live chat
            return result
        
        # For continuing sessions, check topic continuity
        topic_alignment = self._check_topic_continuity(recent_records, live_chat_context)
        if not topic_alignment['valid']:
            result['aligned'] = False
            result['issues'].extend(topic_alignment['issues'])
        
        return result
    
    def _check_temporal_alignment(self, timeline: List[Dict], live_chat_context: str) -> Dict:
        """Check if timeline timestamps make sense with live chat context."""
        result = {'valid': True, 'issues': []}
        
        if not timeline:
            return result
        
        # Get the most recent saved timestamp
        latest_timestamp = timeline[-1]['timestamp']
        current_time = datetime.now(timezone.utc)
        
        # Check if the latest record is from the future (impossible)
        if latest_timestamp > current_time:
            result['valid'] = False
            result['issues'].append(f"Latest record timestamp is in the future: {latest_timestamp}")
            return result
        
        # Check if the latest record is too old (>4 hours) for current session
        time_diff = current_time - latest_timestamp
        if time_diff.total_seconds() > 14400:  # 4 hours
            # This might be a new session - check if live chat mentions recent times
            recent_time_patterns = [
                current_time.strftime('%H:%M'),
                (current_time - timedelta(minutes=30)).strftime('%H:%M'),
                (current_time - timedelta(hours=1)).strftime('%H:%M')
            ]
            
            if any(pattern in live_chat_context for pattern in recent_time_patterns):
                result['issues'].append(f"Large time gap: {time_diff.total_seconds()/3600:.1f} hours since last save")
        
        return result
    
    def _detect_new_chat_session(self, timeline: List[Dict], live_chat_context: str) -> bool:
        """Detect if this is a new chat session with different topics."""
        if not timeline:
            return False
        
        # Check if live chat contains session indicators
        new_session_indicators = [
            'new chat', 'different topic', 'switching to', 'new conversation',
            'starting fresh', 'new session', 'different project'
        ]
        
        live_chat_lower = live_chat_context.lower()
        return any(indicator in live_chat_lower for indicator in new_session_indicators)
    
    def _check_topic_continuity(self, recent_records: List[Dict], live_chat_context: str) -> Dict:
        """
        Check if recent records appear in live chat (directional validation).
        Live chat can contain older events not in timeline - that's fine.
        We only validate that timeline events are reflected in live chat.
        """
        result = {'valid': True, 'issues': []}
        
        if not recent_records:
            return result
        
        live_chat_lower = live_chat_context.lower()
        
        # Check each recent record to see if its content appears in live chat
        for record in recent_records:
            record_alignment = self._check_single_record_alignment(record, live_chat_lower)
            
            if not record_alignment['found']:
                # This is a soft validation - log but don't fail
                result['issues'].append(
                    f"Timeline record {record['timestamp'].strftime('%H:%M')} topics not clearly reflected in live chat"
                )
        
        # Only fail if NO recent records are reflected in live chat
        # This indicates a complete disconnect
        aligned_count = sum(1 for record in recent_records 
                          if self._check_single_record_alignment(record, live_chat_lower)['found'])
        
        if aligned_count == 0 and len(recent_records) > 0:
            result['valid'] = False
            result['issues'].append("Complete topic disconnect: no timeline records reflected in live chat")
        
        return result
    
    def _check_single_record_alignment(self, record: Dict, live_chat_lower: str) -> Dict:
        """Check if a single record's content appears in live chat."""
        result = {'found': False, 'matched_elements': []}
        
        # Extract key phrases from the record (more specific than broad topics)
        record_content = f"{record['summary']} {record['decisions']} {record['actions']}".lower()
        
        # Look for specific meaningful phrases (5+ chars, not common words)
        words = record_content.split()
        meaningful_phrases = []
        
        # Single meaningful words
        for word in words:
            if (len(word) > 6 and 
                word not in ['system', 'create', 'update', 'framework', 'structure', 
                           'implementation', 'development', 'session', 'comprehensive']):
                meaningful_phrases.append(word)
        
        # Two-word phrases
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            if (len(phrase) > 10 and 
                not any(common in phrase for common in ['system', 'create', 'update'])):
                meaningful_phrases.append(phrase)
        
        # Check if any meaningful phrases appear in live chat
        matched = []
        for phrase in meaningful_phrases:
            if phrase in live_chat_lower:
                matched.append(phrase)
        
        # Consider it found if we match at least 1 meaningful phrase
        # Or if we find the timestamp (indicating the session is current)
        timestamp_str = record['timestamp'].strftime('%H:%M')
        timestamp_found = timestamp_str in live_chat_lower
        
        if matched or timestamp_found:
            result['found'] = True
            result['matched_elements'] = matched
            if timestamp_found:
                result['matched_elements'].append(f"timestamp_{timestamp_str}")
        
        return result
    
    def display_results(self, result: Dict) -> None:
        """Display health check results in clean format."""
        print("\n🔍 Chat Health Check")
        print("=" * 50)
        
        if not result['timeline']:
            print("❌ No chat files found to check")
            return
        
        # Show summary
        if result['summary']:
            print(f"\n📊 Summary:")
            print(f"   Files checked: {result['summary']['files_checked']}")
            print(f"   Time span: {result['summary']['time_span']}")
            print(f"   Duration: {result['summary']['total_duration']}")
        
        # Show timeline
        print(f"\n📅 Timeline of Work:")
        for item in result['timeline']:
            status = "✅" if item['valid'] else "❌"
            print(f"\n   {status} {item['timestamp'].strftime('%H:%M')} - {item['summary']}")
            
            if item['decisions']:
                print(f"      💡 {item['decisions']}")
            
            if item['actions']:
                print(f"      ✅ {item['actions']}")
        
        # Show issues
        if result['issues']:
            print(f"\n⚠️  Issues Found:")
            for issue in result['issues']:
                print(f"   - {issue}")
        
        # Show live chat alignment if checked
        if 'live_chat_aligned' in result:
            alignment_status = "✅ ALIGNED" if result['live_chat_aligned'] else "⚠ MISALIGNED"
            print(f"\n🔗 Live Chat: {alignment_status}")
        
        # Overall status
        print(f"\n🎯 Status: {'✅ HEALTHY' if result['healthy'] else '❌ ISSUES FOUND'}")
        
        if result['healthy']:
            print("   All records are valid and timeline is continuous.")
        else:
            print("   Some issues need attention.")

if __name__ == "__main__":
    """Run standalone health check."""
    checker = ChatHealthChecker()
    result = checker.check_health()
    checker.display_results(result)