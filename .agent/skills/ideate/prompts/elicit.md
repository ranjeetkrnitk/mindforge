# elicit

> Structured requirements gathering across all domains.

## Steps

1. **Load** context from discover (if run)
2. **Iterate** domains per REF.md:
   - Announce: "Let's talk about **{{domain}}**..."
   - Ask 2-3 questions from REF.md (use `ask_user`, offer choices)
   - Summarize before next domain
3. **Prioritize** each requirement (Must/Should/Could/Won't)
4. **Track** coverage - mark domains complete

## Output

Table per domain with columns: ID, Requirement, Priority, Notes
End with coverage checkmarks and "Next: run review"

## Rules
- Max 3 questions per turn
- Offer choices when possible
- Summarize after each domain
