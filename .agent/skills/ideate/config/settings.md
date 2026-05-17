# ideate settings

## Elicitation
```yaml
question_depth: standard    # quick | standard | deep
domains_order:
  - vision
  - users
  - functional
  - non_functional
  - constraints
  - risks
  - success
max_questions_per_turn: 3   # Don't overwhelm
```

## Output
```yaml
output_format: markdown
include_rationale: true     # Why each requirement matters
include_alternatives: true  # Options considered
priority_scheme: moscow     # moscow | high-med-low | numbered
```

## Review
```yaml
require_all_domains: true
conflict_detection: true
gap_analysis: true
risk_threshold: medium      # Flag risks >= this level
```
