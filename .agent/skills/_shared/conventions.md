# Shared Skill Conventions

> All vault skills load this first via SKILL.md. Single source of truth.

## Setup (first-run)
```
1. Check config/user.md for vault_root
2. Empty? Try copying from memorize/config/user.md
3. Still empty? Ask user for path
4. Validate: exists + is directory
5. Show: "💡 /add-dir ~/.copilot/skills" and "/add-dir <vault>"
```

## Vault Scan
```
1. glob vault_root/**/*.md
2. Skip: _archived/, _system/, .obsidian/
3. Parse YAML frontmatter → created, tags, maturity, emotion
4. Fallback: file mtime if no created
5. Extract [[wikilinks]] → build link graph
```

## Link Extraction
- `[[Note]]` → Note
- `[[Note|Alias]]` → Note (ignore alias)
- `[[Folder/Note]]` → Note (ignore path)
- `![[Embed]]` → count as link

## Output Rules
- One line per file: `✓ path/to/file.md`
- End: `Saved N note(s) to <vault_root>`
- No content in output unless asked
- Use wikilinks: `[[Note Title]]`

## Display Format
- Section headers: emoji + title (e.g., "🔄 Consolidation")
- Status: ✓ success, ⚠️ warning, ✗ error
- Bar charts: `████░░░░ 50%`
- Deltas: `↑` increase, `↓` decrease

## Emotion Schema
```yaml
emotion:
  arousal: high|medium|low
  valence: positive|negative|neutral
  label: "optional"
```

## Maturity
`fleeting` → `developing` → `evergreen` → `archived`

## Common Tags
- `domain/X` - science, technology, philosophy, self, craft
- `type/X` - episode, concept, claim, question, source
- `maturity/X` - fleeting, developing, evergreen
- `emotion/arousal-X` - high, medium, low

## Graph Metrics
| Metric | Formula |
|--------|---------|
| hub | incoming_links |
| bridge | cross_domain_links / total |
| orphan_risk | age × 0.1 / (links + 1) |

## Safety Rules
- Never hard-delete (archive instead)
- Skip _archived/, _system/ unless explicitly requested
- Handle malformed frontmatter: log warning, skip, continue
- Never overwrite without reading first

## Frontmatter Handling
- Missing → use file mtime for created, leave others empty
- Malformed → log warning, skip note, continue
- Partial → use available fields, fallback for missing

## Reflection Prompts (end of output)
Generate 2-3 questions grounded in findings:
1. Surprise: "What surprised you about [finding]?"
2. Action: "Which [item] needs attention?"
3. Meta: "Is [pattern] intentional?"

## Writing Style
- Imperatives: "Extract", "Scan", "Write"
- No filler: remove "please", "should", "you will"
- Bullets over prose
- Max 50 lines per prompt file
