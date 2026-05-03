# mindmap

> Graph generation — visualize the knowledge structure.

Read: `REF.md` · `config/settings.md` (`mindmap_depth`)

## Steps

1. **Find root**: topic-scoped → MOC note or most-linked concept; full vault → Home MOC in `maps/`.
2. **Build graph**: traverse outbound links up to `mindmap_depth` levels. Per node: title, type, maturity, top 3 links by strength.
3. **Generate MOC note** (`templates/moc.md`): group by Core Concepts → Developing Ideas → Open Questions → Sources.
4. **Generate Mermaid fallback**:
   ```mermaid
   mindmap
     root((Topic))
       SubtopicA
       SubtopicB
   ```
5. **Flag weak nodes** (mark with ⚠️ in MOC):
   - 0 inbound links from other concepts
   - questions with no `answers` link
   - episodes beyond `decay_window` without a concept link

## Output
Write MOC note to `vault_root/maps/<topic> MOC.md`.
Print: `✓ maps/<topic> MOC.md`
Then print the Mermaid block.
End: `NODES: N concepts, M episodes, X questions | WEAK: [list] | NEXT: "..."`
