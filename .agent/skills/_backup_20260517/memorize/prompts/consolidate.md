# consolidate

> Neocortical compression — the "sleep" phase.

Read: `REF.md` · `config/settings.md`

## Pre-flight checks
- `archive_threshold` > `decay_window` — abort if not, warn user
- `last_consolidation_run` + `consolidate_frequency` — warn if run too soon
- `warn_on_early_consolidation` flag

## Steps

1. **Audit** `inbox/` and `episodes/` for notes tagged `#maturity/fleeting`, older than `decay_window` days, with fewer than `min_links_for_evergreen` outbound links.
2. **Cluster** candidates by shared keywords/tags/domains. Clusters of ≥ `min_cluster_size` are promotion candidates.
3. **Promote** each cluster → new `concept` note (`templates/concept.md`):
   - Title: declarative claim (generalized insight)
   - Body: synthesis, not copy
   - Links: `derived-from` → source episodes; `extends`/`supports` → related concepts
   - Tag source episodes `#maturity/developing`
4. **Merge** near-duplicate concept notes: keep broader title, combine links, add alias, update backlinks.
5. **Update MOCs** in `maps/` for each domain that gained concepts.
6. **Decay report**: list episodes older than `archive_threshold` with no concept link → propose archival (requires user confirmation).

## Output

Write each new concept note to `vault_root/concepts/<domain>/<title>.md`.
Write updated MOC notes to `vault_root/maps/<domain>.md`.
Print one line per file: `✓ concepts/domain/Title.md`

End with:
```
Consolidated N→M notes. Merged X. Updated MOCs: [list]. Flagged for archive: Y (confirm to proceed).
```

## Rules
- Never delete episodes — only archive or tag
- No fabricated connections — genuine overlap only
- Concept titles must be falsifiable and specific
- After run: update `last_consolidation_run` in `config/settings.md`
