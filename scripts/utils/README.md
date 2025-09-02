# Utilities

## System Context
**This folder is part of the Data Core System.** 
For full system context, rules, and philosophy, see: `../../README.md`

**Core System Principles:**
- Data Immutability: Once saved, never modified/deleted
- Zero Information Loss: Every piece preserved forever  
- File Protection: Files cannot be modified/deleted once created
- GMT Timezone Only: All timestamps in GMT/UTC

## Status: UNFIXED
*This folder is still in development and can be modified. AI systems can create, modify, and delete files here. Once finalized, status will be changed to FIXED.*

**Status Meanings:**
- **UNFIXED:** AI systems can create, modify, and delete files freely
- **FIXED:** AI systems can create new files, but cannot modify or delete existing files

## Purpose
**Provides utility modules and helper functions that support Data Core System processes.** These utilities are not standalone processes but supporting infrastructure that enables the main system to function reliably and efficiently. They provide validation, helper functions, and common utilities that multiple processes can use.

## Framework: Utility Module Framework
- **Type:** utility
- **Purpose:** Supporting infrastructure for Data Core processes
- **Integration:** Imported and used by other processes
- **Standalone:** Not user-facing, not callable through master script
- **Validation:** Provides validation and helper functions for data integrity

## File Rules
- **Utility Modules Only:** Only utility modules and helper functions allowed
- **No Standalone Processes:** Must not be executable processes
- **Importable:** Must be designed for import by other processes
- **Validation Focus:** Primary purpose is data validation and integrity checking
- **Helper Functions:** Provide common functionality used across multiple processes

## File Restrictions
- **ONLY utility modules** are allowed in this folder
- **NO standalone processes** may be created here
- **NO user-facing scripts** that can be called directly
- **ONLY importable modules** that support other processes
- **File naming must follow:** descriptive names ending in `.py`

## AI System Rules
- **Status: UNFIXED** - AI systems can create, modify, and delete files
- **Utility Creation Required** - AI must create proper utility modules, not standalone processes
- **Framework Compliance** - All utilities must follow the Utility Module Framework
- **Importable Design** - Utilities must be designed for import by other processes
- **Validation Functions** - Focus on data validation and integrity checking
- **Helper Functions** - Provide common functionality used across processes
- **No Main Functions** - Utilities should not have executable main sections
- **Documentation Required** - Clear docstrings and usage examples for all functions

## Utility Modules

### `memory_file_validator.py`
**Memory file validation utilities for the live chat recording system.**

**Functions:**
- `validate_memory_file_format(content)` - Check format compliance (User:/Assistant: structure)
- `validate_gapless_history(new_file, previous_file)` - Ensure continuity between chat records (deprecated - replaced by Natural Value Extraction)
- `validate_memory_file_creation(file_path, content)` - Verify file creation success
- `get_last_message(content)` - Extract last message for continuity checking
- `get_first_message(content)` - Extract first message for continuity checking

**Usage:**
```python
from scripts.utils.memory_file_validator import validate_memory_file_format, validate_gapless_history

# Validate format
is_valid, message = validate_memory_file_format(content)

# Check gapless history
is_continuous, message = validate_gapless_history("temp/chat_memory_batch_002.txt", "temp/chat_memory_batch_001.txt")
```

### `check_mutability.py`
**Utility for checking file mutability and protection status.**

## Related Systems
- **Master System:** `../../README.md` - Full system rules and philosophy
- **Process System:** `../../processes/README.md` - How operations are performed
- **Chat System:** `../../chats/README.md` - Chat reports and memory file framework
- **Other Data Types:** See master README for planned systems

## Usage
- **Processes import utilities** to use validation and helper functions
- **Utilities provide common functionality** used across multiple processes
- **Validation functions ensure** data integrity and framework compliance
- **Helper functions reduce** code duplication between processes
- **Utilities support** the main Data Core System processes
- **Import structure:** `from scripts.utils.module_name import function_name`

## Organization
- **Descriptive filenames** for easy identification of utility purpose
- **Importable modules** designed for use by other processes
- **Validation focus** on data integrity and framework compliance
- **Helper functions** for common operations across processes
- **Supporting infrastructure** that enables main system functionality

## Additional Notes
This system provides reliable, reusable utilities that support the Data Core System's core functionality. Utilities are designed to be imported and used by processes, not executed directly. They focus on validation, helper functions, and common operations that multiple processes need.

**Utility Module Framework Features:**
- **Importable Design** - All utilities designed for import by other processes
- **Validation Functions** - Data integrity and framework compliance checking
- **Helper Functions** - Common operations used across multiple processes
- **No Standalone Execution** - Utilities are supporting infrastructure, not user-facing
- **Clear Documentation** - Comprehensive docstrings and usage examples
- **Framework Compliance** - All utilities follow established patterns and standards

**Integration Capabilities:**
- **Process Support** - Utilities enable processes to function reliably
- **Validation Support** - Ensure data integrity across all operations
- **Helper Support** - Reduce code duplication and improve maintainability
- **Framework Support** - Maintain consistency across all system components
