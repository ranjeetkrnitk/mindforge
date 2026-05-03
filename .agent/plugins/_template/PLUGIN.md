---
name: "{{PLUGIN_NAME}}"
version: 0.1.0
description: >
  What behavior this plugin modifies or adds. When should an agent load it?
type: "{{prefix | suffix | override | filter}}"
compatible_agents:
  - all   # or list specific agents
compatible_skills:
  - all   # or list specific skills
---

# {{PLUGIN_NAME}} Plugin

## What This Changes

{{Describe precisely what this plugin modifies about the agent's behavior.
Is it changing output format? Adding a reasoning step? Enforcing a constraint?}}

## When to Load

Load this plugin when:
- {{Condition 1}}
- {{Condition 2}}

Do NOT load when:
- {{Anti-condition 1}}

## Inject Point

Where in the system prompt does this plugin's snippet go?

- `prefix` — before all other instructions
- `suffix` — after all other instructions
- `override` — replaces a specific section (name it below)
- `filter` — post-processes output before returning to user

Inject point: `{{prefix | suffix | override: <section name> | filter}}`

## Effect on Output

Before plugin:
```
{{example output without plugin}}
```

After plugin:
```
{{example output with plugin}}
```

---

See `inject.md` for the actual prompt snippet to inject.
