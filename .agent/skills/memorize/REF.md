# memorize — Quick Reference

> Agents: read this file ONCE before any mode. Replaces schema/taxonomy.md, schema/node-types.md, schema/link-types.md.

## Node Types

| type | folder | template | title format |
|---|---|---|---|
| `concept` | `concepts/<domain>/` | `templates/concept.md` | declarative claim sentence |
| `episode` | `episodes/YYYY/MM/` | `templates/episode.md` | `YYYY-MM-DD -- Short title` |
| `claim` | `concepts/<domain>/` | `templates/claim.md` | verifiable assertion |
| `question` | `inbox/` | — | ends with `?` |
| `source` | `sources/` | `templates/source.md` | `Author YEAR -- Title` |
| `moc` | `maps/` | `templates/moc.md` | `Topic MOC` |
| `person` | `people/` | — | person name |

## Domains
`science` · `technology` · `philosophy` · `self` · `craft` · `people` · `reference`

## Maturity
`fleeting` → `developing` → `evergreen` · `archived`

Evergreen requires: 2+ outbound concept links + 1 consolidate revisit + claim-based title.

## Link Types
| type | meaning |
|---|---|
| `supports` | evidence for another note |
| `contradicts` | challenges another note |
| `extends` | builds on without contradicting |
| `recalls` | episode that triggered a concept retrieval |
| `derived-from` | concept distilled from episodes/sources |
| `questions` | question probing a concept |
| `answers` | concept resolving a question |

## Tags
YAML frontmatter (no `#`): `tags: [domain/X, type/Y, maturity/Z]`
Inline body text: `#domain/X` syntax with `#`.

## Naming
- episode: `YYYY-MM-DD -- Short title.md`
- concept: `Declarative claim sentence.md`
- source: `Author YEAR -- Title.md`
- moc: `Topic MOC.md`

## Vault Paths (defaults)
`inbox/` · `concepts/` · `episodes/YYYY/MM/` · `sources/` · `maps/` · `people/` · `_archived/` · `_system/`
