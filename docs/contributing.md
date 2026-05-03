# Contributing

## Before You Add Anything

Ask: does this belong in `.agent/` (instruction-space) or `helpers/` (implementation-space)?

| It's a... | Goes in |
|---|---|
| Task instruction set | `.agent/skills/` |
| Role/persona definition | `.agent/agents/` |
| Behavioral modifier | `.agent/plugins/` |
| External tool connector | `.agent/mcp-servers/` |
| Python/bash utility script | `helpers/` |
| Architecture decision | `docs/` |

## Checklist for a New Skill

- [ ] Directory created at `.agent/skills/<name>/`
- [ ] `SKILL.md` has valid YAML frontmatter (name, version, description)
- [ ] All modes listed in `SKILL.md` have a matching file in `prompts/`
- [ ] `schema/` files define all types and rules the skill operates on
- [ ] `config/settings.md` has all tunable parameters with sensible defaults
- [ ] Templates use `{{UPPER_SNAKE_CASE}}` placeholders consistently
- [ ] Root `README.md` skill count updated

## Checklist for a New Agent

- [ ] Directory at `.agent/agents/<name>/`
- [ ] `AGENT.md` filled (role, capabilities, constraints, handoff)
- [ ] `system-prompt.md` tested with at least one LLM
- [ ] Skills this agent uses are documented in `AGENT.md`

## Checklist for a New MCP Server

- [ ] Directory at `.agent/mcp-servers/<name>/`
- [ ] `server.json` validates against MCP spec
- [ ] `MCP.md` includes setup, auth, and limitations
- [ ] `docs/usage.md` covers every tool with input/output examples
- [ ] Tested locally before committing

## Commit Message Format

```
<type>(<scope>): <short description>

Types: feat | fix | docs | refactor | chore
Scope: skill/<name> | agent/<name> | plugin/<name> | mcp/<name> | helpers | docs

Examples:
  feat(skill/memorize): add consolidate mode
  fix(helpers/vault): handle missing frontmatter
  docs(architecture): add CLS theory section
  feat(mcp/notion): add initial server manifest
```
