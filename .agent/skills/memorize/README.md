# /memorize — Second Brain Skill

> Agent-agnostic knowledge management grounded in Complementary Learning Systems (CLS) theory.

## What is this?

This skill turns any AI agent into a second brain. It mirrors how the human brain
actually encodes and consolidates memory — using two complementary systems:

- **Fast layer (Hippocampus):** Captures raw, specific experiences quickly
- **Slow layer (Neocortex):** Gradually abstracts patterns into lasting knowledge

## Quickstart

Tell your agent:

| You say | Mode triggered |
|---|---|
| `"memorize: I learned that X causes Y"` | `capture` |
| `"consolidate my notes on machine learning"` | `consolidate` |
| `"show me a mind map of my AI notes"` | `mindmap` |
| `"remap my vault using CLS theory"` | `remap` (first-run) |
| `"harvest this session"` | `harvest` |

## Obsidian Setup

1. Point your vault to the directory where captured notes are stored
2. Enable the Graph View plugin
3. Run `remap` mode once on your existing vault to apply the taxonomy
4. Use `capture` daily, `consolidate` weekly, `harvest` at end of any rich session

## CLS Theory — 30 Second Primer

Complementary Learning Systems theory (McClelland et al., 1995) proposes that
the brain uses two systems that work together:

- The **hippocampus** learns fast and stores specific episodes (your meeting notes,
  a paper you read, an idea you had)
- The **neocortex** learns slowly and builds generalized models (your understanding
  of a field, mental models, evergreen principles)

Memory becomes durable when episodes are "replayed" and gradually compressed into
the neocortex. This skill implements that loop.

## Contributing

This skill is intentionally minimal. Extend it by:
- Adding new node types to `schema/node-types.md`
- Adding domain-specific taxonomies to `schema/taxonomy.md`
- Writing new prompt variants in `prompts/`
