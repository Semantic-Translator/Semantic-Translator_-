# Architecture

## Processing pipeline

```text
Input text
   ↓
Language detection
   ↓
Domain detection
   ↓
Terminology extraction
   ↓
Semantic analysis
   ↓
Translation engine
   ↓
Terminology validation
   ↓
Quality control
   ↓
Final translation
```

## Main modules

- `backend/api` — application interface.
- `backend/translator` — translation engine.
- `backend/semantic` — semantic and domain analysis.
- `backend/ontology` — concept relations.
- `backend/rag` — retrieval-augmented generation.
- `backend/memory` — translation memory.
- `backend/database` — data access.
- `dictionaries` — subject terminology.
