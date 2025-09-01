# AI AGENT MEMORY - CRITICAL BEHAVIORS

## 🚨 IMMEDIATE COMPLIANCE REQUIRED

When working with this Data Core System, AI agents MUST follow these behaviors:

### Chat Protocol (MANDATORY)
- **Read `processes/chats/README.md` BEFORE starting any chat**
- **Confirm understanding to user:** "I understand and will follow the live recording protocol during this chat"
- **Begin recording conversation in memory** during normal workflow
- **Monitor 30-minute timer** and development milestones
- **Create chat memories** when timer expires or milestone completed (whichever comes first)
- **Follow strict procedure** in `chats/chat_memories/procedure.md` for memory creation
- **Use validation process** `python data_core.py validate memory --file <path>` after creation
- **Ask periodic value-generating questions** about design decisions, technical choices, and professional insights
- **Reset 30-minute timer** after each memory creation

### Data Protection (MANDATORY)
- **Never modify or delete existing files** - data immutability is absolute
- **Always backup before any Git operations** - mandatory pre-commit backup
- **Use GMT timezone only** for all timestamps (avoid regional/VPN issues)
- **Follow the immutable data principles** - zero information loss
- **Protect irreplaceable data** - data safety is paramount

### System Philosophy (MANDATORY)
- **Capture everything** - don't filter for perceived value
- **Record raw information** without premature analysis
- **Let future analysis determine what's valuable** - don't make assumptions
- **Focus on data preservation, not interpretation** - protect data, don't analyze it
- **Build incrementally** - only add what's actually needed

### File Creation Standards (MANDATORY)
- **Use descriptive, searchable names** - ensure data discoverability
- **Timestamp everything** - maintain chronological accuracy
- **Follow established frameworks** - ensure data follows established patterns
- **Validate results** - check that operations completed successfully

### Chat Memory System (MANDATORY)
- **Read `chats/chat_memories/framework.md`** for format requirements
- **Follow `chats/chat_memories/procedure.md`** exactly for memory creation
- **Use validation process** after each memory creation
- **Store memories in `chats/chat_memories/temp/`** folder (secure isolated storage)
- **Maintain gapless history** between all memory files

---

**Remember: This system is designed for perfect preservation of irreplaceable development data. Every message matters. Every design decision is valuable. Follow this protocol without exception.**

**Failure to follow these behaviors will result in information loss and system failure.**
