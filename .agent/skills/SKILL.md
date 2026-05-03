---
name: memorize
version: 0.1.0
description: >
  A second-brain skill grounded in Complementary Learning Systems (CLS) theory.
  Use this skill when the user wants to capture new knowledge, consolidate existing
  notes, build a mind map, or reorganize an Obsidian vault. Triggers on phrases like
  "remember this", "add to my second brain", "memorize", "consolidate my notes",
  "remap my vault", "build a mind map", or any request to store/structure knowledge
  for long-term retrieval. Agent-agnostic — works with Claude, GPT, Cursor, or any
  LLM that can read markdown.
agent: agnostic
compatibility:
  preferred_vault: obsidian
  format: markdown + YAML frontmatter
  requires: none
---

# /memorize — Second Brain Skill

A CLS-theory-backed knowledge management skill. Every concept captured here lives
in one of two layers, mirroring how the brain stores information:

| Layer | CLS Analog | Role |
|---|---|---|
| `episode/` | Hippocampus | Fast, specific, raw captures |
| `concept/` | Neocortex | Slow, generalized, evergreen notes |

---

## Modes

This skill operates in four modes. Read the corresponding prompt file before acting.

### 1. `capture` — Fast intake (hippocampal layer)
> Prompt: `prompts/capture.md`

Use when the user says: *"remember this", "note this down", "memorize", "log this"*

- Creates an `episode` note from raw input
- Tags with `#fleeting` and timestamp
- Links to nearest existing concept node if similarity > threshold
- Does NOT restructure anything

### 2. `consolidate` — Pattern extraction (neocortical layer)
> Prompt: `prompts/consolidate.md`

Use when the user says: *"consolidate", "what have I learned about X", "strengthen my notes", "review"*

- Scans episode notes older than `decay_window` (see `config/settings.md`)
- Promotes recurring patterns into `concept` notes
- Merges near-duplicate episodes
- Updates link graph

### 3. `mindmap` — Graph generation
> Prompt: `prompts/mindmap.md`

Use when the user says: *"show me a mind map", "visualize my knowledge", "map this topic"*

- Generates Obsidian-compatible graph using `[[wikilinks]]`
- Produces a MOC (Map of Content) note as the root node
- Outputs Mermaid diagram for non-Obsidian agents

### 4. `remap` — First-run vault reorganization
> Prompt: `prompts/remap.md`

Use when the user says: *"remap my vault", "reorganize my notes", "apply CLS to my vault"*

- **Destructive operation** — always dry-run first
- Audits existing files against the taxonomy in `schema/taxonomy.md`
- Proposes a new folder structure and tag set
- Renames, moves, and relinks files
- Generates a `_REMAP_REPORT.md` with all changes made

---

## File Structure Reference

```
.agent/skills/memorize/
├── SKILL.md                  ← You are here
├── README.md                 ← Human-facing docs
├── schema/
│   ├── taxonomy.md           ← Core ontology (read before any mode)
│   ├── node-types.md         ← Concept, Episode, Claim, Question, Source
│   └── link-types.md         ← supports, contradicts, extends, recalls, derived-from
├── prompts/
│   ├── capture.md            ← Mode 1 instructions
│   ├── consolidate.md        ← Mode 2 instructions
│   ├── mindmap.md            ← Mode 3 instructions
│   └── remap.md              ← Mode 4 instructions
├── templates/
│   ├── concept.md            ← Evergreen note template
│   ├── episode.md            ← Fleeting capture template
│   └── moc.md                ← Map of Content template
└── config/
    └── settings.md           ← Tunable parameters
```

---

## Always-Read Files

Before executing **any** mode, read:
1. `schema/taxonomy.md` — so you know the ontology
2. `schema/node-types.md` — so you create the right note type
3. `config/settings.md` — so you respect the user's thresholds

Then read the mode-specific prompt file.

---

## Output Conventions

- All notes use YAML frontmatter (see templates)
- Links use Obsidian `[[wikilink]]` syntax
- Tags use `#kebab-case`
- Dates use ISO 8601: `2024-01-15`
- Mermaid diagrams used as fallback for non-Obsidian environments
