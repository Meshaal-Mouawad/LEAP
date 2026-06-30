# Leap AI Memory Folder

This `.ai` folder is the shared memory layer for all AI assistants working on Leap.

## Core principle

Chat is temporary.  
`.ai` is memory.  
Git is history.  
Source code is truth.

## Memory layers

| File | Role |
|---|---|
| `RESEARCH_CONTEXT.md` | WHY Leap exists |
| `PROJECT_CONTEXT.md` | WHAT the project does, to be filled by Gemini after repo analysis |
| `ARCHITECTURE.md` | HOW the system works |
| `START_HERE.md` | Entry point for every AI session |
| `AI_AGENT.md` | Behavior rules for all agents |
| `CURRENT_STATE.md` | Current work and blockers |
| `HANDOFF.md` | Last session summary |
| `DECISIONS.md` | Architectural/product decisions |
| `CHANGELOG.md` | AI-assisted change history |
| `BUGS.md` | Known bugs and risks |
| `ROADMAP.md` | PhD, enterprise, and future agentic roadmap |
| `USAGE_GUIDE.md` | How Meshaal uses the AI team |
| `PROMPTS/` | Reusable prompts |
| `SESSIONS/` | Compressed summaries of long sessions |

## Daily rule

Every AI starts with:

```text
Read `.ai/START_HERE.md` first.
```

Every AI ends with:

```text
Update `.ai/CURRENT_STATE.md`, `.ai/HANDOFF.md`, `.ai/CHANGELOG.md`, and any relevant memory file before ending.
```
