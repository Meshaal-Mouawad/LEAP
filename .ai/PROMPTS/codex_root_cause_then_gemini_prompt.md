# Codex Prompt — Root Cause then Gemini Prompt

Read `.ai/START_HERE.md`.

Analyze this problem without editing code first:

```text
[PASTE PROBLEM]
```

Return:

1. Root cause.
2. Relevant files/functions.
3. Minimal safe fix.
4. Risks.
5. Verification steps.
6. Exact Gemini CLI prompt to implement the fix.

Constraints:

- Preserve KPI behavior.
- Preserve governance behavior.
- Preserve traceability.
- Preserve deterministic output.
- Do not refactor unrelated code.
