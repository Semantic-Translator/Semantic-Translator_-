# Retrieval-oriented generation

Version 0.2.0 generates a structured answer in three stages:

1. Detect subject domain.
2. Retrieve semantically related terminology.
3. Apply approved terminology and return the retrieval context.

The current generator is intentionally local and deterministic. It does not yet
rewrite complete sentences with a language model. Instead, it creates the exact
context required for a future LLM adapter.

## Output

- generated text;
- resolved domain;
- retrieved concepts;
- Semantic-ID values;
- similarity scores;
- terminology replacements;
- generation mode.
