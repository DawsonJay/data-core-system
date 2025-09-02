# AI Agent Memory & Behavior Instructions

## **CRITICAL: This file MUST be read and applied immediately when referenced**

When you are told to "apply the memory file" or similar, you MUST:
1. **Read this file completely**
2. **Implement ALL behaviors listed below**
3. **Start maintaining the value log immediately**
4. **Follow the exact sequence specified**

## **Behavior Implementation (MANDATORY)**

### **Step 1: Immediate System Understanding**
- Read `README.md` to understand the Data Core System
- Read `reference/value_definitions.md` to understand what constitutes value
- Read `reference/value_patterns.md` to understand how to identify value
- Read `processes/chats/README.md` to understand the Natural Value Extraction System

### **Step 2: Continuous Value Logging (START IMMEDIATELY)**
**You MUST write to `conversation_memory.md` throughout the entire conversation:**

- **Real-time insight capture**: Write valuable insights AS THEY OCCUR, not at the end
- **Technical discoveries**: Code patterns, bug root causes, architectural insights
- **Process improvements**: Better ways of doing things, workflow optimizations
- **Knowledge gaps**: What you don't know, what needs research
- **User preferences**: How the user likes to work, their priorities
- **System flaws**: Problems you identify in tools, processes, or documentation

**Format for each insight:**
```markdown
### [Date] - [Topic] - [Insight Type]
- **Insight**: [Specific technical or process insight]
- **Context**: [Why this matters, what it affects]
- **Value**: [How this improves future work]
```

### **Step 3: Pre-Save Value Update (CRITICAL)**
**BEFORE triggering any chat save:**
1. **Review the entire conversation** for any missed insights
2. **Update `conversation_memory.md`** with final insights and current status
3. **Ensure all valuable content is captured** before save
4. **Only then trigger the save process**

### **Step 4: Self-Improvement of Value Reference Files**
**After each chat save, improve the value reference files:**

- **Update `reference/value_definitions.md`** with new value categories discovered
- **Update `reference/value_patterns.md`** with better identification patterns
- **Add examples** of what the user found valuable in this conversation
- **Refine the guidance** based on what worked and what didn't
- **Make the system smarter** at recognizing value for future conversations

### **Step 5: Value Log Maintenance**
**Keep the value log organized and focused:**
- **Remove completed insights** after they're successfully implemented
- **Archive resolved issues** to prevent duplication
- **Maintain context** for ongoing work
- **Highlight unresolved items** that need attention

## **What Constitutes Value (Examples)**

### **Technical Value**
- Bug root causes and solutions
- Code architecture patterns
- Performance optimizations
- Security vulnerabilities
- Integration challenges and solutions

### **Process Value**
- Workflow improvements
- Tool limitations and workarounds
- Communication patterns that work
- Time-saving techniques
- Quality assurance methods

### **Knowledge Value**
- Domain-specific insights
- Technology stack understanding
- User preferences and priorities
- System limitations and capabilities
- Best practices discovered

## **Implementation Checklist**

When implementing these behaviors, verify you have:

- [ ] Read all reference files
- [ ] Started continuous value logging
- [ ] Captured all insights in real-time
- [ ] Updated value log before save
- [ ] Improved value reference files
- [ ] Maintained organized value log

## **Failure Modes to Avoid**

- **Delayed logging**: Waiting until the end to capture insights
- **Incomplete capture**: Missing valuable content during conversation
- **Static reference files**: Not improving the system based on experience
- **Manual intervention**: Requiring user to request saves instead of autonomous operation
- **Context loss**: Not maintaining continuity between conversations

## **Success Indicators**

- User never needs to ask you to save the chat
- Value reference files continuously improve
- Insights are captured in real-time without disruption
- System becomes more intelligent at recognizing value
- Chat records are comprehensive and up-to-date

---

**Remember**: This system is designed to be autonomous and self-improving. Your role is to continuously identify, capture, and preserve value while making the system better at doing so.
