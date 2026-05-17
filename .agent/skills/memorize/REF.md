# memorize — Quick Reference

> Agents: loaded via SKILL.md. Skill-specific node types and links.

## Node Types
| type | folder | template | title |
|---|---|---|---|
| `concept` | `concepts/<domain>/` | `concept.md` | declarative claim |
| `episode` | `episodes/YYYY/MM/` | `episode.md` | `YYYY-MM-DD -- Title` |
| `claim` | `concepts/<domain>/` | `claim.md` | verifiable assertion |
| `question` | `inbox/` | — | ends with `?` |
| `source` | `sources/` | `source.md` | `Author YEAR -- Title` |
| `moc` | `maps/` | `moc.md` | `Topic MOC` |

## Domains
`science` · `technology` · `philosophy` · `self` · `craft` · `people` · `reference`

## Maturity
`fleeting` → `developing` → `evergreen` · `archived`

Evergreen: 2+ outbound links + consolidate revisit + claim title.

## Link Types
| type | meaning |
|---|---|
| `supports` | evidence for note |
| `contradicts` | challenges note |
| `extends` | builds on |
| `recalls` | episode triggered retrieval |
| `derived-from` | distilled from episodes |
| `questions` / `answers` | Q&A relationship |

## Emotion
See `_shared/conventions.md`. Recall boosts: arousal=high → +3, matching valence → +1.5

## Tags
Frontmatter: `tags: [domain/X, type/Y, maturity/Z, emotion/arousal-high]`

## Paths
`inbox/` · `concepts/` · `episodes/YYYY/MM/` · `sources/` · `maps/` · `_archived/`
