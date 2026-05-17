# recall

> Retrieve what vault knows about a topic.

## Steps

1. **Parse query**
   - Keywords: nouns, entities
   - Hints: domain, scope ("recent", "evergreen", "emotional"), emotion
   - Mode: question | lookup | related

2. **Search** (priority: concepts → maps → episodes → sources → inbox)
   - Match: filename, tags, body
   - Cap: 20 candidates

3. **Rank**
   | Signal | Weight |
   |--------|--------|
   | evergreen | +3 |
   | developing | +1 |
   | keyword in filename/tags | +2 |
   | keyword in body | +1 (cap 3) |
   | arousal-high | +3 |
   | mood-congruent match | +1.5 |

4. **Answer**
   - Question → synthesize, cite sources
   - Lookup → return note content
   - Related → map links to `mindmap_depth`

5. **Surface gaps**
   - Open questions
   - Fleeting clusters ready to consolidate
   - High-arousal unlinked episodes

## Output
```
## Recall: <topic>
### Answer
<grounded in vault>
### Sources
📗 [[Note]] [evergreen] — "excerpt"
### Suggestions
→ Consolidate: N fleeting episodes ready
```

## Rules
- Read-only
- Ground in vault content only
- Preserve emotional context
- Cite every claim
