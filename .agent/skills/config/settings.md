# Settings

Tunable parameters for the `/memorize` skill.
Agents should read this file before executing any mode.

---

## Consolidation Settings

```yaml
# How many days before a fleeting episode is eligible for consolidation review
decay_window: 7

# How many days before an unlinked episode is flagged for archival
archive_threshold: 30

# Minimum number of episodes in a cluster to trigger concept promotion
min_cluster_size: 3

# Minimum outbound links for a concept to be marked "evergreen"
min_links_for_evergreen: 2

# How often to run consolidation (in days) — agent should warn if run too frequently
consolidate_frequency: 7
```

---

## Pattern Matching Settings

```yaml
# Minimum keyword overlap to consider a pattern match "found" (0.0 - 1.0)
similarity_threshold: 0.4

# Maximum depth to traverse links when building a mind map
mindmap_depth: 3

# Maximum number of related notes to surface per capture
max_related_suggestions: 5
```

---

## Link Strength Weights

```yaml
link_weights:
  co_occurrence: 1.0       # notes appear in the same episode
  recency_half_life: 14    # days — link strength halves every N days
  annotation_bonus: 1.5    # multiplier for explicitly typed links
  backlink_bonus: 1.2      # multiplier when link is bidirectional
```

---

## Vault Paths (customize per user)

```yaml
vault_root: "./"           # relative to vault root
inbox_path: "inbox/"
concepts_path: "concepts/"
episodes_path: "episodes/"
sources_path: "sources/"
maps_path: "maps/"
people_path: "people/"
system_path: "_system/"
archive_path: "_archived/"
```

---

## Agent Behavior

```yaml
# Always dry-run remap before applying
remap_dry_run_default: true

# Confirm before archiving any note
archive_requires_confirmation: true

# Warn if consolidate is run within consolidate_frequency days of last run
warn_on_early_consolidation: true

# Output format preference
output_format: obsidian   # obsidian | mermaid | both
```

---

## Customization Notes

- Increase `decay_window` if you capture infrequently (e.g., set to 14 for weekly capturers)
- Lower `similarity_threshold` to cast a wider pattern-matching net
- Set `output_format: mermaid` if not using Obsidian
- `archive_threshold` should always be > `decay_window`
