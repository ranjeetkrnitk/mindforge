# How Skills Work

A skill is a self-contained directory that teaches an agent how to perform
a complex, multi-step task. Skills are the primary building block of this repo.

## Anatomy of a Skill

```
skill-name/
├── SKILL.md          # Required. Frontmatter + mode index + file map.
├── README.md         # Human-facing documentation.
├── schema/           # Ontology, types, rules the skill operates on.
├── prompts/          # One file per mode. Agent reads the relevant one.
├── templates/        # Output templates (notes, reports, etc.)
└── config/           # Tunable parameters.
```

## How an Agent Uses a Skill

1. Agent reads `SKILL.md` to understand available modes and file layout
2. Agent reads `schema/` files for domain rules (always)
3. Agent reads `config/settings.md` for thresholds (always)
4. Agent reads the mode-specific `prompts/<mode>.md`
5. Agent executes, using `templates/` as output scaffolds

## Adding a New Skill

1. Copy `_template/` (if it exists) or create the directory structure manually
2. Write `SKILL.md` — define modes, file map, always-read files
3. Write `schema/` files — what are the rules and types?
4. Write one `prompts/<mode>.md` per mode
5. Write templates for each output type
6. Set sensible defaults in `config/settings.md`
7. Update the root `README.md` skill count

## Naming Conventions

- Skill directory: `kebab-case`
- Mode names: `kebab-case` (capture, consolidate, remap, mindmap)
- Template placeholders: `{{UPPER_SNAKE_CASE}}`
- Config keys: `snake_case`
