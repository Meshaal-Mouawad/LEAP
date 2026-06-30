# DECISIONS.md

## 2026-06-30 — Use `.ai` as shared memory

**Decision:** Use repository-local `.ai` files as the shared memory layer for all agents.

**Why:** Deterministic, auditable, Git-versioned, and aligned with Leap's philosophy.

---

## 2026-06-30 — Separate WHY / WHAT / HOW

**Decision:** Split project memory into:

```text
RESEARCH_CONTEXT.md → WHY
PROJECT_CONTEXT.md  → WHAT
ARCHITECTURE.md     → HOW
```

**Why:** AI agents often confuse motivation, functionality, and implementation.

---

## 2026-06-30 — Codex as expert, Gemini as worker

**Decision:** Use Codex mainly for hard diagnosis and final review; use Gemini CLI for implementation.

**Why:** Codex is strong but limited/costly. Gemini CLI is useful for large routine work.

---

## 2026-06-30 — Keep workflow simple before PhD completion

**Decision:** Do not add Mem0, Cognee, AgentMemory, OpenCode, Aider, or complex orchestration now.

**Why:** PhD-critical work needs stability. More tools can create coordination overhead.

---

## 2026-06-30 — Register Qwen for future optional use

**Decision:** Qwen is available as a future optional coding agent, but not part of the daily workflow yet.

**Why:** It may help later for implementation/refactoring, but current stack is enough.
