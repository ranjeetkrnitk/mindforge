# Taxonomy

This is the core ontology for the `/memorize` skill. Every note in the vault
must belong to exactly one **domain** and one **node type**.

---

## Top-Level Domains

These are the root categories. Keep this list stable — adding new domains
should be deliberate, not reactive.

| Domain Tag | Description |
|---|---|
| `#domain/science` | Empirical research, theories, experiments |
| `#domain/technology` | Tools, systems, code, architecture |
| `#domain/philosophy` | Frameworks, ethics, epistemology, mental models |
| `#domain/self` | Personal experiences, reflections, goals |
| `#domain/craft` | Skills being actively learned or practiced |
| `#domain/people` | Notes on individuals, thinkers, collaborators |
| `#domain/reference` | Definitions, specs, docs — lookup-only nodes |

---

## Maturity Levels

Every note has a maturity that reflects its position in the CLS consolidation cycle.

| Tag | Meaning | Layer |
|---|---|---|
| `#maturity/fleeting` | Just captured, unverified | Hippocampal |
| `#maturity/developing` | Revisited at least once, partially linked | Transitional |
| `#maturity/evergreen` | Stable, well-linked, generalized | Neocortical |
| `#maturity/archived` | No longer active but preserved | — |

**Rule:** A note should only be promoted to `evergreen` when it has:
- At least 2 outbound links to other concept nodes
- Been revisited at least once during a `consolidate` run
- A clear, claim-based title (not a question or vague phrase)

---

## Folder Structure (Vault Layout)

```
vault/
├── inbox/              # All new captures land here (fleeting)
├── concepts/           # Evergreen concept notes (neocortical layer)
│   ├── science/
│   ├── technology/
│   ├── philosophy/
│   └── self/
├── episodes/           # Raw episodic notes (hippocampal layer)
│   └── YYYY/MM/        # Organized by date
├── sources/            # Books, papers, articles referenced
├── people/             # Notes on individuals
├── maps/               # MOC (Map of Content) index nodes
└── _system/            # Skill metadata, remap reports, settings
```

---

## Naming Conventions

- **Concept notes:** Declarative sentence titles — `The brain reconstructs memories on retrieval.md`
- **Episode notes:** Date-prefixed — `2024-01-15 — Meeting with team on CLS model.md`
- **MOC notes:** Topic + " MOC" suffix — `Machine Learning MOC.md`
- **Source notes:** Author + Year + Title — `McClelland 1995 — Why there are complementary learning systems.md`

---

## Tag Composition Rules

Every note should carry tags from three dimensions:

```yaml
tags:
  - domain/technology       # what domain
  - type/concept            # what node type (see node-types.md)
  - maturity/evergreen      # how mature
```

Optional additional tags for cross-cutting themes:
```yaml
  - theme/cognition
  - theme/distributed-systems
  - status/needs-review
```
