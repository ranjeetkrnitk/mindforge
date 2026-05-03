# Settings

> Agents: read this file before any mode. Edit values to customize behavior.

## Consolidation
```yaml
decay_window: 7                # days before fleeting episode is consolidation-eligible
archive_threshold: 30          # days before unlinked episode is archival candidate (must be > decay_window)
min_cluster_size: 3            # min episodes in a cluster to trigger concept promotion
min_links_for_evergreen: 2     # min outbound links for a concept to be evergreen
consolidate_frequency: 7       # min days between consolidation runs
last_consolidation_run: ""     # ISO 8601 — updated by agent after each run
```

## Pattern Matching
```yaml
similarity_threshold: 0.4      # min keyword overlap for a pattern match (0.0–1.0)
mindmap_depth: 3               # max link traversal depth for mindmap
max_related_suggestions: 5     # max related notes surfaced per capture
```

## Harvest
```yaml
harvest_min_turns: 2           # min turns in a span to be worth capturing
harvest_merge_threshold: 0.5   # keyword overlap to merge adjacent spans
```

## Link Strength
```yaml
link_weights:
  co_occurrence: 1.0
  recency_half_life: 14        # days — strength halves every N days
  annotation_bonus: 1.5        # typed links get 1.5x weight
  backlink_bonus: 1.2          # bidirectional links get 1.2x weight
```

## Vault Paths
```yaml
vault_root: "./"
inbox_path: "inbox/"
concepts_path: "concepts/"
episodes_path: "episodes/"
sources_path: "sources/"
maps_path: "maps/"
people_path: "people/"
system_path: "_system/"
archive_path: "_archived/"
```

## Prune
```yaml
prune_min_body_words: 20           # files with fewer body words are classified as "stub"
prune_dry_run_default: true        # when true, only report — do not patch frontmatter
prune_requires_confirmation: true  # require explicit yes before archiving stubs
```

## Agent Behavior
```yaml
remap_dry_run_default: true
archive_requires_confirmation: true
warn_on_early_consolidation: true
output_format: obsidian        # obsidian | mermaid | both
```
