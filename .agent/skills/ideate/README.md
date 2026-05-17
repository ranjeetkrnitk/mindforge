# ideate

Project planning skill that transforms rough ideas into comprehensive planning documents.

## Quick Start

```
/ideate new idea        # Start with discovery
/ideate grill me        # Jump to requirements gathering
/ideate review          # Validate requirements
/ideate create plan     # Generate planning document
```

## Workflow

```
┌─────────┐    ┌─────────┐    ┌────────┐    ┌──────┐
│ discover│ →  │ elicit  │ →  │ review │ →  │ plan │
└─────────┘    └─────────┘    └────────┘    └──────┘
     ↑              │              │
     └──────────────┴──────────────┘
              (iterate as needed)
```

## Modes

| Mode | Purpose | Output |
|------|---------|--------|
| **discover** | Clarify vision, explore problem space | Vision summary, assumptions |
| **elicit** | Structured Q&A across 7 domains | Requirements table with priorities |
| **review** | Find gaps, conflicts, validate SMART | Issues list, recommendations |
| **plan** | Generate full planning document | Markdown PRD |

## Elicitation Domains

1. **Vision** - Problem, opportunity, why now
2. **Users** - Personas, needs, technical comfort
3. **Functional** - Features, journeys, data
4. **Non-Functional** - Performance, security, scale
5. **Constraints** - Time, budget, tech, team
6. **Risks** - What could fail, unknowns
7. **Success** - Metrics, KPIs, definition of done

## Comparison with Similar Skills

| Feature | ideate | plan-feature | bhn-dev-architect |
|---------|--------|--------------|-------------------|
| Discovery phase | ✓ | ✗ | ✗ |
| Interactive Q&A | ✓ | ✗ | ✗ |
| Gap analysis | ✓ | ✗ | ✗ |
| Conflict detection | ✓ | ✗ | ✗ |
| PRD generation | ✓ | Checklist only | Architecture doc |
| MoSCoW priority | ✓ | ✗ | ✗ |
| SMART validation | ✓ | ✗ | ✗ |
| Iterative workflow | ✓ | Linear | Linear |

## Example Session

```
User: /ideate new idea
Agent: What problem are you trying to solve?
User: "Teams waste time in meetings that could be async"
Agent: Why is this important now?
User: "Remote work made it worse"
Agent: What does success look like in 6 months?
User: "50% fewer meetings, same outcomes"

... continues through elicit, review, plan ...

Agent: ✓ Planning document generated
       📄 async-meetings-prd.md
       Saved to: ~/.copilot/session-state/.../files/
```

## Configuration

Edit `config/settings.md` to adjust:
- `question_depth`: quick | standard | deep
- `priority_scheme`: moscow | high-med-low
- `output_format`: markdown

## Integration with Other Skills

- **memorize**: Save planning docs to Obsidian vault
- **reflect**: Review project progress over time
