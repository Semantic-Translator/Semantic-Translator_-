# Vector-oriented search

## Purpose

Vector search allows the system to retrieve terminology by semantic proximity,
not only by an exact text match.

## Current implementation

Version 0.2.0 uses a deterministic local hashing vectorizer:

- word n-grams;
- character n-grams;
- fixed vector dimensions;
- cosine similarity;
- JSON storage.

This implementation is lightweight, reproducible, and works without internet access.

## Pipeline

```text
Dictionary records
      ↓
Search-text construction
      ↓
Vectorization
      ↓
JSON vector index
      ↓
Query vectorization
      ↓
Cosine similarity
      ↓
Top-K semantic terms
      ↓
Retrieval-guided generation
```

## Future replacement

The `HashingVectorizer` can later be replaced with:

- Sentence Transformers;
- multilingual-e5;
- BGE-M3;
- Qwen embeddings;
- local GGUF embedding models;
- external embedding APIs.

The `VectorIndex.search()` interface can remain unchanged.
