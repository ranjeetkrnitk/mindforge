# Node Types

Every note created by `/memorize` is one of the following types.
Read this before creating any note.

---

## `concept`
**Tag:** `#type/concept`
**Folder:** `concepts/<domain>/`
**Template:** `templates/concept.md`

An evergreen, claim-based note representing a single, stable idea. Concepts are
the neocortical layer -- they compress many episodes into a generalized insight.

- Title must be a declarative claim: *"Attention mechanisms scale better than RNNs"*
- Must link to at least one source or episode
- Should be domain-agnostic enough to survive context changes

---

## `episode`
**Tag:** `#type/episode`
**Folder:** `episodes/YYYY/MM/`
**Template:** `templates/episode.md`

A timestamped, specific capture. Raw, personal, tied to a moment in time.
This is the hippocampal layer.

- Title must be date-prefixed: `2024-01-15 -- ...`
- Can be messy — accuracy over polish
- Decays: if not linked to a concept within `decay_window`, flagged for review

---

## `question`
**Tag:** `#type/question`
**Folder:** `inbox/` (until answered)

An open question driving inquiry. The "if not found, ask deeper questions" node
from your CLS model. Questions are the engine of new learning.

- Title must end with `?`
- When answered, convert to a `concept` note and link back to the question
- Example: *"Why does sleep improve memory consolidation?"*

---

## `claim`
**Tag:** `#type/claim`
**Folder:** `concepts/<domain>/`
**Template:** `templates/claim.md`

A specific, verifiable assertion extracted from a source. Smaller than a concept,
bigger than a quote.

- Must have a `source` field in frontmatter
- Should note confidence level: `high | medium | low | disputed`
- Example: *"The hippocampus is necessary for spatial navigation (O'Keefe, 1971)"*

---

## `source`
**Tag:** `#type/source`
**Folder:** `sources/`
**Template:** `templates/source.md`

A reference to an external artifact -- paper, book, article, video, conversation.

Required frontmatter fields:
```yaml
author:
year:
url:           # optional
medium:        # paper | book | article | video | conversation | course
key_claims:    # list of [[wikilinks]] to claim or concept notes derived from this
```

---

## `moc`
**Tag:** `#type/moc`
**Folder:** `maps/`
**Template:** `templates/moc.md`

Map of Content -- an index node for a topic. Not a concept itself, but a structured
entry point into a cluster of related notes.

- Contains grouped `[[wikilinks]]` organized by subtopic
- Updated during `consolidate` runs when new concepts emerge in a domain
- Think of it as the table of contents for a region of your graph

---

## `person`
**Tag:** `#type/person`
**Folder:** `people/`

A note about an individual -- researcher, collaborator, author.

Required frontmatter:
```yaml
aliases: []
related_sources: []   # their works as [[wikilinks]]
related_concepts: []  # ideas attributed to them
```
