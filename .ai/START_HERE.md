# START_HERE.md

## Purpose

This is the bootloader for every AI session.

Use it for every new agent, every new chat, every time an agent seems confused, every handoff after another agent edited the project, and every final review.

## Required reading order

Read these files in order:

1. `.ai/RESEARCH_CONTEXT.md` — WHY Leap exists
2. `.ai/AI_AGENT.md` — how to behave
3. `.ai/PROJECT_CONTEXT.md` — WHAT the project does
4. `.ai/ARCHITECTURE.md` — HOW the system works
5. `.ai/BUSINESS_RULES.md` — rules not to break
6. `.ai/CURRENT_STATE.md` — current work
7. `.ai/HANDOFF.md` — previous session
8. `.ai/BUGS.md` — known risks
9. `.ai/DECISIONS.md` — decisions not to reverse
10. `.ai/CHANGELOG.md` — recent changes

## After reading

Before editing code, respond with:

1. What you understand Leap is.
2. Which subsystem is relevant to the user’s request.
3. Which files you need to inspect.
4. A safe plan.
5. Whether this is a task for Codex, Gemini, Kimi, Copilot, or manual work.

## Before ending

Update:

- `.ai/CURRENT_STATE.md`
- `.ai/HANDOFF.md`
- `.ai/CHANGELOG.md`
- `.ai/BUGS.md` if risks changed
- `.ai/DECISIONS.md` if a decision was made
- `.ai/SESSIONS/` if the session was long

## Never

- Do not invent business facts.
- Do not silently remove traceability.
- Do not break KPI behavior.
- Do not break governance.
- Do not certify AI-generated interpretation as truth.
- Do not make broad refactors during PhD-critical debugging.
