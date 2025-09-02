# Data Core Processes

## System Context
**This folder is part of the Data Core System.** 
For full system context, rules, and philosophy, see: `../README.md`

**Core System Principles:**
- Data Immutability: Once saved, never modified/deleted
- Zero Information Loss: Every piece preserved forever  
- Mandatory Backup Before Commit: All Git commits MUST be preceded by comprehensive backups
- Data Protection First: Always backup before any changes or commits
- Multiple Backup Strategies: Redundancy at every level

## Purpose & Philosophy

**Processes ARE the rules - executable enforcement instead of documentation hoping.**

### The Core Problem We Solve
Traditional approach: Put rules in README, hope AI reads and follows them.
**Result:** AI ignores, forgets, or misinterprets rules. Rules get violated, data gets corrupted.

### Our Solution
**Processes ARE the rules** - not documentation of rules.
- When AI is asked to do data core tasks, it finds and runs processes
- **Rules are enforced automatically** by the process scripts  
- **No relying on AI memory** or rule interpretation
- **The AI can't accidentally break rules because the processes ARE the rules**

## AI-First Design Requirements

### Critical Requirements for ALL Processes

**1. NO Interactive Elements**
- ❌ NEVER use `input()` calls
- ❌ NEVER wait for user confirmation  
- ❌ NEVER require manual intervention during execution
- ✅ AI must be able to run process completely autonomously

**2. AUTO-EXTRACT Context**
- ✅ Automatically extract live conversation context when needed
- ✅ Process should determine what data it needs and get it
- ❌ NEVER require AI to manually provide conversation context
- **Example:** When AI asked "save this chat", process auto-extracts current conversation

**3. VERBOSE Progress Reporting**
- ✅ Show step-by-step progress with clear status indicators
- ✅ Use ✓ for success, ✗ for errors, ⚠ for warnings
- ✅ Provide comprehensive final reports
- ✅ Include health checks and validation results
- **Purpose:** User can see exactly what happened and verify results

**4. FAIL HARD with Clear Messages**
- ✅ Stop immediately when critical issues occur  
- ✅ Provide specific error messages with context
- ✅ Explain what went wrong and what needs to be fixed
- ❌ NEVER continue with degraded functionality
- **Philosophy:** Better to fail clearly than succeed with data corruption

**5. DUAL-TIME Display Standards**
- ✅ Store ALL data timestamps in GMT/UTC (immutable data requirement)
- ✅ Display ALL user-facing times in local timezone with GMT reference
- ✅ Use clear format: "20:09 (GMT: 19:09)" or "20:35:57 (local) / 19:35:57 GMT"
- ✅ Prioritize user experience while maintaining data consistency

## Process Patterns & Examples

### Established Process Patterns

**1. Chat Operations (Real-Time Value Capture)**
```
Pattern: AI automatically identifies valuable content → creates chat records immediately → maintains gapless history
✓ Real-time value capture using Framework v3.0
✓ No save process needed - immediate creation of chat records
✓ Maintains complete conversation coverage through validation
✓ Learning system continuously improves capture quality
✓ **Fully autonomous** - AI operates independently during conversation
```

**2. Git Operations (`git_commit.py`)**
```  
Pattern: AI asked "commit work" → finds process → saves chat first → creates backups → commits safely
✓ Chat-first workflow (zero-gap principle)
✓ Three-tier backup system (major/standard/minor)
✓ Mandatory backup before commit
✓ Auto-generates commit messages
```

**3. Health Check Operations (`chats/chat_health_check.py`)**
```
Pattern: AI asked "run health check" → finds process → validates system → reports with dual-time display
✓ Comprehensive file analysis and timeline validation
✓ Local time display: "20:09 (GMT: 19:09)" for user readability
✓ GMT data preservation: All stored timestamps remain GMT
✓ User-friendly feedback while maintaining data integrity
```

### Process Structure Standard
```python
#!/usr/bin/env python3
"""
Process Name - PURPOSE STATEMENT
Brief description of what this process does and why.
Follows Data Core System principles: [relevant principles].
"""

def main():
    print("=" * 70)
    print("PROCESS NAME - PURPOSE")
    print("=" * 70)
    print("Brief description of what will happen.")
    
    # Step-by-step execution with verbose reporting
    # Each step shows progress and validates success
    
    print("\n" + "=" * 70)
    print("SUCCESS: OPERATION COMPLETED")
    print("=" * 70)
    # Comprehensive final report
```

## Integration with Master Script

### Standard Integration Pattern

**All processes should be callable through `data_core.py`:**

```python
# In data_core.py
def process_name():
    """Brief description of what this does."""
    print("=" * 60)
    print("DATA CORE - PROCESS NAME")
    print("=" * 60)
    
    script_path = os.path.join("processes", "process_name.py")
    if os.path.exists(script_path):
        try:
            result = subprocess.run([sys.executable, script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Process failed: {e}")
    else:
        print(f"Error: Process script not found at {script_path}")
```

### AI Discovery Pattern
```
User asks AI to do something → AI finds appropriate process → AI runs process → Reports results
```

**Examples:**
- "Commit work" → AI finds `git_commit.py` → Backup-first workflow → Commits & reports  
- "Check chat health" → AI finds `chats/chat_health_check.py` → Validates system → Reports timeline
- "Capture value" → AI automatically creates chat records using Framework v3.0

## Technical Standards

### File Organization
```
processes/
├── README.md (this file)
├── process_name.py (individual process scripts)  
├── chats/ (chat-specific processes)
│   └── chat_health_check.py
└── [other_data_types]/ (future data type processes)
```

### Code Quality Standards
- **Python 3**: All processes must be Python 3 compatible
- **Executable**: Include `#!/usr/bin/env python3` shebang
- **Error Handling**: Comprehensive exception handling with clear messages
- **Documentation**: Clear docstrings explaining purpose and workflow
- **Verbose Output**: Step-by-step progress reporting throughout execution

### Data Safety Standards
- **Backup First**: Any destructive operations must backup first
- **Validate Before Saving**: All data must be validated before writing
- **Integrity Checks**: Verify saved data matches intended content
- **Health Monitoring**: Include health checks relevant to the operation
- **Gap Detection**: Ensure no information loss between operations

### User Interface Standards
- **GMT Data Storage**: ALL timestamps in stored data MUST use GMT/UTC timezone (immutable requirement)
- **Local Time Display**: ALL user-facing time displays MUST show local time with GMT reference for readability
- **Dual-Time Format**: Use format like "20:09 (GMT: 19:09)" or "20:35:57 (local) / 19:35:57 GMT" 
- **User Experience Priority**: Make feedback natural and readable while preserving data consistency

## Rule Enforcement Philosophy

### Core Principle
**Rules must be built into the processes, not documented for AI to remember.**

### Implementation Strategy
- **Automatic Enforcement**: Rules are code, not suggestions
- **Fail-Safe Design**: System fails safely when rules would be violated  
- **No Bypasses**: Processes provide the ONLY way to perform operations
- **Comprehensive Validation**: Every aspect of data integrity is checked automatically

### Examples of Rule Enforcement
- **Framework Compliance**: AI automatically enforces Framework v3.0 through real-time capture
- **Smart Deduplication**: save_chat.py enforces content-aware duplication prevention
- **Backup Requirements**: git_commit.py MUST create backups before commits
- **Content Validation**: All processes validate data quality before saving
- **Zero Information Loss**: Gap detection prevents missing data

## Process Creation Guidelines

When creating new processes:

1. **Read this entire document** to understand requirements
2. **Study existing processes** for patterns and standards  
3. **Design for AI-first use** - no interactive elements
4. **Build in comprehensive validation** and error handling
5. **Provide verbose progress reporting** throughout execution
6. **Test thoroughly** to ensure AI can run autonomously
7. **Integrate with master script** following established patterns

## Current Process Status

### Implemented & Ready
- **Real-Time Value Capture**: AI automatically creates chat records using Framework v3.0
- **Git Commit Process**: `git_commit.py` - Backup-first commit with three-tier protection  
- **Chat Health Check**: `chats/chat_health_check.py` - Timeline and validation reporting

### Process Standards
- **AI-First Design**: All processes designed for autonomous AI operation
- **Rule Enforcement**: Processes ARE the rules, not documentation of rules
- **Comprehensive Reporting**: Verbose output with health checks and validation
- **Data Protection**: Multiple backup strategies and integrity verification built-in
- **Zero Information Loss**: Gap detection and continuous validation throughout

## Integration Notes

- **Master Script**: All processes accessible through `python data_core.py [action]`
- **AI Discovery**: Processes designed to be naturally found when AI asked to perform tasks
- **Autonomous Operation**: No manual intervention required during process execution  
- **Comprehensive Reporting**: All processes provide detailed results and health information
- **Rule Compliance**: Automatic enforcement of all Data Core System principles

**Remember: Every process is a guardian of data integrity, designed to make rule violations impossible rather than unlikely.**