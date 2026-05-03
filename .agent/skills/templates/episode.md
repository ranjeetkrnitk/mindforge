---
title: "{{DATE}} — {{SHORT_DESCRIPTION}}"
created: {{DATETIME}}
tags:
  - domain/{{DOMAIN}}
  - type/episode
  - maturity/fleeting
captured_from: "{{conversation | article | book | thought | meeting}}"
source_url: ""   # optional
related:
  - "[[{{nearest_concept_or_leave_empty}}]]"
promoted: false  # set to true when consolidated into a concept
---

# {{DATE}} — {{SHORT_DESCRIPTION}}

## Raw Capture

{{VERBATIM_OR_NEAR_VERBATIM_INPUT — messy is fine}}

## Initial Interpretation

{{ONE OR TWO SENTENCES — what do you think this means right now?}}

## Pattern Match

- Closest existing concept: [[{{MATCHED_CONCEPT_OR_NONE}}]]
- Match confidence: {{high | low | none}}
- If no match → Open question: [[{{QUESTION_THIS_RAISES}}?]]

## Fleeting Tags

{{#theme/X #theme/Y — keywords that may help future consolidation}}
