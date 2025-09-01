# Chat Memory Creation Procedure

## 🚨 MANDATORY: Follow Every Step Exactly

This procedure MUST be followed precisely when creating any chat memory file. Deviation from these steps will result in system failure.

## Prerequisites
- **30-minute timer expired** OR **development milestone completed**
- **Live chat transcript** available in memory
- **Previous chat memory** (if not first memory)

## Step-by-Step Procedure

### Step 1: Locate Previous Memory
- **Search for previous memory files** in `chats/chat_memories/temp/`
- **Identify most recent** by batch number (highest number)
- **Note the last line** of the most recent memory file
- **If no previous memory exists**, skip to Step 3

### Step 2: Extract New Content
- **Compare live transcript** to previous memory
- **Identify lines after** the last line of previous memory
- **Extract only new content** since last save
- **Verify content exists** - must have meaningful conversation

### Step 3: Determine File Name
- **If no previous memory**: `chats/chat_memories/temp/chat_memory_batch_001.txt`
- **If previous memory exists**: increment batch number
- **Format**: `chats/chat_memories/temp/chat_memory_batch_XXX.txt` (3-digit zero-padded)

### Step 4: Create Memory File
- **Use the reliable `cat` method**:
```bash
cat > chats/chat_memories/temp/chat_memory_batch_XXX.txt << 'EOF'
[extracted new content in User:/Assistant: format]
EOF
```

### Step 5: Verify File Creation (3 Attempts)
**Attempt 1:**
- Check file exists: `ls chats/chat_memories/temp/chat_memory_batch_XXX.txt`
- Check file has content: `wc -c chats/chat_memories/temp/chat_memory_batch_XXX.txt`
- If file size < 100 bytes, proceed to Attempt 2

**Attempt 2:**
- Delete failed file: `rm chats/chat_memories/temp/chat_memory_batch_XXX.txt`
- Recreate using `cat` method
- Verify file exists and has content
- If still fails, proceed to Attempt 3

**Attempt 3:**
- Delete failed file: `rm chats/chat_memories/temp/chat_memory_batch_XXX.txt`
- Final attempt using `cat` method
- If still fails, **IMMEDIATELY ERROR** - system failure

### Step 6: Validate Gapless History
- **If previous memory exists**:
  - **Call validation process**: `python3 processes/chats/validate_memory.py chats/chat_memories/temp/chat_memory_batch_XXX.txt`
  - **Verify gapless connection** with previous memory
  - **Verify content matches** live transcript exactly
- **If validation fails**: **IMMEDIATELY ERROR** - serious failure

### Step 7: Success Confirmation
- **Display message**: "Chat memory saved successfully"
- **Reset 30-minute timer** to 0
- **Continue recording** new conversation in memory

## Error Handling

### Critical Failures (Immediate Error)
- **File creation fails after 3 attempts**
- **Validation fails** (gapless history or content mismatch)
- **File corruption detected**
- **Framework validation fails** (content insufficient for requirements)
- **Save process fails** after memory cleanup

### Error Response
- **Stop all operations immediately**
- **Display comprehensive error analysis** with root cause identification
- **Provide specific recovery steps** for immediate problem resolution
- **Suggest system strengthening measures** to prevent future failures
- **Request user intervention** with detailed problem description
- **Do not proceed** until error is resolved and system is strengthened

### Error Recovery Protocol
When any error occurs:

1. **Immediate Problem Analysis**
   - Identify the specific failure point
   - Determine if data loss has occurred
   - Assess system integrity status

2. **Recovery Action Plan**
   - Provide step-by-step recovery instructions
   - Identify any data that needs to be restored
   - Specify validation steps to confirm recovery

3. **System Strengthening Recommendations**
   - Identify the root cause of the failure
   - Suggest process improvements to prevent recurrence
   - Recommend additional validation or safety measures
   - Propose system architecture enhancements

4. **Prevention Measures**
   - Document the failure scenario for future reference
   - Update procedures to include additional safety checks
   - Implement additional validation layers if needed

## Success Criteria
- ✅ **File created successfully** with proper content
- ✅ **Format validation passed** (User:/Assistant: pattern)
- ✅ **Gapless history verified** (connects with previous memory)
- ✅ **Content integrity confirmed** (matches live transcript)
- ✅ **File size adequate** (>100 bytes)

## Save Process Integration
- **Automatic backup creation** - save process creates compressed backups before cleanup
- **Backup verification** - cleanup only proceeds after successful backup creation
- **Data safety guarantee** - no memory files deleted without verified backup
- **Recovery capability** - backups can restore memories if save process fails

## Notes
- **This procedure is non-negotiable** - follow exactly
- **Validation is critical** - never skip validation steps
- **Error handling is mandatory** - system must fail safely
- **Success is quiet** - only show success message, no commands
- **Failure is loud** - errors must be immediately visible
