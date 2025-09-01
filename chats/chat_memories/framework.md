# Chat Memory Framework

## Purpose
**Standardized format for chat memory files that can be processed by the save chat system.** Each memory file captures a segment of live conversation in a format that ensures gapless history and proper processing by the save system.

## Required Format
```
User: [exact message content]
Assistant: [exact response content]
User: [next message content]
Assistant: [next response content]
```

## Format Rules
1. **Must start with User:** (not Assistant:)
2. **Must alternate** User: → Assistant: → User: → Assistant:
3. **Must end with Assistant:** (for proper conversation flow)
4. **No consecutive messages** from same speaker
5. **Minimum 2 messages** (one complete pair)
6. **Proper spacing** after colons
7. **Exact content preservation** - no paraphrasing or summarization

## File Naming Convention
```
chats/chat_memories/temp/chat_memory_batch_001.txt
chats/chat_memories/temp/chat_memory_batch_002.txt
chats/chat_memories/temp/chat_memory_batch_003.txt
```

## Validation Requirements
- **Format compliance** - follows User:/Assistant: pattern
- **Gapless history** - connects seamlessly with previous memory
- **Content integrity** - matches live transcript exactly
- **File existence** - file created successfully with content
- **Minimum size** - file contains meaningful conversation

## Integration with Save Process
- **Direct compatibility** - save process can process without reformatting
- **Batch processing** - multiple memories combined for complete history
- **Automatic backup** - memories backed up before cleanup (prevents data loss)
- **Automatic cleanup** - memories deleted after successful save and backup verification
- **Error handling** - validation failures prevent save process corruption

## Quality Standards
- **Zero information loss** - every message preserved exactly
- **Perfect continuity** - no gaps between memory files
- **Real-time accuracy** - matches live conversation verbatim
- **System reliability** - validation prevents save process failures
- **Data safety** - automatic backups before any destructive operations
- **Error recovery** - comprehensive error analysis and recovery guidance
