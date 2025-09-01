# Chat Behavior Protocol - Data Core System

## 🎯 **CRITICAL: AI Must Read This Before Starting Any Chat**

This README defines the mandatory behaviors for ALL AI systems interacting with the Data Core System.

## 🚀 **Immediate Actions Required:**

### 1. **Smart Live Chat Recording Protocol**
- **START IMMEDIATELY** when chat begins
- **Record conversation in memory** during normal workflow
- **Create memory files when:**
  - 30 minutes have passed since last save
  - Major development milestone is completed
  - User requests save
- **Timer resets** after each save
- **Format:** `temp/chat_memory_batch_001.txt`, `chat_memory_batch_002.txt`, etc.
- **Streaming validation:** Each new memory file must form gapless history with previous file
- **Gapless history:** Each save captures only new messages since last save

### 2. **User Confirmation Required**
- **MUST tell user:** "I understand and will follow the live recording protocol during this chat"
- User must know the AI understands and will comply
- Creates accountability and trust

### 3. **Continuous Value Generation**
- Ask **periodic insightful questions** during development
- Focus on design decisions, technical choices, and professional insights
- Generate maximum value for portfolio building

## 📁 **Memory File Management:**

### **File Naming Convention:**
```
temp/chat_memory_batch_001.txt
temp/chat_memory_batch_002.txt
temp/chat_memory_batch_003.txt
```

### **Save Triggers:**
- **30-minute timer:** Automatically save after 30 minutes of conversation
- **Development milestones:** Save after completing significant work
- **Timer resets:** After each save, timer starts from 0
- **Gapless history:** Each save captures only new messages since last save

### **File Content Format:**
```
User: [exact message content]
Assistant: [exact response content]
```

### **Memory File Location:**
**CRITICAL:** Memory files are now stored in `chats/chat_memories/temp/` for enhanced security:
```
chats/chat_memories/temp/chat_memory_batch_001.txt
chats/chat_memories/temp/chat_memory_batch_002.txt
chats/chat_memories/temp/chat_memory_batch_003.txt
```

### **Reliable File Creation Method:**
**CRITICAL:** Use the reliable `cat` method to prevent 3-byte file creation issues:

```bash
# ✅ RELIABLE METHOD (use this):
cat > chats/chat_memories/temp/chat_memory_batch_001.txt << 'EOF'
User: [exact message content]
Assistant: [exact response content]
User: [next message content]
Assistant: [next response content]
EOF

# ❌ PROBLEMATIC METHOD (avoid this):
edit_file --target_file temp/chat_memory_batch_001.txt --code_edit "[content]"
```

**Why the `cat` method is reliable:**
- **Direct shell command** - bypasses tool issues
- **Heredoc syntax** - reliable content insertion
- **No tool dependencies** - pure bash functionality
- **Immediate verification** - can check file size right after creation

**Always verify file creation:**
```bash
wc -c chats/chat_memories/temp/chat_memory_batch_001.txt  # Should be > 100 bytes, not 3
```

### **Troubleshooting File Creation Issues:**

**If file is only 3 bytes (common problem):**
1. **Delete the corrupted file:** `rm chats/chat_memories/temp/chat_memory_batch_001.txt`
2. **Use the reliable `cat` method** shown above
3. **Verify file size immediately:** `wc -c chats/chat_memories/temp/chat_memory_batch_001.txt`
4. **File should be > 100 bytes** for a meaningful conversation

**Common causes of 3-byte files:**
- ❌ **Tool malfunctions** - `edit_file` or similar tools not working correctly
- ❌ **Content not written** - file created but content insertion failed
- ❌ **Permission issues** - file created but writing blocked
- ❌ **Tool dependencies** - relying on external tools that may fail

**The `cat` method prevents these issues** by using direct shell commands with no external dependencies.

### **Streaming Validation Requirements:**
- **Gapless History Check:** Each new memory file must connect seamlessly with previous file
- **Last Message Match:** Last message of previous file must match first message of new file
- **Speaker Continuity:** Maintain User → Assistant → User → Assistant pattern
- **Content Validation:** Verify proper User:/Assistant: format and minimum content length
- **Fail Hard:** If validation fails, do not create memory file and report error

### **Validation Process:**
**CRITICAL:** After creating each memory file, validate it using:
```bash
python3 data_core.py validate memory --file chats/chat_memories/temp/chat_memory_batch_XXX.txt
```

**Validation checks:**
- **Format compliance** - User:/Assistant: pattern validation
- **Gapless history** - connects seamlessly with previous memory
- **Content integrity** - file size and corruption checks
- **Error recovery** - comprehensive failure analysis and recovery guidance

**Validation Tools:**
- **Import validation functions:** `from scripts.utils.memory_file_validator import validate_memory_file_format, validate_gapless_history`
- **Use before creating memory files:** Validate format and gapless history
- **Fail hard on validation errors:** Do not proceed with invalid files

### **Cleanup Protocol:**
- Memory files are automatically cleaned up after successful save
- Maintains clean temp folder for next session

## 💾 **Save Process Integration:**

### **When Save is Triggered (30 min timer or milestone):**
1. **Create ONE batch memory file** containing all new messages since last save
2. **Validate gapless history** with previous memory file before proceeding
3. **Pass batch file** to save_chat.py with `--file` argument
4. **Create record** of new conversation section
5. **Reset 30-minute timer** to 0
6. **Clean up batch memory file** only after successful save and validation
7. **Continue recording** new messages in memory

## 🎯 **Expected Behaviors:**

### **AI Must:**
- ✅ Read this README before starting chat
- ✅ Confirm understanding to user
- ✅ Begin recording conversation in memory
- ✅ Monitor 30-minute timer and development milestones
- ✅ Ask periodic value-generating questions
- ✅ Create ONE batch memory file when timer expires or milestone completed
- ✅ Validate gapless history with previous memory file before proceeding
- ✅ Reset timer after each save
- ✅ Maintain gapless conversation history

### **AI Must NOT:**
- ❌ Start chat without reading this README
- ❌ Skip user confirmation
- ❌ Miss any messages in recording
- ❌ Fail to ask value-generating questions

## 🔄 **Workflow Example:**

```
1. AI starts chat
2. AI reads this README
3. AI: "I understand and will follow the live recording protocol during this chat"
4. AI begins recording conversation in memory
5. AI monitors 30-minute timer and development milestones
6. When timer expires or milestone completed:
   - AI creates ONE batch memory file for new messages since last save
   - AI saves conversation history
   - Timer resets to 0
7. AI continues recording in memory
8. Process repeats for gapless history
```

## ⚠️ **Failure Consequences:**

- **Missing messages** = Information loss
- **No user confirmation** = Lack of accountability
- **Incomplete recording** = Failed portfolio building
- **System designed to fail hard** on critical issues

## 🎯 **Success Metrics:**

- ✅ **Zero information loss** - every message preserved
- ✅ **Complete development journey** captured
- ✅ **Maximum value extraction** for portfolio
- ✅ **User confidence** in system reliability

---

**Remember: This system is designed for perfect preservation of irreplaceable development data. Every message matters. Every design decision is valuable. Follow this protocol without exception.**
