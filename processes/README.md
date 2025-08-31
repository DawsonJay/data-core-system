# Data Core Processes

## Purpose
This folder contains all process scripts that enforce rules and frameworks when interacting with the data-core system. Processes ensure data integrity and rule compliance.

## Process Rules & Standards

### 1. Verbose Output Requirement
- **All processes must be verbose** - show every step clearly
- **Step-by-step logging** - each action should be logged with status
- **Success/failure indicators** - use ✓ for success, ✗ for errors
- **Clear section headers** - separate major process phases
- **Progress tracking** - show what step is currently executing

### 2. Process Structure Pattern
```
==================================================
PROCESS NAME - BRIEF DESCRIPTION
==================================================
Checking environment...
✓ Environment validated

Starting main process...

==================================================
MAIN PROCESS PHASE
==================================================
Step 1: Description...
✓ Step completed
Step 2: Description...
✓ Step completed

==================================================
SUCCESS/FAILURE MESSAGE
==================================================
```

### 3. Error Handling
- **Clear error messages** - explain what went wrong
- **Helpful guidance** - suggest how to fix the issue
- **Graceful failure** - don't crash the system
- **Error logging** - capture all error details

### 4. Framework Enforcement
- **Validate all inputs** - check data before processing
- **Enforce naming conventions** - ensure proper file naming
- **Verify framework compliance** - check required sections/fields
- **Maintain data integrity** - prevent corruption or loss

### 5. Time & Validation
- **Always verify GMT time** - use current GMT time for timestamps
- **Validate file paths** - ensure directories exist before writing
- **Check file permissions** - verify write access before saving
- **Sequence management** - handle sequential numbering correctly

## Current Processes

### Chat Operations
- **`chats/save_chat.py`** - Creates new chat reports following Chat Report Framework
  - Enforces all required sections
  - Uses correct GMT timestamps
  - Manages sequential numbering
  - Validates framework compliance

## Process Development Guidelines

### Adding New Processes
1. **Follow the verbose pattern** - use the established output format
2. **Enforce relevant frameworks** - check all required fields/sections
3. **Validate all inputs** - prevent invalid data from being saved
4. **Handle errors gracefully** - provide clear error messages
5. **Test thoroughly** - ensure process works correctly before use

### Process Naming
- **Descriptive names** - `save_chat.py`, `create_project.py`
- **Clear purpose** - immediately obvious what the process does
- **Consistent format** - lowercase with underscores

### Process Organization
- **Group by data type** - `chats/`, `projects/`, `personal/`
- **Keep processes focused** - one process per operation
- **Maintain clear hierarchy** - easy to find specific processes

## Integration with Master Script
- **Master script calls processes** - `data_core.py` coordinates operations
- **Processes handle details** - each process manages its specific domain
- **Unified interface** - all operations go through `data_core.py`
- **Consistent experience** - same pattern for all data types

## Status
- **Chat processes:** Implemented and tested
- **Project processes:** To be implemented
- **Personal processes:** To be implemented
- **System processes:** To be implemented
