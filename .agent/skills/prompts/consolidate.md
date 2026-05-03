# Prompt: consolidate mode

> Slow neocortical compression. Pattern extraction from episodes.
> This is the "sleep" phase of your second brain.

---

## Your job in this mode

Review recent episodes, find patterns, and promote durable insights into
concept notes. This is the CLS replay cycle — compress specific memories into
generalized knowledge.

---

## Step-by-Step

### Step 1 — Audit the inbox

List all notes in `inbox/` and `episodes/` that:
- Are tagged `#maturity/fleeting`
- Were created more than `decay_window` days ago (see `config/settings.md`)
- Have fewer than `min_links` outbound links

These are candidates for consolidation or archival.

### Step 2 — Cluster by theme

Group the candidate episodes by shared keywords, tags, and domains.
A cluster of 3+ episodes touching the same idea is a signal to promote.

> Example cluster:
> - `2024-01-10 — Read about hippocampal pattern completion`
> - `2024-01-13 — Noticed I remembered a song from a single note`
> - `2024-01-15 — CLS theory discussion with Claude`
>
> → Promote to concept: *"Pattern completion allows full memory retrieval from partial cues"*

### Step 3 — Promote to concept

For each cluster, create a new `concept` note using `templates/concept.md`:
- Title: declarative claim (the generalized insight)
- Body: synthesized understanding, not a copy of the episodes
- Links: `derived-from` → each source episode, `extends` or `supports` → related concepts

Tag the source episodes as `#maturity/developing` once linked.

### Step 4 — Merge near-duplicates

If two concept notes say essentially the same thing, merge them:
- Keep the more general title
- Combine their link sets
- Add an alias for the absorbed note
- Update all backlinks

### Step 5 — Update MOCs

For each domain that gained new concepts, update or create the corresponding
MOC note in `maps/`. Add the new concept under the appropriate section.

### Step 6 — Decay report

List any episodes that:
- Are older than `archive_threshold` days
- Have never been linked to a concept

Propose archiving them to `_archived/`. Do not archive without user confirmation.

---

## Output format

```
CONSOLIDATED: N episodes → M new concept notes
MERGED: X near-duplicate pairs
UPDATED MOCs: [list]
FLAGGED FOR ARCHIVE: [list] — awaiting confirmation
```

Then output each new concept note in full.

---

## Rules for consolidate mode

- Never delete episodes — only archive or tag
- Do not fabricate connections — only promote clusters with genuine thematic overlap
- Keep concept titles falsifiable and specific — avoid vague titles like *"AI is interesting"*
- Run consolidate at most once per `consolidate_frequency` days (see settings)
