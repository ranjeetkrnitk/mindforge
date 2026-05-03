# Architecture

## Core Philosophy

This repo is built around one constraint: **every piece must work with any agent**.
No vendor lock-in. No tool-specific syntax. Pure markdown + YAML frontmatter.

The knowledge layer is grounded in **Complementary Learning Systems (CLS) theory**
(McClelland et al., 1995) — the neuroscience of how the brain encodes and
consolidates memory using two complementary systems.

---

## The Four Layers

### 1. Skills — "How to do X"
Skills are task-level instruction sets. An agent reads a SKILL.md and knows
exactly how to perform a complex, multi-step task. Skills are:
- Self-contained directories
- Composed of prompts, templates, schema, and config
- Mode-based (one skill, multiple modes of operation)

### 2. Agents — "Who does X"
Agents are role definitions. They define a persona, its capabilities,
its constraints, and its communication style. An agent may use multiple
skills in the course of its work. Agents are:
- Composable — you can layer agents with plugins
- System-prompt ready — `system-prompt.md` drops straight into any LLM

### 3. Plugins — "How agent acts"
Plugins are behavioral modifiers. They don't define what an agent does
but *how* it does it — output format, reasoning style, verbosity, constraints.
Plugins inject into the system prompt at a specified point (prefix/suffix/override).

### 4. MCP Servers — "What agent can access"
MCP (Model Context Protocol) servers expose external tools to agents.
Each server has a manifest (`server.json`), documentation, and usage guide.
Agents reference MCP servers by name; the server handles the actual integration.

---

## CLS Theory Applied

| Brain System | This Repo | Role |
|---|---|---|
| Hippocampus | `episodes/` notes | Fast, specific, raw captures |
| Neocortex | `concepts/` notes | Slow, generalized, evergreen |
| Sleep replay | `consolidate` mode | Compress episodes → concepts |
| Pattern completion | `capture` mode matching | Find nearest existing concept |
| Novelty detection | `question` node type | New info with no existing match |

The `/memorize` skill implements this full cycle.

---

## Data Flow

```
User input
    ↓
capture mode          ← hippocampal layer (fast, specific)
    ↓
episode note
    ↓  (after decay_window days)
consolidate mode      ← neocortical layer (slow, generalized)
    ↓
concept note
    ↓
mindmap mode          ← graph visualization
    ↓
MOC note + Mermaid diagram
```

---

## Design Decisions

**Why markdown over JSON/YAML for skill definitions?**
Markdown is readable by humans and all LLMs without parsing. JSON skills
would require an interpreter layer that breaks agent-agnosticism.

**Why separate prompts per mode?**
Monolithic prompts grow unmanageable. Mode-specific files allow targeted
iteration — you can improve `consolidate.md` without touching `capture.md`.

**Why `config/settings.md` instead of `.json`?**
Agents read config as context. A markdown file with YAML blocks is both
machine-parseable and human-readable without tooling.

**Why `helpers/` separate from `.agent/`?**
`.agent/` is instruction-space (agent-readable). `helpers/` is
implementation-space (human/script-runnable). Mixing them breaks the
clean abstraction.
