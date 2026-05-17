# plan

> Generate comprehensive planning document.

## Steps

1. **Load** all prior context (discover, elicit, review)
2. **Verify** no unresolved blockers from review
3. **Ask** destination via `ask_user`:
   - Session folder (default)
   - Obsidian vault (if memorize configured)
   - Clipboard
4. **Generate** using `templates/prd.md`
5. **Write** and confirm

## Output

```
✓ {{filename}}
  Sections: 11 | Requirements: N | Risks: M | Phases: P
  Saved to: {{path}}
```

## Rules
- Include all elicited requirements
- Unresolved items → "Open Questions"
- No placeholder text
