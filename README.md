# Semantic-Translator

AI-powered semantic translation platform for scientific and professional texts.

## Project goal

Semantic-Translator is designed to translate text with attention to:

- subject domain;
- terminology;
- context;
- semantic relations;
- translation memory;
- dictionaries and ontologies;
- future RAG and LLM integration.

## Version

Current archive version: `v0.5.0`

## Initial architecture

```text
Semantic-Translator/
├── backend/
│   ├── api/
│   ├── translator/
│   ├── semantic/
│   ├── ontology/
│   ├── rag/
│   ├── memory/
│   ├── database/
│   └── utils/
├── frontend/
├── dictionaries/
├── corpora/
├── prompts/
├── models/
├── docs/
├── tests/
├── examples/
├── requirements.txt
├── pyproject.toml
└── CHANGELOG.md
```

## Development principle

The project is developed in complete archive versions:

- `Semantic-Translator_v0.1.0.zip`
- `Semantic-Translator_v0.1.1.zip`
- `Semantic-Translator_v0.2.0.zip`

Each archive contains the full current state of the project.

## Planned stages

1. Project structure.
2. Terminology database.
3. Basic translation API.
4. Semantic analysis module.
5. Translation memory.
6. RAG integration.
7. LLM integration.
8. Web interface.

## License

MIT


## Version 0.1.1 capabilities

- Detects a likely subject domain from keywords.
- Loads terminology from JSON dictionaries.
- Searches terms by source word, translation, or Semantic-ID.
- Applies exact phrase replacements as a translation prototype.
- Provides API endpoints for domain detection and terminology lookup.


## Version 0.2.0: vector-oriented search and generation

This version introduces a local vector pipeline:

1. Terminology records are converted into normalized vectors.
2. Vectors are stored in a portable JSON index.
3. Search uses cosine similarity.
4. Retrieved terminology is passed into a context-oriented generation layer.
5. The solution works locally without an external API.

The default vectorizer is deterministic and dependency-free. It uses hashed character
and word features. A later version can replace it with Sentence Transformers or another
embedding model without changing the search interface.

### New API endpoints

- `POST /vectors/rebuild` — rebuild vector index.
- `POST /vectors/search` — semantic search.
- `POST /generate` — retrieval-oriented translation generation.
- `GET /vectors/status` — index status.


## Version 0.3.0 — Hybrid RAG

- ingestion of TXT, MD, JSON and CSV documents;
- chunking with overlap;
- local document vector index;
- hybrid vector and lexical search;
- terminology-aware reranking;
- unified RAG generation context;
- pluggable embedding providers;
- fully local default mode.

### API

- `POST /rag/ingest`
- `POST /rag/rebuild`
- `POST /rag/search`
- `POST /rag/generate`
- `GET /rag/status`


## Version 0.4.0 — Vector Translation Memory

Version 0.4.0 adds a persistent translation-memory layer:

- storage of approved translations;
- vector search over previous translations;
- exact, fuzzy and semantic matching;
- reuse of trusted translations;
- quality scoring;
- user feedback records;
- automatic preference for approved memory matches;
- RAG + terminology + translation-memory fusion.

### New API endpoints

- `POST /memory/add`
- `POST /memory/search`
- `POST /memory/rebuild`
- `GET /memory/status`
- `POST /memory/feedback`
- `POST /translate/advanced`


## Version 0.5.0 — LLM orchestration layer

Version 0.5.0 introduces a model-independent generation layer:

- unified LLM provider interface;
- local deterministic provider for offline operation;
- HTTP-compatible provider adapter;
- prompt assembly from terminology, RAG and translation memory;
- provider routing and fallback;
- request/response logging;
- configurable generation profiles;
- protected handling of API keys through environment variables;
- advanced generation endpoint.

The default mode remains fully local. External providers are optional.
