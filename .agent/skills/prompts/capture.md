# Prompt: capture mode

> Fast hippocampal intake. Speed over perfection.

---

## Your job in this mode

The user has given you something to remember. Your job is to:

1. Parse the raw input
2. Identify the closest existing concept node (pattern matching)
3. Create an `episode` note using `templates/episode.md`
4. Link it to matching concepts if found, or create a `question` node if not
5. Output the note content and its intended file path

---

## Step-by-Step

### Step 1 — Extract the core claim

Strip filler. Identify the atomic idea being captured.

> Input: *"I was reading about sleep and apparently the brain replays memories during deep sleep to move them to long-term storage"*
> Core claim: *"The brain replays memories during deep sleep for long-term consolidation"*

### Step 2 — Pattern match against existing knowledge

Search for existing concept or episode notes whose titles or tags overlap with
keywords from the claim. This mirrors hippocampal pattern completion.

- If **match found (similarity > threshold):** Link the new episode to that concept using `recalls`
- If **no match found:** Create a `question` note: *"How does memory replay during sleep work?"* and flag for future consolidation

### Step 3 — Classify the node type

Using `schema/node-types.md`, decide: is this an `episode`, `claim`, or `concept`?

- Raw personal experience → `episode`
- Verifiable assertion with a source → `claim`
- Already well-formed insight → `concept` (rare in capture mode)

### Step 4 — Fill the template

Use `templates/episode.md`. Fill all frontmatter fields. Be specific about:
- `captured_from`: where did this come from? (conversation, article, thought, etc.)
- `related`: list of `[[wikilinks]]` to existing notes

### Step 5 — Output

Return:
```
FILE PATH: episodes/YYYY/MM/YYYY-MM-DD — <short title>.md
---
<full note content>
```

Also return a one-line summary:
```
LINKED TO: [[Existing Concept Name]] (recalls) | OR | NEW QUESTION: [[...?]]
```

---

## Rules for capture mode

- Do NOT restructure or rename existing notes
- Do NOT promote to `concept` during capture — that happens in `consolidate`
- Keep the episode title specific and date-prefixed
- If the input contains multiple distinct ideas, create multiple episode notes
- Maximum one `question` node per capture session
