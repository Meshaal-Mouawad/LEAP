# End Session — Update Memory

Before ending this session, update the shared memory.

## Update required files

- `.ai/CURRENT_STATE.md`
- `.ai/HANDOFF.md`
- `.ai/CHANGELOG.md`
- `.ai/BUGS.md` if needed
- `.ai/DECISIONS.md` if a decision was made
- `.ai/SESSIONS/YYYY-MM-DD-topic.md` if this was a long session

## Required final report

Before finishing, show:

1. Which `.ai` files you modified.
2. The relevant `git diff .ai` summary.
3. Why each update was made.
4. Verification results.
5. If no `.ai` file was modified, explicitly state:  
   “Shared memory was NOT updated.”

## Memory quality rules

Keep only durable facts.

Remove:

- failed attempts unless useful,
- duplicate explanations,
- speculation,
- emotional chat text.

Do not invent completed work.