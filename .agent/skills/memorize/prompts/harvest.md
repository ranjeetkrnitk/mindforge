# harvest

> Retrospective session capture — batch `capture` over a conversation.

## Steps

1. **Load session**: use current conversation context, or query session store by ID, or ask user to paste text.

2. **Segment** into topic spans. Boundary signals:
   - new unrelated question or task
   - domain shift (REF.md domains)
   - resolution phrase ("ok got it", "let's move on", "next")
   - several turns with no connection to prior context
   Discard spans shorter than `harvest_min_turns` unless they contain a standalone claim.

3. **Merge adjacent spans** with keyword overlap ≥ `harvest_merge_threshold`.

4. **Classify each span** (REF.md node types):
   - task / debug / workflow / personal → `episode`
   - sourced verifiable assertion → `claim`
   - formed insight / mental model → `concept`
   - unresolved question → `question`
   Default: `episode`.

5. **Pattern-match** against existing notes (same as `capture` step 3):
   - match → link via `recalls`; skip creating duplicate note
   - no match → new note

6. **Write files** to vault and print one line per file:
```
✓ episodes/YYYY/MM/YYYY-MM-DD -- <title>.md  [turns N-M, episode]
✓ concepts/domain/Claim title.md              [turns N-M, concept]
```

7. **Harvest summary** (one block, no note content):
```
Harvested: X notes (A episodes, B claims, C concepts, D questions)
Skipped: Y spans  |  Merged: Z  |  Linked: [[Note1]], [[Note2]]
Saved to: <vault_root>
Next: "Run consolidate" if ≥3 overlapping episodes created
```

## Rules
- No modifications to existing notes
- Skip purely procedural exchanges (reformatting, "run this command") — knowledge value only
- Safe to run twice — dedup prevents duplicate notes

## Post-Action
After writing notes, run dashboard update (see `prompts/dashboard-update.md`).
