# capture

> Fast hippocampal intake with optional emotion tagging.

## Steps

1. **Extract** atomic core claim. Strip filler.
2. **Classify** node type (REF.md): experience→episode, assertion→claim, insight→concept
3. **Detect emotion** (if present in input):
   - Arousal: high (excited, anxious, angry) | medium | low (calm, tired)
   - Valence: positive | negative | neutral
   - If user expresses emotion or describes intense experience → tag it
4. **Pattern-match** existing notes (keyword overlap ≥ `similarity_threshold`):
   - Match → link via `recalls`
   - No match → create `question` node
5. **Fill template** with emotion fields if detected. Set `captured_from`, `related`.
6. **Write** to `vault_root/episodes/YYYY/MM/YYYY-MM-DD -- <title>.md`

## Output
```
✓ episodes/YYYY/MM/YYYY-MM-DD -- <title>.md
  → [[Existing Note]] (recalls)
  💚 emotion: high arousal, positive
Saved 1 note to <vault_root>
```

## Rules
- No restructuring existing notes
- No concept promotion (use `consolidate`)
- Multiple ideas → multiple episodes
- High-arousal experiences get emotion tags for better recall later

## Post-Action
After writing note(s), run dashboard update (see `prompts/dashboard-update.md`).
