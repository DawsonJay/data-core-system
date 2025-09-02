# Chat Report Framework v3.0 - AI-Friendly Templates

## **Purpose**
Simple templates for creating chat records immediately when you identify valuable content. Copy and paste these templates, then fill in the brackets with real information.

## **Required Fields (Copy This Exactly)**
```markdown
---
type: chat
framework: framework
id: [generate UUID]
timestamp: [current GMT time]
framework_version: 3.0
---
```

## **Content Structure (Three Simple Sections)**

### **1. Context Snapshot (Copy This Template)**
```markdown
## Context Snapshot
**Current Project:** [What project are we working on?]
**Current Status:** [What was just completed?]
**Next Steps:** [What is planned next?]
**How It's Going:** [Is it going well? Any challenges?]
**Current Focus:** [What are we discussing right now?]
```

**Fill in the brackets with actual information from the conversation.**

### **2. Valuable Insight (Copy This Template)**
```markdown
## Valuable Insight
[The specific valuable content that made you create this record. This could be:
- A design decision and why it was made
- A problem solution and how it was solved
- An interview response that showcases skills
- A learning insight or breakthrough
- A technical decision and reasoning
- Any other valuable content from the conversation]
```

**Write the actual valuable content here, not in brackets.**

### **3. Technical Specifications (Copy This Exactly)**
```markdown
## Technical Specifications
Framework v3.0 real-time capture system. AI-first design with autonomous value extraction.
```

## **Complete Example (Copy This Structure)**

```markdown
---
type: chat
framework: framework
id: 82dcd6b6-72e4-4836-ac1f-41112ca57ede
timestamp: 2025-09-02T14:30:00.000000+00:00
framework_version: 3.0
---

# Chat Session Report - 2025-09-02 14:30

## Context Snapshot
**Current Project:** Building a new real-time value capture system
**Current Status:** Just finished designing the framework structure
**Next Steps:** Need to implement the learning system
**How It's Going:** Going well, framework is clear and simple
**Current Focus:** Discussing how to make the system more AI-friendly

## Valuable Insight
The user just explained that the current documentation is too complex for new AIs. This reveals that we need to simplify the instructions and make them more prescriptive rather than descriptive.

## Technical Specifications
Framework v3.0 real-time capture system. AI-first design with autonomous value extraction.
```

## **File Naming Convention**
- **Format:** `chat-YYYY-MM-DD-HH-MM.md`
- **Example:** `chat-2025-09-02-14-30.md`
- **Location:** `chats/` folder

## **When to Create a Record**
Create a record when you see:
- **Design decisions** - User explaining why they chose certain approaches
- **Problem solutions** - User describing how they solved technical challenges
- **Learning insights** - User sharing what they discovered or learned
- **Interview responses** - User giving answers to professional questions
- **Project milestones** - User describing work completed and achievements
- **Technical decisions** - User explaining architecture and implementation choices

## **How to Use This Framework**
1. **Copy the template** from above
2. **Fill in the brackets** with real information
3. **Save the file** in the `chats/` folder
4. **Update your learning** in `chats/system/value_learning.md`

## **Start Simple**
- Don't worry about being perfect
- Just capture what feels valuable
- You'll get better with practice
- The system learns and improves over time

---

**Remember**: You're building a portfolio of valuable insights. Capture what matters, and the system will help you get better at it.
