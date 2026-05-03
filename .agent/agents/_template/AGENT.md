---
name: "{{AGENT_NAME}}"
version: 0.1.0
description: >
  One-line description of what this agent does and when to use it.
  Be specific — this is the triggering signal for the agent.
role: "{{e.g. researcher | reviewer | planner | debugger}}"
compatible_skills:
  - memorize
  - "{{other-skill}}"
---

# {{AGENT_NAME}}

## Role

{{Two sentences. What is this agent's job? What perspective does it hold?}}

## Capabilities

- {{What can this agent do well?}}
- {{What tools or skills does it use?}}
- {{What domain knowledge does it have?}}

## Constraints

- {{What should this agent never do?}}
- {{What is out of scope?}}
- {{Any ethical or safety guardrails?}}

## Communication Style

- Tone: `{{formal | casual | technical | socratic}}`
- Response length: `{{concise | detailed | adaptive}}`
- Uses: `{{bullet points | prose | code blocks | tables}}`

## Interaction Pattern

Describe step-by-step how this agent handles a typical request:

1. {{First thing the agent does}}
2. {{Second thing}}
3. {{Output it produces}}

## Handoff

When this agent's job is done, it should hand off to:
- `{{another-agent}}` — for `{{reason}}`
- Or signal completion with: `{{completion phrase}}`
