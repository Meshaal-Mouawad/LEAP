# USAGE_GUIDE.md

## The simple plan

Use this stack:

```text
ChatGPT Plus → architecture and planning
Codex → hard bugs and final review
Gemini CLI → main implementation and repo analysis
GitHub Copilot → autocomplete and small inline help
Kimi → second-opinion review
Air → local workspace for supported providers
Qwen → future optional tool
```

## Start any AI

```text
Read `.ai/START_HERE.md` first.
```

## First Gemini bootstrap

Use this once after installing/updating `.ai`:

```text
Read `.ai/PROMPTS/gemini_bootstrap_project_memory.md` and execute it.
```

Gemini must inspect the local repo and update `.ai` files only.

## Hard bug workflow

### 1. Codex diagnosis

```text
Read `.ai/START_HERE.md`.

Analyze this problem but do not edit code yet:

[PASTE PROBLEM]

Return:
1. root cause,
2. relevant files,
3. safest plan,
4. exact Gemini implementation prompt.
```

### 2. Gemini implementation

```text
Read `.ai/START_HERE.md`.

Implement this Codex plan:

[PASTE CODEX PLAN]

Make the smallest safe change and update `.ai` memory before ending.
```

### 3. Kimi review

```text
Read `.ai/START_HERE.md`.

Review the recent changes in `.ai/HANDOFF.md`, `.ai/CHANGELOG.md`, and `git diff`.

Focus on correctness, edge cases, missing tests, and enterprise risks.
```

### 4. Codex final review

```text
Read `.ai/START_HERE.md`.

Final-review the implementation for KPI behavior, governance, traceability, Blue Book output, and PhD demo risk.
```

## When an agent hallucinates

Say:

```text
Stop. Re-read `.ai/START_HERE.md`, then verify your claims from source files before continuing.
```

## When the chat gets too long

```text
Compress this session into `.ai/SESSIONS/YYYY-MM-DD-topic.md`.

Keep only:
- problem,
- root cause,
- files changed,
- final solution,
- verification,
- remaining risks,
- next step.

Then update `.ai/HANDOFF.md`.
```
