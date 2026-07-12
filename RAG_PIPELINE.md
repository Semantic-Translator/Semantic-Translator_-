# Hybrid RAG pipeline

```text
Documents → loader → chunks → vectors → hybrid retrieval
→ terminology reranking → context assembly → generation
```

Default score:
- 70% vector similarity
- 20% lexical overlap
- 10% terminology relevance

The default mode is local and requires no external API.
