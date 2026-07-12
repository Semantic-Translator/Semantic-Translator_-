# Ontology JSON format

```json
{
  "nodes": [
    {
      "semantic_id": "BIO-000001",
      "domain": "biology",
      "labels": {
        "en": "cell",
        "ru": "клетка"
      },
      "aliases": {},
      "definition": "..."
    }
  ],
  "relations": [
    {
      "source_id": "BIO-000002",
      "relation_type": "part-of",
      "target_id": "BIO-000001",
      "confidence": 1.0
    }
  ]
}
```
