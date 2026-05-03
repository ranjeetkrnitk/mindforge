# Link Types

Links between notes carry semantic meaning. Always annotate links with their
relationship type using inline comments or a `links` frontmatter block.

---

## Relationship Types

### `supports`
One note provides evidence or reasoning for another.
```
[[Attention mechanisms scale better than RNNs]] — supports → [[Transformers are the dominant architecture]]
```

### `contradicts`
One note challenges or disputes another.
```
[[Sleep deprivation does not affect short-term recall]] — contradicts → [[Sleep is required for memory consolidation]]
```

### `extends`
One note builds on or elaborates another without contradicting it.
```
[[Reconsolidation modifies memories on retrieval]] — extends → [[Memories are not fixed after encoding]]
```

### `recalls`
An episode that triggered retrieval of a concept (the pattern-matching event).
```
[[2024-01-15 — Read paper on hippocampal replay]] — recalls → [[CLS theory separates fast and slow learning]]
```

### `derived-from`
A concept distilled from one or more episodes or sources.
```
[[Pattern completion is the hippocampus's core function]] — derived-from → [[McClelland 1995 — ...]]
```

### `questions`
A question note pointing at the concept it is probing.
```
[[Why does novelty boost encoding strength?]] — questions → [[Novelty detection triggers norepinephrine release]]
```

### `answers`
The reverse — a concept that resolves a question.
```
[[Novelty detection triggers norepinephrine release]] — answers → [[Why does novelty boost encoding strength?]]
```

---

## Usage in Obsidian

Annotate links inline:
```markdown
This is related to [[CLS Theory MOC]] *(extends)* and directly challenges
[[Memories are fixed after consolidation]] *(contradicts)*.
```

Or in frontmatter for structured queries:
```yaml
links:
  - target: "[[CLS Theory MOC]]"
    type: extends
  - target: "[[Memories are fixed after consolidation]]"
    type: contradicts
```

---

## Link Strength

During `consolidate` mode, link strength is computed as:

```
strength = (co-occurrence count) × (recency weight) × (explicit annotation bonus)
```

- **Co-occurrence:** How often two notes appear in the same episode
- **Recency weight:** More recent links decay slower
- **Annotation bonus:** Explicitly typed links (above) get 1.5× weight vs bare wikilinks

High-strength links are candidates for concept promotion.
