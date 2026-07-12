# Vector Translation Memory

Translation Memory stores previously translated source-target pairs.

## Search modes

- exact match;
- lexical overlap;
- vector similarity;
- domain filtering;
- approved-only filtering.

## Reuse policy

An approved translation is reused automatically when its combined similarity score
reaches the configured threshold.

## Processing flow

```text
New source text
      ↓
Translation-memory search
      ↓
Approved high-score match?
   ┌──┴──┐
  yes    no
   ↓      ↓
Reuse   RAG + terminology generation
   └──┬──┘
      ↓
Quality scoring
      ↓
Final result
```
