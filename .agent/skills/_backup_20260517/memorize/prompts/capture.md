# capture

> Fast hippocampal intake.

Read: `REF.md` · `config/settings.md` (`similarity_threshold`, `max_related_suggestions`)

## Steps

1. **Extract** the atomic core claim. Strip filler.
2. **Classify** node type (REF.md):
   - raw experience → `episode`
   - sourced verifiable assertion → `claim`
   - already well-formed insight → `concept` (rare)
3. **Pattern-match** against existing notes (keyword overlap):
   - overlap ≥ `similarity_threshold` → link via `recalls`
   - no match → create `question` node + flag for consolidation
4. **Fill template**. Set `captured_from` and `related`.
5. **Write file** to `vault_root/episodes/YYYY/MM/YYYY-MM-DD -- <title>.md` using available file tools.
   Print: `✓ episodes/YYYY/MM/YYYY-MM-DD -- <title>.md`
   If linked: `  → [[Existing Note]] (recalls)` | If new: `  → new question: [[...?]]`
   End: `Saved 1 note to <vault_root>`

## Rules
- No restructuring or renaming existing notes
- No concept promotion — that happens in `consolidate`
- Multiple distinct ideas → multiple episode notes
- One `question` per unmatched idea; cap at `max_related_suggestions`
