# LLM orchestration

Version 0.5.0 separates the translation pipeline from the model provider.

## Pipeline

```text
Source text
   ↓
Translation memory
   ↓
Terminology retrieval
   ↓
RAG document context
   ↓
Deterministic candidate
   ↓
Prompt builder
   ↓
Provider router
   ├── local provider
   └── HTTP-compatible provider
   ↓
Final translation
   ↓
Generation log
```

## Default behavior

The local provider is enabled by default and requires no network connection.

## External provider

Set environment variables:

```text
SEMANTIC_LLM_PROVIDER=http
SEMANTIC_LLM_BASE_URL=http://localhost:11434/v1
SEMANTIC_LLM_API_KEY=
SEMANTIC_LLM_MODEL=qwen2.5
```

The HTTP adapter expects an OpenAI-compatible `/chat/completions` endpoint.
