---
name: ideate
version: 0.1.0
description: >
  Project planning skill that grills requirements, reviews for gaps, and produces
  comprehensive planning documents. Combines stakeholder elicitation, PRD generation,
  and implementation planning.
  Triggers: "plan project", "new idea", "elicit requirements", "review requirements".
agent: agnostic
---

# /ideate

## Load Order
1. `../_shared/conventions.md` — cross-skill standards
2. `REF.md` — elicitation frameworks, document templates
3. `config/settings.md` — question depth, output format

## Setup
On first run, ask:
1. *"Project/idea name?"*
2. *"Brief description (1-2 sentences)?"*
3. *"Who are the stakeholders? (comma-separated roles)"*

Store context in session for follow-up modes.

## Modes

| # | Mode | Trigger | Prompt | Purpose |
|---|------|---------|--------|---------|
| 1 | `discover` | "new idea", "explore this", "ideate" | `prompts/discover.md` | Open exploration, vision clarity |
| 2 | `elicit` | "elicit requirements", "gather requirements", "grill me" | `prompts/elicit.md` | Structured Q&A across domains |
| 3 | `review` | "review requirements", "find gaps", "validate" | `prompts/review.md` | Gap analysis, conflicts, risks |
| 4 | `plan` | "create plan", "generate PRD", "planning document" | `prompts/plan.md` | Full planning document output |

## Workflow
```
discover → elicit → review → plan
   ↑__________|_________|
        (iterate)
```

Run modes sequentially or jump to any. Each mode builds on prior context.

## Output Conventions
- Ask questions one domain at a time (not all at once)
- Summarize answers before moving to next domain
- Use `ask_user` tool for interactive elicitation
- Final document: markdown to session folder or vault
